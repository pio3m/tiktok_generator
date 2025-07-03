from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess
import os
from moviepy.editor import AudioFileClip

router = APIRouter()

DATA = "/app/data"

class SlugInput(BaseModel):
    slug: str

def run_cmd(cmd):
    """Uruchamia shell command i rzuca HTTPException w razie błędu."""
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"FFmpeg failed: {e}")

def generate_segment(slug, segment_name, overlay_img, audio_path, duration, enable_start, enable_end):
    """Generuje jeden segment wideo z overlay i audio"""
    base = f"/app/data/{slug}"
    seg_out = f"{base}/segments/{segment_name}.mp4"
    os.makedirs(os.path.dirname(seg_out), exist_ok=True)

    # Zapętl tło do potrzebnego czasu
    run_cmd(f"""
    ffmpeg -y -stream_loop -1 -i {base}/video/panning.mp4 \
    -t {duration} -c:v libx264 -preset ultrafast -an {base}/segments/{segment_name}_bg.mp4
    """)

    # Zamień overlay na wideo o pełnej długości segmentu
    overlay_mp4 = f"{base}/segments/{segment_name}_overlay.mp4"
    run_cmd(f"""
    ffmpeg -y -loop 1 -i {overlay_img} -t {duration} \
    -vf scale=1080:1920 -c:v libx264 -pix_fmt yuv420p {overlay_mp4}
    """)

    # Składanie segmentu
    run_cmd(f"""
    ffmpeg -y \
    -i {base}/segments/{segment_name}_bg.mp4 \
    -i {overlay_mp4} \
    -i {audio_path} \
    -filter_complex "
      [0:v][1:v]overlay=enable='between(t,{enable_start},{enable_end})'[v];
      [2:a]anull[audio]
    " \
    -map "[v]" -map "[audio]" \
    -c:v libx264 -preset ultrafast -c:a aac -movflags +faststart -shortest {seg_out}
    """)
    return seg_out

def concat_segments(slug, segments):
    """Łączy segmenty w finalne wideo."""
    base = f"/app/data/{slug}"
    list_path = f"{base}/segments/concat_list.txt"
    with open(list_path, "w") as f:
        for seg in segments:
            f.write(f"file '{seg}'\n")

    final_out = f"{base}/output/final.mp4"
    os.makedirs(os.path.dirname(final_out), exist_ok=True)

    run_cmd(f"""
    ffmpeg -y -f concat -safe 0 -i {list_path} -c copy {final_out}
    """)
    return final_out

@router.post("/generate-final-video", summary="Składa finalny TikTok quiz segmentami", tags=["renderer"])
def generate_final_video(payload: SlugInput):
    slug = payload.slug
    try:
        base = os.path.join(DATA, slug)
        audio_dir = os.path.join(base, "audio")
        img_dir = os.path.join(base, "images")

        # Wczytaj długości audio
        intro_dur = AudioFileClip(os.path.join(audio_dir, "intro.mp3")).duration
        question_dur = AudioFileClip(os.path.join(audio_dir, "question.mp3")).duration
        answers_dur = AudioFileClip(os.path.join(audio_dir, "answers.mp3")).duration
        reveal_dur = AudioFileClip(os.path.join(audio_dir, "reveal.mp3")).duration

        segments = []

        # Segment 1: Intro
        intro_seg = generate_segment(
            slug=slug,
            segment_name="intro",
            overlay_img=os.path.join(img_dir, "question.png"),
            audio_path=os.path.join(audio_dir, "intro.mp3"),
            duration=intro_dur + 0.5,  # + pauza
            enable_start=0,
            enable_end=intro_dur + 0.5
        )
        segments.append(intro_seg)

        # Segment 2: Question
        question_seg = generate_segment(
            slug=slug,
            segment_name="question",
            overlay_img=os.path.join(img_dir, "question.png"),
            audio_path=os.path.join(audio_dir, "question.mp3"),
            duration=question_dur + 0.5,
            enable_start=0,
            enable_end=question_dur + 0.5
        )
        segments.append(question_seg)

        # Segment 3: Answers
        answers_seg = generate_segment(
            slug=slug,
            segment_name="answers",
            overlay_img=os.path.join(img_dir, "output_buttons", "answer_A.png"),
            audio_path=os.path.join(audio_dir, "answers.mp3"),
            duration=answers_dur + 0.8,
            enable_start=0,
            enable_end=answers_dur + 0.8
        )
        segments.append(answers_seg)

        # Segment 4: Countdown (3 sekundy)
        countdown_seg = generate_segment(
            slug=slug,
            segment_name="countdown",
            overlay_img=os.path.join(img_dir, "countdown3.png"),  # można zmieniać w przyszłości
            audio_path=os.path.join(audio_dir, "beep.mp3"),  # opcjonalnie beep
            duration=3,
            enable_start=0,
            enable_end=3
        )
        segments.append(countdown_seg)

        # Segment 5: Reveal
        reveal_seg = generate_segment(
            slug=slug,
            segment_name="reveal",
            overlay_img=os.path.join(img_dir, "highlight_correct.png"),
            audio_path=os.path.join(audio_dir, "reveal.mp3"),
            duration=reveal_dur + 1,
            enable_start=0,
            enable_end=reveal_dur + 1
        )
        segments.append(reveal_seg)

        # Scalenie wszystkich segmentów w final.mp4
        final_out = concat_segments(slug, segments)

        return {"status": "success", "file": final_out, "segments": segments}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
