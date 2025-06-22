from fastapi import FastAPI, HTTPException
from sequence import generate_sequence, detect_correct_key

app = FastAPI()

@app.post("/generate-sequence")
def handle_generate_sequence():
    try:
       
        result = generate_sequence()
        return {"status": "success", "file": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Renderer API is running. POST to /generate-sequence"}
