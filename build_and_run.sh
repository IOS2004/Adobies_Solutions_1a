#!/bin/bash

# Build and Run Script for PDF Structure Extractor
# This script builds the Docker image and runs the PDF extraction process

set -e

IMAGE_NAME="pdf-extractor"
TAG="latest"

echo "Building PDF Structure Extractor Docker image..."
docker build --platform linux/amd64 -t ${IMAGE_NAME}:${TAG} .

echo "Docker image built successfully: ${IMAGE_NAME}:${TAG}"

# Check if input directory exists
if [ ! -d "input" ]; then
    echo "Creating input directory..."
    mkdir -p input
fi

# Check if output directory exists
if [ ! -d "output" ]; then
    echo "Creating output directory..."
    mkdir -p output
fi

# Check if there are PDF files in input
if [ ! "$(ls -A input/*.pdf 2>/dev/null)" ]; then
    echo "Warning: No PDF files found in input/ directory"
    echo "Please place PDF files in the input/ directory before running"
    exit 1
fi

echo "Running PDF extraction..."
docker run --rm \
    -v "$(pwd)/input:/app/input" \
    -v "$(pwd)/output:/app/output" \
    --network none \
    ${IMAGE_NAME}:${TAG}

echo "PDF extraction completed. Check the output/ directory for results."
