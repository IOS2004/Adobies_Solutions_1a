@echo off
REM Build and Run Script for PDF Structure Extractor (Windows)
REM This script builds the Docker image and runs the PDF extraction process

set IMAGE_NAME=pdf-extractor
set TAG=latest

echo Building PDF Structure Extractor Docker image...
docker build --platform linux/amd64 -t %IMAGE_NAME%:%TAG% .

if %ERRORLEVEL% neq 0 (
    echo Failed to build Docker image
    exit /b 1
)

echo Docker image built successfully: %IMAGE_NAME%:%TAG%

REM Check if input directory exists
if not exist "input" (
    echo Creating input directory...
    mkdir input
)

REM Check if output directory exists
if not exist "output" (
    echo Creating output directory...
    mkdir output
)

REM Check if there are PDF files in input
dir input\*.pdf >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Warning: No PDF files found in input\ directory
    echo Please place PDF files in the input\ directory before running
    exit /b 1
)

echo Running PDF extraction...
docker run --rm -v "%cd%\input:/app/input" -v "%cd%\output:/app/output" --network none %IMAGE_NAME%:%TAG%

if %ERRORLEVEL% neq 0 (
    echo PDF extraction failed
    exit /b 1
)

echo PDF extraction completed. Check the output\ directory for results.
