from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from moviepy.editor import *
import numpy as np
import os

router = APIRouter()

DATA = "/app/data"

class SlugInput(BaseModel):
    slug: str

@router.post(
    "/generate-background-video",
    summary="Generuje wideo tła z efektem panoramy kamery",
    description="Wersja 1.3: Dodano payload z polem slug, zapis pliku w katalogu quizu.",
    tags=["v1.3"]
)
def generate_background_video(payload: SlugInput):
    try:
        slug = payload.slug
        width, height = 1080, 1920
        duration = 12  # całkowity czas wideo

        out_dir = os.path.join(DATA, payload.slug)
        
        bg_image = os.path.join(out_dir  + "/images", "ultra.webp")
        if not os.path.exists(bg_image):
            raise HTTPException(status_code=404, detail="Background image not found")

        # Przygotuj katalog wyjściowy w folderze quizu
        out_dir = os.path.join(DATA, slug, "video")
        os.makedirs(out_dir, exist_ok=True)
        out_video = os.path.join(out_dir, "panning.mp4")

        img_clip = ImageClip(bg_image)
        img_w, img_h = img_clip.size

        # Skaluj tło do min. 1920 px wysokości
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
            return 0.5 * (1 - np.cos(np.pi * t))

        def make_frame(t):
            if t < duration / 2:
                progress = ease_in_out(t / (duration / 2))
            else:
                progress = ease_in_out(1 - (t - duration / 2) / (duration / 2))

            x_base = int(max_pan_x * progress)

            zoom_base = 1 + 0.1 * np.sin(2 * np.pi * t / 5)
            zoom_jitter = 0.02 * (np.sin(2 * np.pi * t / 3) + np.sin(2 * np.pi * t / 7))
            zoom_factor = zoom_base + zoom_jitter

            crop_w = int(width / zoom_factor)
            crop_h = int(height / zoom_factor)

            y_drift = int(40 * np.sin(2 * np.pi * t / 4))

            x = np.clip(x_base, 0, max(0, img_w - crop_w))
            y = np.clip((img_h - crop_h) // 2 + y_drift, 0, max(0, img_h - crop_h))

            frame = img_clip.get_frame(t)
            crop = frame[y:y + crop_h, x:x + crop_w, :]
            crop_clip = ImageClip(crop).resize((width, height))

            return crop_clip.get_frame(0)

        pan_clip = VideoClip(make_frame, duration=duration).set_fps(30)
        pan_clip.write_videofile(out_video, fps=30, codec="libx264")

        return {"status": "success", "file": out_video}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
