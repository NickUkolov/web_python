FROM python:3.10.4-slim-bullseye

COPY . /app
WORKDIR /app
RUN apt update && apt-get install ffmpeg libsm6 libxext6  -y && pip install --no-cache-dir -r /app/requirements.txt
ENTRYPOINT bash run_app.sh