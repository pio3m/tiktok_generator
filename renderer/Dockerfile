FROM python:3.10-slim

WORKDIR /app
COPY . /app

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    imagemagick \
    ghostscript \
    fonts-dejavu-core \
    libgl1 \
 && rm -rf /var/lib/apt/lists/*

# Nadpisanie policy.xml – pozwolenie na operacje na plikach
RUN echo '<?xml version="1.0" encoding="UTF-8"?>\
<!DOCTYPE policymap [\
<!ELEMENT policymap (policy*)>\
<!ELEMENT policy EMPTY>\
<!ATTLIST policy domain (resource|delegate|coder|filter|path) #REQUIRED>\
<!ATTLIST policy name CDATA #IMPLIED>\
<!ATTLIST policy pattern CDATA #IMPLIED>\
<!ATTLIST policy value CDATA #IMPLIED>\
<!ATTLIST policy rights CDATA #IMPLIED>\
<!ATTLIST policy stealth (True|False) "False">\
]>\
<policymap>\
  <policy domain="path" rights="read|write" pattern="@*" />\
</policymap>' > /etc/ImageMagick-6/policy.xml

# Instalacja zależności Python
RUN pip install --no-cache-dir -r requirements.txt

# 👇 Uruchomienie z autoreloadem
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
