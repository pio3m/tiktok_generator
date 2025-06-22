import os
os.environ["IMAGEMAGICK_BINARY"] = "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"

from moviepy.editor import (
    ImageClip, AudioFileClip, TextClip, CompositeVideoClip,
    concatenate_videoclips, ColorClip, CompositeAudioClip
)
from moviepy.video.fx.all import resize
from math import sin, pi

# --- KONFIG ---
VIDEO_SIZE = (1080, 1920)
FPS = 30

# --- ŚCIEŻKI ---
background_path = "../data/obraz.png"
voice_path = "../data/glos.mp3"
reveal_text_path = "../data/odpowiedz.txt"
avatar_path = "../assets/pan_zagadka.png"
ambient_path = "../assets/ambient.mp3"  # dodaj tę ścieżkę

# --- WCZYTAJ ---
with open(reveal_text_path, "r", encoding="utf-8") as f:
    reveal_text = f.read()

# --- TŁO Z ZOOMEM ---
def get_zoom_bg(duration):
    return ImageClip(background_path).resize(height=1920).set_duration(duration).set_fps(FPS)\
        .resize(lambda t: 1 + 0.01 * t)

# --- AVATAR ---
def get_avatar(duration):
    avatar = ImageClip(avatar_path).resize(width=350).set_duration(duration).fadein(1)
    scale_fx = lambda t: 1 + 0.05 * sin(2 * pi * t)
    return avatar.resize(scale_fx).set_position(("right", "bottom"))

# --- WJAZD TEKSTU ---
def get_intro_text(text, duration):
    clip = TextClip(text, fontsize=70, font="Arial-Bold", color="white", align="center", size=(900, None))
    return clip.set_position(lambda t: ('center', 1900 - 1000*t)).set_duration(duration).fadein(0.5)

# --- TIMER ---
def get_timer_clips():
    timer_clips = []
    for i in range(5, 0, -1):
        t_clip = TextClip(str(i), fontsize=120, font="Arial-Bold", color="white")
        t_clip = t_clip.set_duration(1).set_position(("center", "center"))
        timer_clips.append(t_clip)
    return timer_clips

# --- REVEAL (FLASH + TEKST) ---
def get_reveal_clip(text, duration):
    flash = ColorClip(size=VIDEO_SIZE, color=(255, 255, 255), duration=0.2)
    bg = ColorClip(size=VIDEO_SIZE, color=(0, 0, 0), duration=duration)
    reveal = TextClip("ODPOWIEDŹ: " + text, fontsize=70, font="Arial-Bold", color="white", align="center", size=(1000, None))
    reveal = reveal.set_position(("center", "center")).set_duration(duration).fadein(0.5)
    return concatenate_videoclips([flash, CompositeVideoClip([bg, reveal])])

# --- AUDIO ---
voice = AudioFileClip(voice_path)

ambient = AudioFileClip(ambient_path).subclip(0, voice.duration).volumex(0.1)
audio = CompositeAudioClip([voice, ambient])


# --- SEKWENCJE ---
intro = CompositeVideoClip([
    get_zoom_bg(6),
    get_avatar(6),
    get_intro_text("Na tym obrazie widać coś dziwnego...", 6)
], size=VIDEO_SIZE)

timer = concatenate_videoclips(get_timer_clips())

reveal = get_reveal_clip(reveal_text, 3)

# --- FINALNY KLIP ---
final = concatenate_videoclips([intro, timer, reveal], method="compose").set_audio(audio)
final.write_videofile("../output/film.mp4", fps=FPS)
