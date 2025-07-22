# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ /app/src/
COPY block_model.lgb .
COPY level_model.lgb .

# Make input and output directories
RUN mkdir -p /app/input /app/output

# Command to run the application
CMD ["python", "src/main.py"]
