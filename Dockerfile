# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for PDF processing and LightGBM
RUN apt-get update && apt-get install -y \
  libmupdf-dev \
  libgomp1 \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy model files
COPY block_model.lgb .
COPY level_model.lgb .
COPY block_label_encoder.joblib .
COPY level_label_encoder.joblib .

# Copy the application source code
COPY src/ /app/src/

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Set environment variables for better Python behavior in containers
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Command to run the application
CMD ["python", "src/main.py"]
