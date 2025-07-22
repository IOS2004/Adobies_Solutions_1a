import json
from pathlib import Path
from extractor import PDFExtractor

def main():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(exist_ok=True)

    extractor = PDFExtractor()

    for pdf_path in input_dir.glob("*.pdf"):
        try:
            print(f"Processing {pdf_path.name}...")
            structured_data = extractor.extract(pdf_path)
            
            output_path = output_dir / f"{pdf_path.stem}.json"
            with open(output_path, 'w') as f:
                json.dump(structured_data, f, indent=2)
            print(f"Successfully generated {output_path.name}")

        except Exception as e:
            print(f"Error processing {pdf_path.name}: {e}")

if __name__ == "__main__":
    main()
