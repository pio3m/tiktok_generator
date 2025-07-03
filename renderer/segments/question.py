import os
import subprocess
from moviepy.editor import AudioFileClip

DATA = "/app/data"

def generate_question_segment(slug: str):
    """
    Generuje segment question.mp4: tło + pytanie (z przezroczystością PNG),
    trwa dokładnie tyle, co question.mp3, w jednym kroku.
    """
    base = f"{DATA}/{slug}"
    bg_video = f"{base}/video/panning.mp4"
    audio = f"{base}/audio/question.mp3"
    question_img = f"{base}/images/question.png"
    segments_dir = f"{base}/segments"
    os.makedirs(segments_dir, exist_ok=True)

    # Zmierz długość audio
    question_audio = AudioFileClip(audio)
    duration = question_audio.duration
    print(f"Detected audio duration: {duration:.2f}s")

    output_file = f"{segments_dir}/question.mp4"

    # Jeden krok: tło loopowane + overlay PNG + audio + fade-in
    subprocess.run(
        f"ffmpeg -y "
        f"-stream_loop -1 -i {bg_video} "
        f"-loop 1 -i {question_img} "
        f"-i {audio} "
        f"-filter_complex \""
        f"[0:v]scale=1080:1920,setsar=1,trim=duration={duration}[bg];"
        f"[1:v]format=rgba,fade=t=in:st=0:d=0.5:alpha=1[ovr];"
        f"[bg][ovr]overlay=shortest=1:x=(main_w-overlay_w)/2:y=200[v]"
        f"\" "
        f"-map \"[v]\" -map 2:a "
        f"-c:v libx264 -preset veryfast -c:a aac -b:a 192k "
        f"-movflags +faststart -shortest {output_file}",
        shell=True, check=True
    )

    print("Question segment generated successfully.")
    return output_file
