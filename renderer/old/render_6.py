import os
os.environ["IMAGEMAGICK_BINARY"] = "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"

from datetime import datetime
from math import sin, pi
from moviepy.editor import (
    ImageClip, AudioFileClip, TextClip, CompositeVideoClip,
    concatenate_videoclips, ColorClip, CompositeAudioClip
)

# --- ŚCIEŻKI ---
VIDEO_SIZE = (1080, 1920)
FPS = 30

background_path = "../data/obraz.png"
voice_path = "../data/glos.mp3"
reveal_text_path = "../data/odpowiedz.txt"
avatar_path = "../assets/pan_zagadka.png"
ambient_path = "../assets/ambient.mp3"
font_path = "../assets/fonts/BebasNeue-Regular.ttf"

os.environ["IMAGEMAGICK_BINARY"] = "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"

# --- WCZYTAJ DANE ---
with open(reveal_text_path, "r", encoding="utf-8") as f:
    reveal_text = f.read()

# --- TŁO ---
def get_zoom_bg(duration):
    return ImageClip(background_path).resize(height=1920).set_duration(duration).set_fps(FPS)\
        .resize(lambda t: 1 + 0.01 * t)

# --- AVATAR ---
def get_avatar(duration):
    avatar = ImageClip(avatar_path).resize(width=350).set_duration(duration).fadein(1)
    scale_fx = lambda t: 1 + 0.05 * sin(2 * pi * t)
    return avatar.resize(scale_fx).set_position(("right", "bottom"))

# --- TEKST WJAZD Z DOŁU ---
def get_intro_text(text, duration):
    clip = TextClip(
        text,
        fontsize=90,
        font=font_path,
        color="#F72585",
        stroke_color="black",
        stroke_width=3,
        method="caption"
    )
    return clip.set_position(lambda t: ('center', 1900 - 1000*t)).set_duration(duration).fadein(0.5)

# --- TIMER ---
def get_timer_clips():
    timer_clips = []
    for i in range(5, 0, -1):
        t_clip = TextClip(
            str(i),
            fontsize=160,
            font=font_path,
            color="white",
            stroke_color="black",
            stroke_width=5,
            method="caption"
        ).set_opacity(0.6)\
         .set_duration(1)\
         .fadein(0.2).fadeout(0.2)\
         .set_position(("center", 200))
        timer_clips.append(t_clip)
    return timer_clips

# --- REVEAL + TEKST ---
def get_reveal_clip(text, duration):
    bg = ColorClip(size=VIDEO_SIZE, color=(0, 0, 0), duration=duration)
    reveal = TextClip(
        "ODPOWIEDŹ: " + text,
        fontsize=80,
        font=font_path,
        color="white",
        stroke_color="black",
        stroke_width=2,
        align="center",
        size=(1000, None),
        method="caption"
    ).set_position(("center", "center")).set_duration(duration).fadein(0.5)
    return CompositeVideoClip([bg, reveal])

# --- SHAKE + FLASH ---
def get_shake_with_flash(base_clip, duration=0.6):
    shaky = base_clip.set_position(lambda t: ("center", 960 + 15 * sin(40 * t))).set_duration(duration)
    flash = ColorClip(size=VIDEO_SIZE, color=(255,255,255), duration=0.2).set_opacity(0.9)
    return concatenate_videoclips([shaky, flash])

# --- AUDIO ---
voice = AudioFileClip(voice_path)
ambient = AudioFileClip(ambient_path).subclip(0, voice.duration).volumex(0.12)
audio = CompositeAudioClip([voice, ambient])

# --- KLIPY ---
intro = CompositeVideoClip([
    get_zoom_bg(6),
    get_avatar(6),
    get_intro_text("Zobacz uważnie ten kadr...", 6)
], size=VIDEO_SIZE)

timer = concatenate_videoclips(get_timer_clips())

reveal = get_reveal_clip(reveal_text, 2)
reveal_final = get_shake_with_flash(reveal, 0.5)

# --- SKLEJANIE ---
final = concatenate_videoclips([intro, timer, reveal_final], method="compose").set_audio(audio)

# --- NAZWA Z TIMESTAMPEM ---
filename = datetime.now().strftime("film_%Y%m%d_%H%M%S.mp4")
output_path = f"../output/{filename}"
final.write_videofile(output_path, fps=FPS)
print(f"✅ Zapisano: {output_path}")
