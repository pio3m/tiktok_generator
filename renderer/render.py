import os
os.environ["IMAGEMAGICK_BINARY"] = "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"

from moviepy.editor import (
    ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
)

from moviepy.video.fx.all import resize
from math import sin, pi

# --- Konfiguracja ---
VIDEO_SIZE = (1080, 1920)
FPS = 30

# --- Pliki wejściowe ---
background_path = "../data/obraz.png"
voice_path = "../data/glos.mp3"
avatar_path = "../assets/pan_zagadka.png"
text_path = "../data/text.txt"
reveal_text_path = "../data/odpowiedz.txt"  # nowy plik: zawiera rozwiązanie

# --- Wczytaj dane ---
with open(text_path, "r", encoding="utf-8") as f:
    intro_text = f.read()

with open(reveal_text_path, "r", encoding="utf-8") as f:
    reveal_text = f.read()

# --- Tło z efektem shake ---
def get_shaky_bg(duration):
    bg = ImageClip(background_path).resize(height=1920).set_duration(duration)
    return bg.set_position(lambda t: ("center", 960 + 10 * sin(5 * t))).set_fps(FPS)

# --- Avatar z efektem pulsowania ---
def get_pulsating_avatar(duration):
    avatar = ImageClip(avatar_path).resize(width=250).set_duration(duration)
    scale_fx = lambda t: 1 + 0.05 * sin(2 * pi * t)
    return avatar.resize(scale_fx).set_position(("right", "bottom"))


# --- Tekst (fade in/out + pozycja) ---
def get_text_clip(text, duration):
    return TextClip(text, fontsize=60, font="Arial-Bold", color="white", align="center", size=(900, None))\
        .set_duration(duration).set_position(("center", 200)).fadein(1).fadeout(1)

# --- Sekwencja 1: zagadka ---
intro_duration = 6
bg1 = get_shaky_bg(intro_duration)
avatar1 = get_pulsating_avatar(intro_duration)
text1 = get_text_clip(intro_text, intro_duration)

# --- Sekwencja 2: reveal ---
reveal_duration = 4
bg2 = get_shaky_bg(reveal_duration)
avatar2 = get_pulsating_avatar(reveal_duration)
text2 = get_text_clip("ODPOWIEDŹ: " + reveal_text, reveal_duration)

# --- Audio ---
audio = AudioFileClip(voice_path)

# --- Kompozycja ---
clip1 = CompositeVideoClip([bg1, avatar1, text1], size=VIDEO_SIZE)
clip2 = CompositeVideoClip([bg2, avatar2, text2], size=VIDEO_SIZE)
final_video = concatenate_videoclips([clip1, clip2]).set_audio(audio)

# --- Eksport ---
final_video.write_videofile("../output/film.mp4", fps=FPS)
