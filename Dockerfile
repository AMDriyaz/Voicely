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

# Copy your app code
COPY app.py .

# Install Python dependencies
RUN pip install TTS gradio

# Expose the Gradio port (7860)
EXPOSE 7860

# Start the app
CMD ["python", "app.py"]