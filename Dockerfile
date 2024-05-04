# Stage 1: Setup the base with Python 3.10 and install PyTorch
FROM python:3.10-slim-buster as builder

WORKDIR /usr/src/app

# Copy the requirements file
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch and other Python packages
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

# Stage 2: Prepare the runtime environment
FROM python:3.10-slim-buster

WORKDIR /usr/src/app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copy application files
COPY ./*.py /usr/src/app/
COPY templates/index.html /app/templates/
COPY static/* /usr/src/app/static/

# Cleaning up to keep the image clean and compact
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose the port the app runs on
EXPOSE 8081

# Command to run the application
CMD ["python", "./clip_server.py"]
