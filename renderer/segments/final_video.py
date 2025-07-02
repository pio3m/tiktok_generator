import os
import subprocess

DATA = "/app/data"

def generate_fast_final_video(slug: str):
    """
    Łączy segmenty w final.mp4 w katalogu slug/output, dodaje ambient w tle,
    z płynnymi przejściami między segmentami.
    """
    base = f"{DATA}/{slug}"
    segments_dir = f"{base}/segments"
    output_dir = f"{base}/output"
    final_output = f"{output_dir}/final.mp4"
    os.makedirs(output_dir, exist_ok=True)

    # Lista segmentów w kolejności, z countdown pomiędzy answers a reveal
    segments = [
        f"{segments_dir}/intro.mp4",
        f"{segments_dir}/question.mp4",
        f"{segments_dir}/answers.mp4",
        f"{segments_dir}/countdown.mp4",
        f"{segments_dir}/reveal.mp4",
    ]

    # 1️⃣ Przedłuż ostatni frame reveal, by uniknąć nagłego końca (tylko video, bez apad)
    reveal_ext = f"{segments_dir}/reveal_ext.mp4"
    subprocess.run(
        f"ffmpeg -y -i {segments[-1]} -vf tpad=stop_mode=clone:stop_duration=1 "
        f"-c:v libx264 -preset veryfast -c:a copy {reveal_ext}",
        shell=True, check=True
    )
    segments[-1] = reveal_ext

    # 2️⃣ Stwórz concat list
    list_path = f"{segments_dir}/concat_list.txt"
    with open(list_path, "w") as f:
        for seg in segments:
            f.write(f"file '{seg}'\n")

    temp_concat = f"{segments_dir}/temp_concat.mp4"

    # 3️⃣ Sklej segmenty z reenkodowaniem (żeby uniknąć twardych cięć)
    subprocess.run(
        f"ffmpeg -y -f concat -safe 0 -i {list_path} "
        f"-c:v libx264 -preset veryfast -c:a aac -b:a 192k "
        f"-movflags +faststart {temp_concat}",
        shell=True, check=True
    )

    # 4️⃣ Dodaj ambient jako tło audio i wykonaj finalny render
    ambient_audio = f"{DATA}/audio/ambient.mp3"
    subprocess.run(
        f"ffmpeg -y -i {temp_concat} -stream_loop -1 -i {ambient_audio} "
        f"-filter_complex \"[1:a]volume=0.2[amb];"
        f"[0:a][amb]amix=inputs=2:duration=first[aout]\" "
        f"-map 0:v -map \"[aout]\" -c:v libx264 -preset veryfast -c:a aac -b:a 192k "
        f"-shortest -movflags +faststart {final_output}",
        shell=True, check=True
    )

    print(f"Final video generated successfully: {final_output}")
    return final_output
