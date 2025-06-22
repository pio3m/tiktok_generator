import os
os.environ["IMAGEMAGICK_BINARY"] = "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"

from moviepy.editor import (
    ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip
)
from moviepy.video.fx.all import resize, fadein, fadeout
from math import sin, pi

# --- Konfiguracja ---
VIDEO_SIZE = (1080, 1920)
FPS = 30

# --- Pliki wejściowe ---
background_path = "../data/obraz.png"
voice_path = "../data/glos.mp3"
avatar_path = "../assets/pan_zagadka.png"
reveal_text_path = "../data/odpowiedz.txt"

# --- Wczytaj dane ---
with open(reveal_text_path, "r", encoding="utf-8") as f:
    reveal_text = f.read()

# --- Tło (bez rozciągania, zakładamy poprawny format) ---
def get_background(duration):
    return ImageClip(background_path).set_duration(duration).set_fps(FPS).resize(height=1920)

# --- Avatar z pulsacją i fade-in ---
def get_avatar(duration):
    avatar = ImageClip(avatar_path).resize(width=350).set_duration(duration).fadein(1)
    scale_fx = lambda t: 1 + 0.05 * sin(2 * pi * t)
    return avatar.resize(scale_fx).set_position(("right", "bottom"))

# --- Reveal na czarnym tle z fade-in ---
def get_reveal_clip(text, duration):
    bg = ColorClip(size=VIDEO_SIZE, color=(0, 0, 0), duration=duration)
    reveal = TextClip("ODPOWIEDŹ: " + text, fontsize=65, font="Arial-Bold", color="white", align="center", size=(900, None))
    reveal = reveal.set_position(("center", "center")).set_duration(duration).fadein(1).fadeout(1)
    return CompositeVideoClip([bg, reveal])

# --- Sekwencje ---
intro_duration = 6
reveal_duration = 4

bg1 = get_background(intro_duration)
avatar1 = get_avatar(intro_duration)
clip1 = CompositeVideoClip([bg1, avatar1], size=VIDEO_SIZE)

clip2 = get_reveal_clip(reveal_text, reveal_duration)

# --- Audio z fade-in/out ---
audio = AudioFileClip(voice_path).audio_fadein(0.5).audio_fadeout(1)

# --- Kompozycja finalna ---
final = concatenate_videoclips([clip1, clip2], method="compose").set_audio(audio)

# --- Eksport ---
final.write_videofile("../output/film.mp4", fps=FPS)
