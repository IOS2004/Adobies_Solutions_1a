import pdfplumber
import json
import pandas as pd
from pathlib import Path
from thefuzz import fuzz

def build_dataset():
    pdf_dir = Path("sample/sample_dataset/pdfs")
    json_dir = Path("sample/sample_dataset/outputs")
    
    all_features = []

    for pdf_path in pdf_dir.glob("*.pdf"):
        json_path = json_dir / f"{pdf_path.stem}.json"
        
        with open(json_path, 'r') as f:
            ground_truth = json.load(f)
        
        outline_texts = {o['text'].strip(): o['level'] for o in ground_truth['outline']}
        title_text = ground_truth['title'].strip()

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                words = page.extract_words(use_text_flow=True, extra_attrs=["fontname", "size"])
                
                if not words:
                    continue

                # Advanced line grouping
                lines = []
                current_line = []
                for word in words:
                    if not current_line or abs(word['top'] - current_line[-1]['top']) < 5:
                        current_line.append(word)
                    else:
                        lines.append(current_line)
                        current_line = [word]
                lines.append(current_line)

                for line in lines:
                    process_line(line, title_text, outline_texts, page.page_number, all_features)

    df = pd.DataFrame(all_features)
    df.to_csv("training_data.csv", index=False)
    print("Dataset created successfully: training_data.csv")

def process_line(line, title, outlines, page_num, all_features):
    text = " ".join(w['text'] for w in line).strip()
    if not text:
        return

    # Labeling with fuzzy matching
    label = "body_text"
    if fuzz.ratio(text, title) > 90:
        label = "title"
    else:
        for outline_text, level in outlines.items():
            if fuzz.ratio(text, outline_text) > 90:
                label = level
                break

    # Feature Engineering
    avg_size = sum(w['size'] for w in line) / len(line)
    is_bold = "bold" in line[0]['fontname'].lower()
    x_indentation = line[0]['x0']
    
    all_features.append({
        "text": text,
        "avg_size": avg_size,
        "is_bold": is_bold,
        "x_indentation": x_indentation,
        "page_num": page_num,
        "label": label
    })

if __name__ == "__main__":
    build_dataset()
