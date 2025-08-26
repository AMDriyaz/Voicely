# Base image with Python
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git espeak ffmpeg libsndfile1 && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY app.py .

RUN pip install TTS gradio

# Expose port 80 (CapRover default)
EXPOSE 80

# Run Gradio on port 80
CMD ["python", "app.py", "--server.port", "80", "--server.name", "0.0.0.0"]
