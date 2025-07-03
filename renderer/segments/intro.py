import os
import subprocess
from moviepy.editor import AudioFileClip

DATA = "/app/data"

def generate_intro_segment(slug: str):
    """
    Generuje segment intro.mp4: tło + intro audio + logo statycznie nałożone w prawym górnym rogu.
    """
    base = f"{DATA}/{slug}"
    video_input = f"{base}/video/panning.mp4"
    audio_input = f"{base}/audio/intro.mp3"
    logo_img = f"{DATA}/images/logo.png"
    output_dir = f"{base}/segments"
    output_file = f"{output_dir}/intro.mp4"

    os.makedirs(output_dir, exist_ok=True)

    # Zmierz długość intro.mp3
    intro_audio = AudioFileClip(audio_input)
    duration = intro_audio.duration

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", video_input,  # input 0: tło
        "-loop", "1", "-i", logo_img,             # input 1: logo jako pojedynczy obraz
        "-i", audio_input,                        # input 2: audio
        "-filter_complex",
        (
            f"[0:v]scale=1080:1920,setsar=1,trim=duration={duration}[bg];"
            f"[1:v]scale=300:-1[logo];"
            f"[bg][logo]overlay=shortest=1:x=W-w-50:y=50[v]"
        ),
        "-map", "[v]",
        "-map", "2:a",
        "-t", f"{duration}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        "-shortest",
        output_file
    ]
  
    try:
        print(f"Running FFmpeg command: {' '.join(cmd)}")
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("Intro segment generated successfully with static logo.")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed: {e.stderr.decode()}")
        raise RuntimeError(f"FFmpeg failed with exit code {e.returncode}")

    return output_file
