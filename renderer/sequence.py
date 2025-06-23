from fastapi import FastAPI, HTTPException
from moviepy.editor import *
import os

app = FastAPI()

DATA = "/app/data"
OUT = f"{DATA}/output/final.mp4"

# PARAMETRY MONTAŻU
TIMING = {
    "intro_duration": None,  # wyliczane
    "pause_after_intro": 0.5,
    "question_fadein": 0.5,
    "pause_after_question": 0.5,
    "answers_fadein": 0.5,
    "delay_between_answers": 0.3,
    "pause_after_answers": 0.8,
    "countdown_gap": 1.0,
    "highlight_delay": 0.5,
    "highlight_duration": 3,
}

@app.post("/generate-sequence")
def generate_sequence():
    try:
        width, height = 1080, 1920
        button_y_start, gap = 600, 150

        # 🔊 AUDIO
        intro_audio = AudioFileClip(f"{DATA}/audio/intro.mp3")
        question_audio = AudioFileClip(f"{DATA}/audio/question.mp3")
        answers_audio = AudioFileClip(f"{DATA}/audio/answers.mp3")
        reveal_audio = AudioFileClip(f"{DATA}/audio/reveal.mp3")
        beep = AudioFileClip(f"{DATA}/audio/beep.mp3").volumex(0.6)

        # 🎞️ TŁO
        total_duration = (
            intro_audio.duration +
            TIMING["pause_after_intro"] +
            question_audio.duration +
            TIMING["pause_after_question"] +
            answers_audio.duration +
            TIMING["pause_after_answers"] +
            3 * TIMING["countdown_gap"] +
            TIMING["highlight_delay"] +
            reveal_audio.duration + 1
        )

        bg = VideoFileClip(f"{DATA}/video/background.mp4").loop(duration=total_duration).resize((width, height))

        # CZASY STARTOWE POSZCZEGÓLNYCH SEGMENTÓW
        t_intro = 0
        t_question = t_intro + intro_audio.duration + TIMING["pause_after_intro"]
        t_answers = t_question + question_audio.duration + TIMING["pause_after_question"]
        t_countdown = t_answers + answers_audio.duration + TIMING["pause_after_answers"]
        t_reveal = t_countdown + 3 * TIMING["countdown_gap"] + TIMING["highlight_delay"]

        # 🖼️ PYTANIE (question.png)
        question_img_path = f"{DATA}/images/question.png"
        question_img = None
        if os.path.exists(question_img_path):
            question_img = (ImageClip(question_img_path)
                            .set_duration(question_audio.duration)
                            .set_start(t_question)
                            .fadein(TIMING["question_fadein"])
                            .set_position("center"))

        # 🅰️ ODPOWIEDZI A–D
        answers = []
        for i, key in enumerate(["A", "B", "C", "D"]):
            clip = (ImageClip(f"{DATA}/images/output_buttons/answer_{key}.png")
                    .set_position(("center", button_y_start + i * gap))
                    .set_duration(answers_audio.duration)
                    .fadein(TIMING["answers_fadein"])
                    .set_start(t_answers + i * TIMING["delay_between_answers"]))
            answers.append(clip)

        # ⏱️ COUNTDOWN
        countdown = []
        for i, num in enumerate(["3", "2", "1"]):
            txt = (TextClip(num, fontsize=200, color='white', font='DejaVu-Sans-Bold', method='caption')
                   .set_position("center")
                   .set_duration(1)
                   .set_start(t_countdown + i * TIMING["countdown_gap"])
                   .fadein(0.3).fadeout(0.3))
            countdown.append(txt)

        # ✅ HIGHLIGHT poprawnej odpowiedzi (zakładamy B = index 1)
        highlight = (ImageClip(f"{DATA}/images/output_buttons/highlight_correct.png")
                     .set_position(("center", button_y_start + 1 * gap))
                     .set_start(t_reveal)
                     .set_duration(TIMING["highlight_duration"])
                     .fadein(0.5))

        # 🔊 AUDIO MIX
        audio = CompositeAudioClip([
            intro_audio.set_start(t_intro),
            question_audio.set_start(t_question),
            answers_audio.set_start(t_answers),
            beep.set_start(t_countdown),
            beep.set_start(t_countdown + 1),
            beep.set_start(t_countdown + 2),
            reveal_audio.set_start(t_reveal)
        ])

        # FINALNA KOMPOZYCJA
        layers = [bg] + answers + countdown + [highlight]
        if question_img:
            layers.insert(1, question_img)

        full = CompositeVideoClip(layers).set_audio(audio)

        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        full.write_videofile(OUT, fps=30)

        return {"status": "success", "file": OUT}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Renderer API is running. POST to /generate-sequence"}
