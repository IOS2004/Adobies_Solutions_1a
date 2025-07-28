import json
import sys
from pathlib import Path
from extractor import PDFExtractor

def main():
    input_dir = Path("input")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Validate input directory exists and contains PDFs
    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist")
        sys.exit(1)

    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"Warning: No PDF files found in '{input_dir}' directory")
        return

    print(f"Found {len(pdf_files)} PDF file(s) to process")

    # Initialize extractor with model directory
    try:
        extractor = PDFExtractor(model_dir=".")
        print("PDF extractor initialized successfully")
    except Exception as e:
        print(f"Error initializing PDF extractor: {e}")
        sys.exit(1)

    processed_count = 0
    error_count = 0

    for pdf_path in pdf_files:
        try:
            print(f"Processing {pdf_path.name}...")
            structured_data = extractor.extract(pdf_path)
            
            output_path = output_dir / f"{pdf_path.stem}.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Successfully generated {output_path.name}")
            processed_count += 1

        except Exception as e:
            print(f"✗ Error processing {pdf_path.name}: {e}")
            error_count += 1
            
            # Create empty output file to maintain expected output structure
            output_path = output_dir / f"{pdf_path.stem}.json"
            empty_output = {"title": "", "outline": []}
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(empty_output, f, indent=2)

    print(f"\nProcessing complete: {processed_count} succeeded, {error_count} failed")
    
    if error_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
