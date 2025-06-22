from fastapi import FastAPI, HTTPException
from moviepy.editor import *
import os
from PIL import Image

app = FastAPI()

DATA = "/app/data"
OUT = f"{DATA}/output/final.mp4"

# Pillow: kompatybilność z wersją 10+
try:
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE = Image.ANTIALIAS

@app.post("/generate-sequence")
def generate_sequence():
    try:
        width = 1080
        height = 1920
        button_y_start = 600
        gap = 150
        button_duration = 4
        countdown_start = 5
        reveal_start = 8

        # 1. Background
        bg = VideoFileClip(f"{DATA}/video/background.mp4").loop(duration=12).resize((width, height))

        # 2. Intro audio
        intro_audio = AudioFileClip(f"{DATA}/audio/intro.mp3")
        bg = bg.set_audio(intro_audio)

        # 3. Buttons (A–D)
        answers = []
        for i, key in enumerate(["A", "B", "C", "D"]):
            clip = (ImageClip(f"{DATA}/images/output_buttons/answer_{key}.png")
                    .set_position(("center", button_y_start + i * gap))
                    .set_duration(button_duration)
                    .fadein(0.5)
                    .set_start(1 + i * 0.3))
            answers.append(clip)

        # 4. Countdown
        countdown_clips = []
        for i, num in enumerate(["3", "2", "1"]):
            txt = (TextClip(num, fontsize=200, color='white', font='Arial-Bold')
                   .set_position("center")
                   .set_duration(1)
                   .set_start(countdown_start + i)
                   .fadein(0.3).fadeout(0.3))
            countdown_clips.append(txt)

        # 5. Highlight (zawsze jeden plik)
        highlight = (ImageClip(f"{DATA}/images/output_buttons/highlight_correct.png")
                     .set_position(("center", button_y_start + 1 * gap))  # ← domyślnie druga pozycja (B)
                     .set_start(reveal_start)
                     .set_duration(3)
                     .fadein(0.5))

        # 6. Reveal audio
        outro_audio = AudioFileClip(f"{DATA}/audio/reveal.mp3")

        # 7. Składanie
        full = CompositeVideoClip([bg] + answers + countdown_clips + [highlight])
        full = full.set_audio(CompositeAudioClip([
            intro_audio.set_start(0),
            outro_audio.set_start(reveal_start)
        ]))

        # 8. Eksport
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        full.write_videofile(OUT, fps=30)

        return {"status": "success", "file": OUT}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
