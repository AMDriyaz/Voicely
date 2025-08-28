# --------------------------
# Base image with Python
# --------------------------
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install OS-level dependencies (speech + audio support)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        espeak \
        ffmpeg \
        libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip + setuptools + wheel (important for TTS builds)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy app code
COPY app.py .

# Install Python dependencies (no cache to save disk space)
RUN pip install --no-cache-dir TTS gradio

# CapRover dynamically injects PORT env variable
EXPOSE 80

# Start app with CapRover's PORT env
CMD ["python", "app.py"]
