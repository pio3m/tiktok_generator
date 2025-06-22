from fastapi import FastAPI, HTTPException
from moviepy.editor import *
import os

app = FastAPI()

DATA = "/app/data"
OUT = f"{DATA}/output/final.mp4"

@app.post("/generate-sequence")
def generate_sequence():
    try:
        width = 1080
        height = 1920
        button_y_start = 600
        gap = 150
        button_duration = 4

        # 1. Background
        bg = VideoFileClip(f"{DATA}/video/background.mp4").loop(duration=15).resize((width, height))

        # 2. Intro audio
        intro_audio = AudioFileClip(f"{DATA}/audio/intro.mp3")
        intro_duration = intro_audio.duration
        show_answers_start = intro_duration * 0.8
        countdown_start = intro_duration
        reveal_start = countdown_start + 5  # po odliczaniu 5s

        bg = bg.set_audio(intro_audio)

        # 3. Odpowiedzi A–D
        answers = []
        for i, key in enumerate(["A", "B", "C", "D"]):
            clip = (ImageClip(f"{DATA}/images/output_buttons/answer_{key}.png")
                    .set_position(("center", button_y_start + i * gap))
                    .set_duration(4)
                    .fadein(0.5)
                    .set_start(show_answers_start + i * 0.3))
            answers.append(clip)

        # 4. Countdown
        countdown_clips = []
        for i, num in enumerate(["3", "2", "1"]):
            txt = (TextClip(num, fontsize=200, color='white', font='DejaVu-Sans-Bold', method='caption')
                   .set_position("center")
                   .set_duration(1)
                   .set_start(countdown_start + i)
                   .fadein(0.3).fadeout(0.3))
            countdown_clips.append(txt)

        # 5. Beep audio (pikanie)
        beep_audio = AudioFileClip(f"{DATA}/audio/beep.mp3").volumex(0.6)
        beep_track = CompositeAudioClip([
            beep_audio.set_start(countdown_start),
            beep_audio.set_start(countdown_start + 1),
            beep_audio.set_start(countdown_start + 2)
        ])

        # 6. Highlight
        highlight = (ImageClip(f"{DATA}/images/output_buttons/highlight_correct.png")
                     .set_position(("center", button_y_start + 1 * gap))  # ← poprawna: B
                     .set_start(reveal_start)
                     .set_duration(3)
                     .fadein(0.5))

        # 7. Reveal audio
        outro_audio = AudioFileClip(f"{DATA}/audio/reveal.mp3").volumex(1.0)

        # 8. Composite
        full = CompositeVideoClip([bg] + answers + countdown_clips + [highlight])
        full = full.set_audio(CompositeAudioClip([
            intro_audio.set_start(0),
            beep_track,
            outro_audio.set_start(reveal_start)
        ]))

        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        full.write_videofile(OUT, fps=30)

        return {"status": "success", "file": OUT}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Renderer API is running. POST to /generate-sequence"}
