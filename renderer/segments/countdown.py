import os
import subprocess

DATA = "/app/data"

def generate_countdown_segment(slug: str):
    """
    Generuje segment countdown.mp4: tło + odliczanie 3-2-1 + beep w tle.
    """
    base = f"{DATA}/{slug}"
    bg_video = f"{base}/video/panning.mp4"
    beep_audio = f"{DATA}/audio/beep.mp3"  # uniwersalny beep
    segments_dir = f"{base}/segments"
    os.makedirs(segments_dir, exist_ok=True)

    duration = 3  # 3 sekundy na odliczanie
    output_file = f"{segments_dir}/countdown.mp4"

    # Zbuduj filter_complex do generowania tekstu 3-2-1 z fade-in/out
    filter_complex = (
        f"[0:v]scale=1080:1920,setsar=1,trim=duration={duration}[bg];"
        # Cyfra 3
        "[bg]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "text='3':fontsize=400:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:"
        "enable='between(t,0,1)'[v1];"
        # Cyfra 2
        "[v1]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "text='2':fontsize=400:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:"
        "enable='between(t,1,2)'[v2];"
        # Cyfra 1
        "[v2]drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "text='1':fontsize=400:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:"
        "enable='between(t,2,3)'[v]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", bg_video,
        "-stream_loop", "2", "-i", beep_audio,  # powtórz beep 3 razy
        "-filter_complex", filter_complex,
        "-map", "[v]", "-map", "1:a",
        "-t", f"{duration}",
        "-c:v", "libx264", "-preset", "veryfast", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", "-shortest", output_file
    ]

    try:
        print(f"Running FFmpeg command: {' '.join(cmd)}")
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("Countdown segment generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed: {e.stderr.decode()}")
        raise RuntimeError(f"FFmpeg failed with exit code {e.returncode}")

    return output_file
