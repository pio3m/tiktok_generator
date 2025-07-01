import os
import subprocess
from moviepy.editor import AudioFileClip

DATA = "/app/data"

def generate_reveal_segment(slug: str):
    """
    Generuje segment reveal.mp4: tło + highlight poprawnej odpowiedzi + audio reveal.mp3.
    """
    base = f"{DATA}/{slug}"
    bg_video = f"{base}/video/panning.mp4"
    audio = f"{base}/audio/reveal.mp3"
    highlight_img = f"{base}/images/output_buttons/highlight_correct.png"
    segments_dir = f"{base}/segments"
    os.makedirs(segments_dir, exist_ok=True)

    # Zmierz długość audio reveal.mp3
    reveal_audio = AudioFileClip(audio)
    duration = reveal_audio.duration
    print(f"Detected reveal audio duration: {duration:.2f}s")

    output_file = f"{segments_dir}/reveal.mp4"

    # Ustaw pozycję highlight (np. odpowiedź B → y=750)
    highlight_y = 750

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", bg_video,
        "-loop", "1", "-i", highlight_img,
        "-i", audio,
        "-filter_complex",
        (
            f"[0:v]scale=1080:1920,setsar=1,trim=duration={duration}[bg];"
            f"[1:v]format=rgba,fade=t=in:st=0:d=0.5:alpha=1[highlight];"
            f"[bg][highlight]overlay=shortest=1:x=(main_w-overlay_w)/2:y={highlight_y}[v]"
        ),
        "-map", "[v]",
        "-map", "2:a",
        "-t", f"{duration}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", "-shortest", output_file
    ]

    try:
        print(f"Running FFmpeg command: {' '.join(cmd)}")
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("Reveal segment generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed: {e.stderr.decode()}")
        raise RuntimeError(f"FFmpeg failed with exit code {e.returncode}")

    return output_file
