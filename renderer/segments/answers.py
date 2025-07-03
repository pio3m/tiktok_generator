import os
import subprocess
from moviepy.editor import AudioFileClip

DATA = "/app/data"

def generate_answers_segment(slug: str):
    """
    Generuje segment answers.mp4: tło + 4 odpowiedzi pojawiające się kolejno,
    trwa dokładnie tyle, co answers.mp3.
    """
    base = f"{DATA}/{slug}"
    bg_video = f"{base}/video/panning.mp4"
    audio = f"{base}/audio/answers.mp3"
    answers_imgs = [
        f"{base}/images/output_buttons/answer_A.png",
        f"{base}/images/output_buttons/answer_B.png",
        f"{base}/images/output_buttons/answer_C.png",
        f"{base}/images/output_buttons/answer_D.png",
    ]
    segments_dir = f"{base}/segments"
    os.makedirs(segments_dir, exist_ok=True)

    # Zmierz długość audio answers.mp3
    answers_audio = AudioFileClip(audio)
    duration = answers_audio.duration
    print(f"Detected answers audio duration: {duration:.2f}s")

    output_file = f"{segments_dir}/answers.mp4"

    # Zbuduj dynamiczny filter_complex
    filter_parts = [
        f"[0:v]scale=1080:1920,setsar=1,trim=duration={duration}[bg];"
    ]
    last = "[bg]"
    button_y = 600
    delay = 0.3
    for idx in range(4):
        label = f"btn{idx}"
        start = idx * delay
        y_pos = button_y + idx * 150
        filter_parts.append(
            f"[{idx+1}:v]format=rgba,fade=t=in:st={start}:d=0.5:alpha=1[{label}];"
            f"{last}[{label}]overlay=enable='gte(t,{start})':x=(main_w-overlay_w)/2:y={y_pos}[tmp{idx}];"
        )
        last = f"[tmp{idx}]"

    # Poprawka: usuń nadmiarowy średnik z ostatniego overlayu
    if filter_parts[-1].endswith(';'):
        filter_parts[-1] = filter_parts[-1][:-1]
    filter_complex = "".join(filter_parts)
    print(f"Generated filter_complex:\n{filter_complex}")

    # Buduj komendę FFmpeg
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", bg_video,
    ]

    # Dodaj inputy buttonów
    for img in answers_imgs:
        cmd.extend(["-loop", "1", "-i", img])

    # Dodaj audio
    cmd.extend(["-i", audio])

    cmd.extend([
        "-filter_complex", filter_complex,
        "-map", last,  # ostatni overlay chain
        "-map", f"{len(answers_imgs)+1}:a",  # audio input (po inputach obrazów)
        "-t", f"{duration}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", "-shortest", output_file
    ])

    try:
        print(f"Running FFmpeg command: {' '.join(cmd)}")
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("Answers segment generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed: {e.stderr.decode()}")
        raise RuntimeError(f"FFmpeg failed with exit code {e.returncode}")

    return output_file
