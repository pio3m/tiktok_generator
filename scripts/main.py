from fastapi import FastAPI, HTTPException
from answers import generate_answer_buttons, QuizData
from question_image import  generate_question_image, QuestionInput

app = FastAPI()


@app.post("/generate-buttons")
async def generate_buttons(quiz: QuizData):
    try:
        output_path = generate_answer_buttons(quiz)
        return {"status": "success", "output": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-question-image")
async def handle_generate_question_image(payload: QuestionInput):

    try:
        path = generate_question_image(payload.text)
        return {"status": "success", "file": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Quiz API is running. POST to /generate-buttons"}
