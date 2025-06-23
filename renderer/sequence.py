from fastapi import FastAPI, HTTPException
from moviepy.editor import *
import os

app = FastAPI()

DATA = "/app/data"
OUT = f"{DATA}/output/final.mp4"

@app.post("/generate-sequence")
def generate_sequence():
    try:
        width, height = 1080, 1920
        button_y_start, gap = 600, 150

        # 🎧 AUDIO SEGMENTY
        intro_audio = AudioFileClip(f"{DATA}/audio/intro.mp3")
        question_audio = AudioFileClip(f"{DATA}/audio/question.mp3")
        answers_audio = AudioFileClip(f"{DATA}/audio/answers.mp3")
        reveal_audio = AudioFileClip(f"{DATA}/audio/reveal.mp3")
        beep = AudioFileClip(f"{DATA}/audio/beep.mp3").volumex(0.6)

        intro_dur = intro_audio.duration
        question_dur = question_audio.duration
        answers_dur = answers_audio.duration
        countdown_start = intro_dur + question_dur + answers_dur
        reveal_start = countdown_start + 3  # po countdown

        total_duration = reveal_start + reveal_audio.duration + 1

        # 🎞️ TŁO
        bg = VideoFileClip(f"{DATA}/video/background.mp4").loop(duration=total_duration).resize((width, height))

        # 🖼️ PYTANIE – opcjonalna grafika
        question_img_path = f"{DATA}/images/question.png"
        question_img = None
        if os.path.exists(question_img_path):
            question_img = (ImageClip(question_img_path)
                            .set_duration(question_dur)
                            .set_start(intro_dur)
                            .fadein(0.5)
                            .set_position("center"))

        # 🔤 ODPOWIEDZI A–D
        answers = []
        answers_start = intro_dur + question_dur
        for i, key in enumerate(["A", "B", "C", "D"]):
            clip = (ImageClip(f"{DATA}/images/output_buttons/answer_{key}.png")
                    .set_position(("center", button_y_start + i * gap))
                    .set_duration(answers_dur)
                    .fadein(0.5)
                    .set_start(answers_start + i * 0.3))
            answers.append(clip)

        # ⏱️ COUNTDOWN
        countdown = []
        for i, num in enumerate(["3", "2", "1"]):
            txt = (TextClip(num, fontsize=200, color='white', font='DejaVu-Sans-Bold', method='caption')
                   .set_position("center")
                   .set_duration(1)
                   .set_start(countdown_start + i)
                   .fadein(0.3).fadeout(0.3))
            countdown.append(txt)

        # ✅ HIGHLIGHT poprawnej odpowiedzi (domyślnie B)
        highlight = (ImageClip(f"{DATA}/images/output_buttons/highlight_correct.png")
                     .set_position(("center", button_y_start + 1 * gap))
                     .set_start(reveal_start)
                     .set_duration(3)
                     .fadein(0.5))

        # 🔊 AUDIO CAŁOŚĆ
        audio = CompositeAudioClip([
            intro_audio.set_start(0),
            question_audio.set_start(intro_dur),
            answers_audio.set_start(intro_dur + question_dur),
            beep.set_start(countdown_start),
            beep.set_start(countdown_start + 1),
            beep.set_start(countdown_start + 2),
            reveal_audio.set_start(reveal_start)
        ])

        # 🎬 FINALNY KLIP
        layers = [bg] + answers + countdown + [highlight]
        if question_img:
            layers.insert(1, question_img)

        full = CompositeVideoClip(layers)
        full = full.set_audio(audio)

        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        full.write_videofile(OUT, fps=30)

        return {"status": "success", "file": OUT}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"message": "Renderer API is running. POST to /generate-sequence"}
