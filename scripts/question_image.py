from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
from pydantic import BaseModel
from fastapi import HTTPException

class QuestionInput(BaseModel):
    text: str
    slug: str

PREFIX_DIR = "/app/data"
OUT_PATH = "images"
FONT_PATH = os.path.join(PREFIX_DIR, "fonts", "DejaVuSans-Bold.ttf")

def generate_question_image(payload: QuestionInput):
    try:
        # Przygotowanie ścieżki wyjściowej
        out_dir = os.path.join(PREFIX_DIR, payload.slug, OUT_PATH)
        os.makedirs(out_dir, exist_ok=True)

        text = payload.text
        width = 1080
        font_size = 72
        outline_range = 2
        text_color = "#FFD700"
        outline_color = "black"

        font = ImageFont.truetype(FONT_PATH, font_size)
        lines = textwrap.wrap(text, width=25)
        line_height = font.getbbox("Ay")[3] + 20
        height = line_height * len(lines) + 40

        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        for i, line in enumerate(lines):
            bbox = font.getbbox(line)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = i * line_height + 20

            # Czarny kontur
            for dx in range(-outline_range, outline_range + 1):
                for dy in range(-outline_range, outline_range + 1):
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), line, font=font, fill=outline_color)

            # Tekst główny
            draw.text((x, y), line, font=font, fill=text_color)

        output_file = os.path.join(out_dir, "question.png")
        img.save(output_file)

        return {"status": "success", "file": os.path.join("/", OUT_PATH, "question.png")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
