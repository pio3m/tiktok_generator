import os
import subprocess

DATA = "/app/data"

def generate_intro_segment(slug: str):
    """
    Generuje segment intro.mp4: tło video panning + intro audio
    Zapisuje w katalogu {DATA}/{slug}/segments/intro.mp4
    """
    # Ścieżki do plików
    video_input = f"{DATA}/{slug}/video/panning.mp4"
    audio_input = f"{DATA}/{slug}/audio/intro.mp3"
    output_dir = f"{DATA}/{slug}/segments"
    output_file = f"{output_dir}/intro.mp4"

    # Upewnij się, że katalog na output istnieje
    os.makedirs(output_dir, exist_ok=True)

    # Komenda FFmpeg
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", video_input,
        "-i", audio_input,
        "-shortest",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-vf", "scale=1080:1920",
        output_file
    ]

    try:
        print(f"Running FFmpeg command: {' '.join(cmd)}")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("Intro segment generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed: {e.stderr.decode()}")
        raise RuntimeError(f"FFmpeg failed with exit code {e.returncode}")

    return output_file
