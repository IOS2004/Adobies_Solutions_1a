# PDF Structure Extractor

A machine learning-based solution for extracting structured outlines from PDF documents, including titles and hierarchical headings (H1, H2, H3) with page numbers.

## Overview

This project is part of the "Connecting the Dots" Challenge Round 1A, focusing on understanding document structure through intelligent PDF analysis. The solution uses LightGBM models to classify text blocks and determine heading hierarchies with high accuracy and speed.

## Features

- **Title Extraction**: Automatically identifies and extracts document titles
- **Hierarchical Heading Detection**: Classifies headings into H1, H2, H3 levels
- **Page Number Tracking**: Associates each heading with its page location
- **High Performance**: Processes 50-page PDFs in under 10 seconds
- **Offline Operation**: Works completely offline without internet connectivity
- **Multi-language Support**: Handles various document formats and languages

## Architecture

The solution consists of two main components:

### 1. Block Classification Model (`block_model.lgb`)

- Classifies text blocks into categories: Title, Heading, or Other
- Uses features: font size, bold formatting, indentation, page number
- Trained using LightGBM for fast inference

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
├── models/
│   ├── block_model.lgb   # Block classification model
│   ├── level_model.lgb   # Heading level classification model
│   ├── block_label_encoder.joblib  # Block label encoder
│   └── level_label_encoder.joblib  # Level label encoder
├── input/                # Input PDF files directory
├── output/              # Output JSON files directory
├── sample/              # Sample data and reference outputs
├── Dockerfile           # Container configuration
├── .dockerignore        # Docker build exclusions
├── requirements.txt     # Python dependencies
├── build_and_run.sh     # Linux/macOS build script
├── build_and_run.bat    # Windows build script
├── validate_output.py   # Output validation script
└── README.md           # This file
```

## Installation & Usage

### Quick Start (Recommended)

For easy deployment, use the provided build scripts:

**Linux/macOS:**

```bash
chmod +x build_and_run.sh
./build_and_run.sh
```

**Windows:**

```cmd
build_and_run.bat
```

These scripts will automatically:

1. Build the Docker image
2. Create input/output directories if needed
3. Validate that PDF files exist in the input directory
4. Run the extraction process
5. Report results

### Manual Docker Deployment

1. **Build the Docker image:**

   ```bash
   docker build --platform linux/amd64 -t pdf-extractor:latest .
   ```

2. **Run the container:**
   ```bash
   docker run --rm \
     -v $(pwd)/input:/app/input \
     -v $(pwd)/output:/app/output \
     --network none \
     pdf-extractor:latest
   ```

### Local Development

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Train models (if needed):**

   ```bash
   python train_model.py
   ```

3. **Run extraction:**
   ```bash
   python src/main.py
   ```

### Output Validation

Validate the generated JSON outputs against the expected schema:

```bash
python validate_output.py
```

This will check all JSON files in the output directory for:

- Correct JSON format
- Required fields (title, outline)
- Proper data types
- Valid heading levels (H1, H2, H3)
- Positive page numbers

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

- Uses labeled training data with ground truth annotations
- LightGBM classifiers for fast, accurate predictions
- Label encoders for categorical target variables
- Cross-validation for robust performance

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

## Recent Improvements

### Code Quality

- ✅ Enhanced error handling and logging in main.py
- ✅ Fixed variable naming consistency in extractor.py
- ✅ Added UTF-8 encoding support for international characters
- ✅ Improved Docker build optimization with better layer caching

### Deployment

- ✅ Added .dockerignore for faster, cleaner builds
- ✅ Created cross-platform build scripts (Linux/Windows)
- ✅ Added comprehensive output validation script
- ✅ Enhanced Dockerfile with system dependencies and environment variables

### Documentation

- ✅ Comprehensive README with clear setup instructions
- ✅ Detailed API documentation and usage examples
- ✅ Performance specifications and architecture overview
- ✅ Troubleshooting and validation guidance

## Limitations & Future Improvements

### Current Limitations

- Limited to H1, H2, H3 heading levels
- Requires training data for optimal performance
- May struggle with highly non-standard PDF layouts

### Potential Enhancements

- Support for additional heading levels (H4, H5, H6)
- Enhanced multilingual support
- Table of contents generation
- Integration with semantic search capabilities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is part of the "Connecting the Dots" Challenge and follows the competition guidelines.

## Support

For questions or issues:

- Check the sample data in the `sample/` directory
- Review the specifications in `specifications.txt`
- Examine test cases in the `test_*` files

---

_Built for the "Connecting the Dots" Challenge - Rethinking how we read, understand, and connect with documents._
