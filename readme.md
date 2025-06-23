# Dokumentacja – Projekt Quiz TikTok (ścieżka programistyczna)

## Cel projektu

Stworzenie w pełni zautomatyzowanego systemu do generowania wideo-quizów w stylu TikToka, zawierających:

- tło wideo,
- lektora (audio w częściach),
- dynamiczne przyciski odpowiedzi,
- odliczanie,
- highlight poprawnej odpowiedzi,
- zsynchronizowaną narrację i grafikę,
- nowoczesną, wiralową estetykę.

Projekt przygotowany w ramach Zadania 1 – Ścieżka programistyczna.

## Architektura

### Składniki:

| Element        | Opis                                                             |
|----------------|------------------------------------------------------------------|
| `n8n`          | Orkiestracja – automatyczne sterowanie przepływem                |
| `quiz-api`     | API pomocnicze: generowanie grafik, tekstów i przycisków         |
| `quiz-renderer`| Generowanie końcowego wideo (`final.mp4`) z synchronizacją       |
| ElevenLabs API | Generowanie 4 ścieżek audio z tekstu                             |
| GPT-4 API      | Generowanie tekstów lektora na podstawie pytania quizowego       |

## Wykorzystane technologie

- Python 3.10
- FastAPI
- MoviePy
- PIL (Pillow)
- FFmpeg
- PyAV (częściowo)
- Docker + Docker Compose
- n8n (no-code orchestration)
- ElevenLabs API (audio TTS)
- OpenAI GPT-4 (tekst generatywny)

## Przebieg automatyzacji (n8n workflow)

### Wejście:
```json
{
  "question": "Które buty mają charakterystyczną czerwoną podeszwę?",
  "A": "Nike Air Max",
  "B": "Timberlandy",
  "C": "Louboutiny",
  "D": "Crocs",
  "correct": "C",
  "category": "fashion"
}

```

# Quiz TikTok – Dokumentacja sekwencji i systemu

## Sekwencja

1. **Generowanie promptu GPT**

2. **GPT tworzy 4 sekcje tekstu:**
   - `intro_text`
   - `question_text`
   - `answers_text`
   - `reveal_text`

3. **4x ElevenLabs API generuje:**
   - `intro.mp3`
   - `question.mp3`
   - `answers.mp3`
   - `reveal.mp3`

4. **Generacja grafik:**
   - `POST /generate-buttons` → `answer_A.png` – `answer_D.png` + `highlight_correct.png`
   - `POST /generate-question-image` → `question.png`

5. **Render wideo (MoviePy):**
   - Tło (`background.mp4`)
   - `question.png`
   - Odpowiedzi A–D
   - Countdown z tekstem + beep
   - Highlight poprawnej odpowiedzi
   - Synchronizacja z audio
   - Efekty: fade, opóźnienia, zoomy itp.

6. **Eksport końcowy:**
   - `final.mp4`

---

## Struktura danych

/data
├── audio/
│ ├── intro.mp3
│ ├── question.mp3
│ ├── answers.mp3
│ ├── reveal.mp3
│ └── beep.mp3
├── images/
│ ├── question.png
│ └── output_buttons/
│ ├── answer_A.png
│ ├── answer_B.png
│ ├── answer_C.png
│ ├── answer_D.png
│ └── highlight_correct.png
├── video/
│ └── background.mp4
├── output/
│ └── final.mp4


---

## Parametryzacja renderu

Zdefiniowana w `generate_sequence()`:

```python
TIMING = {
  "pause_after_intro": 0.5,
  "question_fadein": 0.5,
  "pause_after_question": 0.5,
  "answers_fadein": 0.5,
  "delay_between_answers": 0.3,
  "pause_after_answers": 0.8,
  "countdown_gap": 1.0,
  "highlight_delay": 0.5,
  "highlight_duration": 3
}


