from fastapi import FastAPI, HTTPException
from segments.fast_full_pipeline import fast_full_pipeline
from segments.countdown import generate_countdown_segment
from segments.final_video import generate_fast_final_video
from segments.reveal import generate_reveal_segment
from segments.answers import generate_answers_segment
from segments.question import generate_question_segment
from segments.intro import generate_intro_segment
from sequence import generate_sequence
from final_video import SlugInput, router as final_video_router 
from background import router as background_router
app = FastAPI()

@app.post("/generate-sequence")
def handle_generate_sequence(slug: str):
    try:
       
        result = generate_sequence(slug)
        return {"status": "success", "file": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/generate-intro")
def handle_generate_intro(slug: str):
    """
    Endpoint do generowania intro.mp4 dla podanego sluga.
    """
    try:
        result = generate_intro_segment(slug)
        return {"status": "success", "file": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-question")
def handle_generate_question(slug: str):
    """
    Endpoint do generowania question.mp4 dla podanego sluga.
    """
    try:
        result = generate_question_segment(slug)
        return {"status": "success", "file": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-answers-segment", summary="Generuje segment z odpowiedziami")
def generate_answers_endpoint(payload: SlugInput):
    """
    Endpoint do generowania answers.mp4: tło + 4 odpowiedzi + audio answers.mp3.
    """
    try:
        result = generate_answers_segment(payload.slug)
        return {"status": "success", "file": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-reveal-segment", summary="Generuje segment z reveal")
def generate_reveal_endpoint(payload: SlugInput):
    """
    Endpoint do generowania reveal.mp4: tło + highlight poprawnej odpowiedzi + reveal.mp3.
    """
    try:
        result = generate_reveal_segment(payload.slug)
        return {"status": "success", "file": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-countdown-segment", summary="Generuje segment z odliczaniem")
def generate_countdown_endpoint(payload: SlugInput):
    """
    Endpoint do generowania countdown.mp4: tło + odliczanie + beep.
    """
    try:
        result = generate_countdown_segment(payload.slug)
        return {"status": "success", "file": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/fast-final-video", summary="Szybko generuje finalne wideo TikTok z ambientem")
def generate_fast_final_endpoint(payload: SlugInput):
    """
    Endpoint do szybkiego łączenia segmentów w final.mp4 z ambientem,
    zapisuje w katalogu slug/output/final.mp4.
    """
    try:
        result = generate_fast_final_video(payload.slug)
        return {"status": "success", "file": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/fast-full-pipeline", summary="Generuje pełne finalne wideo TikTok w jednym kroku")
def generate_full_pipeline_endpoint(payload: SlugInput):
    """
    Endpoint do automatycznego generowania wszystkich segmentów i final.mp4 w jednym kroku.
    """
    try:
        result = fast_full_pipeline(payload.slug)
        return {"status": "success", "file": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Dodaj router z background.py
app.include_router(background_router)
app.include_router(final_video_router)  

from fastapi.staticfiles import StaticFiles

DATA = "/app/data"
app.mount("/output", StaticFiles(directory=f"{DATA}/output"), name="output")

@app.get("/")
def root():
    return {"message": "Renderer API is running. POST to /generate-sequence"}
