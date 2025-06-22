from PIL import Image, ImageDraw, ImageFont
import os
import json

# 🔹 Ścieżki
input_file = "../data/quiz.json"
output_folder = "../data/output_buttons"
font_path = "../assets/fonts/DejaVuSans-Bold.ttf"

# 🔹 Wczytaj dane z quiz.json
with open(input_file, "r", encoding="utf-8") as f:
    quiz_data = json.load(f)

# 🔹 Ustawienia graficzne
width, height = 900, 120
font_size = 48
font_color = "white"
bg_color = "#333355"
highlight_color = "#22ff22"

# 🔹 Upewnij się, że folder wyjściowy istnieje
os.makedirs(output_folder, exist_ok=True)

# 🔹 Generuj obrazki odpowiedzi A–D
for key in ["A", "B", "C", "D"]:
    text = f"{key}: {quiz_data[key]}"
    is_correct = key == quiz_data["correct"]
    bg = highlight_color if is_correct else bg_color

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle([(0, 0), (width, height)], radius=30, fill=bg)

    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textsize(text, font=font)
    draw.text(
        ((width - text_width) // 2, (height - text_height) // 2),
        text,
        font=font,
        fill=font_color
    )

    output_path = os.path.join(output_folder, f"answer_{key}.png")
    img.save(output_path)

# 🔹 Nagłówek z pytaniem
question_text = quiz_data.get("question", "")
question_img = Image.new("RGBA", (width, 160), (0, 0, 0, 0))
q_draw = ImageDraw.Draw(question_img)
font_q = ImageFont.truetype(font_path, 44)
q_text_width, q_text_height = q_draw.textsize(question_text, font=font_q)
q_draw.text(((width - q_text_width) // 2, 40), question_text, font=font_q, fill=font_color)
question_img.save(os.path.join(output_folder, "question_header.png"))

print("✅ Wszystkie grafiki zostały wygenerowane.")
