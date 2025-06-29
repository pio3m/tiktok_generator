from fastapi import APIRouter, HTTPException
from moviepy.editor import *
import numpy as np
import os

router = APIRouter()

DATA = "/app/data"
BG_IMAGE = f"{DATA}/ultra.webp"
OUT_VIDEO = f"{DATA}/output/panning.mp4"

@router.post("/generate-background-video",  tags=["v1.4"])
def generate_background_video():
    try:
        width, height = 1080, 1920
        duration = 12  # całkowity czas wideo

        if not os.path.exists(BG_IMAGE):
            raise HTTPException(status_code=404, detail="Background image not found")

        img_clip = ImageClip(BG_IMAGE)
        img_w, img_h = img_clip.size

        # Przeskaluj tło do co najmniej 1920px wysokości
        if img_h < height:
            img_clip = img_clip.resize(height=height)
            img_w, img_h = img_clip.size

        max_pan_x = img_w - width
        if max_pan_x <= 0:
            raise HTTPException(
                status_code=400,
                detail=f"Background too narrow for horizontal panning after scaling (width={img_w}px). Need >1080px."
            )
 
        def ease_in_out(t):
            """Funkcja easing: przyspieszenie na początku, zwolnienie na końcu"""
            return 0.5 * (1 - np.cos(np.pi * t))

        def make_frame(t):
            # easing ruch lewo->prawo i z powrotem
            if t < duration / 2:
                progress = ease_in_out(t / (duration / 2))
            else:
                progress = ease_in_out(1 - (t - duration / 2) / (duration / 2))

            x_base = int(max_pan_x * progress)

            # mocniejszy zoom: ±10% (0.9-1.1)
            zoom_base = 1 + 0.1 * np.sin(2 * np.pi * t / 5)  # cykl 5s

            # dodaj subtelną, płynną losowość do zoomu i pozycji (pseudo perlin)
            zoom_jitter = 0.02 * (np.sin(2 * np.pi * t / 3) + np.sin(2 * np.pi * t / 7))  # fluktuacje ±2%
            zoom_factor = zoom_base + zoom_jitter

            # oblicz zmienne rozmiary kadru
            crop_w = int(width / zoom_factor)
            crop_h = int(height / zoom_factor)
 
            # losowe, powolne odchylenie w pionie (delikatny "drift" góra/dół, cykl ~4s)
            y_drift = int(40 * np.sin(2 * np.pi * t / 4))  # od -40 do +40 px

            x = np.clip(x_base, 0, max(0, img_w - crop_w))
            y = np.clip((img_h - crop_h) // 2 + y_drift, 0, max(0, img_h - crop_h))

            frame = img_clip.get_frame(t)
            crop = frame[y:y + crop_h, x:x + crop_w, :]

            # resize do finalnego kadru TikTok
            crop_clip = ImageClip(crop).resize((width, height))

            return crop_clip.get_frame(0)





        pan_clip = VideoClip(make_frame, duration=duration).set_fps(30)
        os.makedirs(os.path.dirname(OUT_VIDEO), exist_ok=True)
        pan_clip.write_videofile(OUT_VIDEO, fps=30, codec="libx264")

        return {"status": "success", "file": OUT_VIDEO}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
