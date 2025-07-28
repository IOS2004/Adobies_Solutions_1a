# PDF Structure Extractor

A machine learning-based solution for extracting structured outlines from PDF documents, including titles and hierarchical headings (H1, H2, H3) with page numbers.

## Overview

This project is part of the "Connecting the Dots" Challenge Round 1A, focusing on understanding document structure through intelligent PDF analysis. The solution uses LightGBM models to classify text blocks and determine heading hierarchies.

## Features

- **Title Extraction**: Automatically identifies and extracts document titles
- **Hierarchical Heading Detection**: Classifies headings into H1, H2, H3 levels
- **Page Number Tracking**: Associates each heading with its page location
- **High Performance**: Processes PDFs in under 10 seconds
- **Offline Operation**: Works completely offline without internet connectivity
- **Docker Deployment**: Containerized for consistent cross-platform execution

## Architecture

The solution consists of two main components:

### 1. Block Classification Model (`block_model.lgb`)

- Classifies text blocks into categories: Title, Heading, or Other
- Uses features: font size, bold formatting, indentation, page number
- Trained using synthetic data based on common PDF patterns

### 2. Level Classification Model (`level_model.lgb`)

- Determines heading levels (H1, H2, H3) for identified headings
- Uses the same feature set as block classification
- Provides hierarchical structure understanding

## Technology Stack

- **Python 3.9**: Core runtime environment
- **PyMuPDF (fitz)**: PDF text extraction and styling information
- **LightGBM**: Machine learning models for classification
- **scikit-learn**: Label encoding and preprocessing
- **pandas**: Data manipulation and analysis
- **joblib**: Model serialization

## Project Structure

```
├── src/
│   ├── main.py           # Main application entry point
│   └── extractor.py      # PDF extraction and processing logic
├── input/                # Input PDF files directory (5 sample PDFs)
├── output/              # Output JSON files directory
├── sample/              # Sample data and reference implementation
├── block_model.lgb      # Block classification model (292KB)
├── level_model.lgb      # Heading level classification model (225KB)
├── block_label_encoder.joblib  # Block label encoder
├── level_label_encoder.joblib  # Level label encoder
├── train_models.py      # Model training script
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
├── validate_output.py  # Output validation script
├── specifications.txt  # Project requirements
└── README.md          # This file
```

## Installation & Usage

### Quick Start with Docker (Recommended)

1. **Build the Docker image:**

   ```bash
   docker build -t pdf-extractor .
   ```

2. **Run the container:**

   ```bash
   docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" pdf-extractor
   ```

   **Windows PowerShell:**

   ```powershell
   docker run --rm -v "${PWD}\input:/app/input" -v "${PWD}\output:/app/output" pdf-extractor
   ```

### Local Development

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Train models (if needed):**

   ```bash
   python train_models.py
   ```

3. **Run extraction:**
   ```bash
   python src/main.py
   ```

### Output Validation

Validate the generated JSON outputs:

```bash
python validate_output.py
```

## Input/Output Format

### Input

- Place PDF files in the `input/` directory
- Supports PDFs up to 50 pages
- No preprocessing required

### Output

The solution generates JSON files in the following format:

```json
{
  "title": "Understanding AI",
  "outline": [
    {
      "level": "H1",
      "text": "Introduction",
      "page": 1
    },
    {
      "level": "H2",
      "text": "What is AI?",
      "page": 2
    },
    {
      "level": "H3",
      "text": "History of AI",
      "page": 3
    }
  ]
}
```

## Algorithm Approach

### Feature Engineering

The solution extracts four key features from PDF text spans:

- **Font Size (`avg_size`)**: Primary indicator of text importance
- **Bold Formatting (`is_bold`)**: Secondary styling cue for headings
- **Horizontal Position (`x_indentation`)**: Indicates hierarchical level
- **Page Number (`page_num`)**: Document position context

### Two-Stage Classification

1. **Block Type Classification**: Distinguishes titles, headings from body text
2. **Level Classification**: Determines hierarchical levels (H1, H2, H3) for headings

### Model Training

- Uses synthetic training data based on common PDF patterns
- LightGBM classifiers for fast, accurate predictions
- Label encoders for categorical target variables
- Heuristic-based feature generation for robust performance

## Performance Specifications

| Metric         | Requirement                | Achieved |
| -------------- | -------------------------- | -------- |
| Execution Time | ≤ 10 seconds (50-page PDF) | ✅       |
| Model Size     | ≤ 200MB                    | ✅       |
| Network Access | Offline only               | ✅       |
| Architecture   | CPU (amd64)                | ✅       |
| Memory         | 16GB RAM max               | ✅       |

## Key Design Decisions

1. **Machine Learning Over Heuristics**: Instead of relying solely on font sizes, the solution uses ML models to handle PDFs with inconsistent styling.

2. **Two-Stage Pipeline**: Separating block classification from level classification improves accuracy and modularity.

3. **Robust Feature Set**: Combining multiple text properties (size, style, position) provides better generalization.

4. **Fallback Mechanisms**: Title extraction includes fallbacks for edge cases where ML predictions may fail.

5. **Docker Optimization**: Multi-stage builds and slim base images minimize container size while ensuring compatibility.

6. **Error Handling**: Comprehensive error handling ensures graceful failure and maintains expected output structure.

7. **Validation Tools**: Built-in validation ensures output quality and format compliance.

## Current Status

### ✅ Working Features

- Docker containerization with proper dependencies
- PDF text extraction and feature engineering
- Two-stage ML classification (block type and heading level)
- JSON output generation with valid schema
- Offline processing (no network required)
- Model files under 200MB size constraint

### 🔧 Areas for Improvement

- Model accuracy could be enhanced with real training data
- Title extraction needs refinement
- Heading level classification requires tuning
- Some duplicate headings in output need filtering

### Recent Improvements

- ✅ Fixed LightGBM dependency issues (`libgomp1`)
- ✅ Created working model files using synthetic training data
- ✅ Successful Docker deployment and testing
- ✅ All output files pass validation checks

## Limitations & Future Improvements

### Current Limitations

- Models trained on synthetic data rather than real PDF annotations
- Limited to H1, H2, H3 heading levels
- May produce duplicate headings or misclassified levels
- Title extraction sometimes picks generic headers

### Potential Enhancements

- Train models on manually labeled PDF data for better accuracy
- Implement post-processing to filter duplicate headings
- Add confidence scoring for predictions
- Support for additional heading levels (H4, H5, H6)
- Enhanced title detection with document context

## Contributing

This project was developed for the "Connecting the Dots" Challenge Round 1A.

## License

This project follows the competition guidelines for the "Connecting the Dots" Challenge.
