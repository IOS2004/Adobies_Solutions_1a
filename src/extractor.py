import fitz  # PyMuPDF
import pandas as pd
import lightgbm as lgb
import joblib
from pathlib import Path

class PDFExtractor:
    def __init__(self, model_dir="."):
        model_path = Path(model_dir)
        self.model_block = lgb.Booster(model_file=model_path / 'block_model.lgb')
        self.model_level = lgb.Booster(model_file=model_path / 'level_model.lgb')
        self.le_block = joblib.load(model_path / 'block_label_encoder.joblib')
        self.le_level = joblib.load(model_path / 'level_label_encoder.joblib')
        self.features = ['avg_size', 'is_bold', 'x_indentation', 'page_num']

    def extract(self, pdf_path):
        doc = fitz.open(pdf_path)
        
        # 1. Extract text blocks with style information
        text_blocks = self._get_text_blocks(doc)
        if not text_blocks:
            return {"title": "", "outline": []}

        # 2. Convert to DataFrame for model prediction
        df = pd.DataFrame(text_blocks)
        df['avg_size'] = df['font_size']
        df['x_indentation'] = df['bbox'].apply(lambda bbox: bbox[0])

        # 3. Predict block types (heading, title, etc.)
        block_predictions = self.model_block.predict(df[self.features])
        df['block_label_encoded'] = block_predictions.argmax(axis=1)
        df['block_label'] = self.le_block.inverse_transform(df['block_label_encoded'])

        # 4. Extract Title
        title_df = df[df['block_label'] == 'Title'].copy()
        title = self._extract_title(title_df, df)

        # 5. Predict heading levels
        headings_df = df[df['block_label'] == 'heading'].copy()
        if not headings_df.empty:
            level_predictions = self.model_level.predict(headings_df[self.features])
            headings_df['level_label_encoded'] = level_predictions.argmax(axis=1)
            headings_df['level'] = self.le_level.inverse_transform(headings_df['level_label_encoded'])
            
            # 6. Generate the outline
            outline = self._generate_outline(headings_df)
        else:
            outline = []

        # Remove title from outline if it was captured as a heading
        if title and outline and outline[0]['text'] == title:
            outline.pop(0)

        return {
            "title": title,
            "outline": outline
        }

    def _get_text_blocks(self, doc):
        """Extracts all text blocks with style and position info."""
        text_blocks = []
        for page_num, page in enumerate(doc):
            blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)["blocks"]
            for block in blocks:
                if block["type"] == 0:  # Text block
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if span["text"].strip():
                                text_blocks.append({
                                    "text": span["text"].strip(),
                                    "font_size": round(span["size"]),
                                    "font_name": span["font"],
                                    "is_bold": "bold" in span["font"].lower(),
                                    "color": span["color"],
                                    "page_num": page_num + 1,
                                    "bbox": span["bbox"]
                                })
        return text_blocks

    def _extract_title(self, title_df, all_df):
        """Extracts the document title using model predictions or fallbacks."""
        if not title_df.empty:
            title_df['bbox_y1'] = title_df['bbox'].apply(lambda bbox: bbox[1])
            title_df = title_df.sort_values(by=['page_num', 'bbox_y1'], ascending=[True, True])
            return title_df.iloc[0]['text']

        # Fallback: Find the text with the largest font size on the first page.
        first_page_blocks = all_df[all_df['page_num'] == 1].copy()
        if not first_page_blocks.empty:
            first_page_blocks['bbox_y1'] = first_page_blocks['bbox'].apply(lambda bbox: bbox[1])
            first_page_blocks = first_page_blocks.sort_values(by=['font_size', 'bbox_y1'], ascending=[False, True])
            return first_page_blocks.iloc[0]['text']
        
        return ""

    def _generate_outline(self, headings_df):
        """Builds the outline from the dataframe of predicted headings."""
        if headings_df.empty:
            return []
            
        headings_df['bbox_y1'] = headings_df['bbox'].apply(lambda bbox: bbox[1])
        
        # Sort by page and then by vertical position
        sorted_headings = headings_df.sort_values(by=['page_num', 'bbox_y1'])

        outline = []
        for _, row in sorted_headings.iterrows():
            outline.append({
                "level": row["level"],
                "text": row["text"],
                "page": row["page_num"]
            })
        return outline
