FROM python:3.10-slim

WORKDIR /app
COPY . /app

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    imagemagick \
    fonts-dejavu-core \
    libgl1 \
 && rm -rf /var/lib/apt/lists/*

# Instalacja zależności Python
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
