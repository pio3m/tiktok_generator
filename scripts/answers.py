from pydantic import BaseModel
from typing import Literal
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# Konfiguracja
OUTPUT_DIR = "/app/data/images/output_buttons"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Upewnij się, że folder istnieje
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Dane wejściowe
class QuizData(BaseModel):
    A: str
    B: str
    C: str
    D: str
    correct: Literal["A", "B", "C", "D"]

# Funkcja rysująca pojedynczy przycisk
def draw_button_image(text, width=900, height=120, bg="#333355", font=None, font_color="white", shadow=True):
    shadow_offset = 10
    shadow_radius = 15

    # Cień
    if shadow:
        shadow_img = Image.new("RGBA", (width + shadow_offset * 2, height + shadow_offset * 2), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_img)
        shadow_draw.rounded_rectangle(
            [(shadow_offset, shadow_offset), (width + shadow_offset, height + shadow_offset)],
            radius=30,
            fill=(0, 0, 0, 100)
        )
        shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(shadow_radius))
    else:
        shadow_img = None

    # Główna warstwa przycisku
    button_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(button_img)
    draw.rounded_rectangle([(0, 0), (width, height)], radius=30, fill=bg)

    # Tekst
    box = font.getbbox(text)
    text_width = box[2] - box[0]
    text_height = box[3] - box[1]
    draw.text(
        ((width - text_width) // 2, (height - text_height) // 2),
        text,
        font=font,
        fill=font_color
    )

    # Złożenie z cieniem
    if shadow_img:
        final = Image.new("RGBA", shadow_img.size, (0, 0, 0, 0))
        final.paste(shadow_img, (0, 0))
        final.paste(button_img, (shadow_offset, shadow_offset), mask=button_img)
        return final
    else:
        return button_img

# Główna funkcja API
def generate_answer_buttons(quiz: QuizData):
    width, height = 900, 120
    font_size = 48
    font_color = "white"
    base_color = "#333355"
    highlight_color = "#22ff22"
    font = ImageFont.truetype(FONT_PATH, font_size)

    # 1. Przyciski standardowe
    for key in ["A", "B", "C", "D"]:
        text = f"{key}: {getattr(quiz, key)}"
        img = draw_button_image(text, width, height, bg=base_color, font=font, font_color=font_color)
        img.save(os.path.join(OUTPUT_DIR, f"answer_{key}.png"))

    # 2. Osobno podświetlenie poprawnej odpowiedzi
    correct_key = quiz.correct
    correct_text = f"{correct_key}: {getattr(quiz, correct_key)}"
    highlight_img = draw_button_image(correct_text, width, height, bg=highlight_color, font=font, font_color=font_color)
    highlight_img.save(os.path.join(OUTPUT_DIR, "highlight_correct.png"))

    return OUTPUT_DIR
