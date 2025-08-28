# Base image with Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install OS-level dependencies
RUN apt-get update && \
    apt-get install -y git espeak ffmpeg libsndfile1 && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy app code
COPY app.py .

# Install Python dependencies
RUN pip install TTS gradio

# CapRover injects $PORT, so we just EXPOSE it (default is 8080 for local dev)
EXPOSE 8080

# Run app
CMD ["python", "app.py"]
