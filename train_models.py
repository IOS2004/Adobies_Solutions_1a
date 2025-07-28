#!/usr/bin/env python3
"""
Training script to generate LightGBM models for PDF structure extraction.
This creates models based on heuristic rules derived from PDF analysis.
"""

import numpy as np
import pandas as pd
import lightgbm as lgb
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import fitz  # PyMuPDF
import os
from pathlib import Path

def extract_features_from_pdf(pdf_path):
    """Extract features from a PDF for training data."""
    doc = fitz.open(pdf_path)
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
                                "is_bold": "bold" in span["font"].lower() or span["flags"] & 2**4,
                                "page_num": page_num + 1,
                                "bbox": span["bbox"],
                                "x_indentation": span["bbox"][0],
                                "y_position": span["bbox"][1]
                            })
    doc.close()
    return text_blocks

def generate_training_data():
    """Generate synthetic training data based on common PDF patterns."""
    np.random.seed(42)
    
    # Features: [avg_size, is_bold, x_indentation, page_num]
    training_data = []
    
    # Generate Title patterns
    for _ in range(100):
        # Titles are usually: large font, bold, centered/left-aligned, early pages
        avg_size = np.random.uniform(16, 24)
        is_bold = 1
        x_indentation = np.random.uniform(0, 100)  # Can be centered or left
        page_num = np.random.choice([1, 2], p=[0.8, 0.2])
        
        training_data.append([avg_size, is_bold, x_indentation, page_num, 'Title'])
    
    # Generate H1 patterns
    for _ in range(150):
        # H1: Large font, usually bold, minimal indentation
        avg_size = np.random.uniform(14, 18)
        is_bold = np.random.choice([0, 1], p=[0.3, 0.7])
        x_indentation = np.random.uniform(0, 50)
        page_num = np.random.randint(1, 50)
        
        training_data.append([avg_size, is_bold, x_indentation, page_num, 'heading'])
    
    # Generate H2 patterns  
    for _ in range(200):
        # H2: Medium font, sometimes bold, slight indentation
        avg_size = np.random.uniform(12, 16)
        is_bold = np.random.choice([0, 1], p=[0.5, 0.5])
        x_indentation = np.random.uniform(20, 80)
        page_num = np.random.randint(1, 50)
        
        training_data.append([avg_size, is_bold, x_indentation, page_num, 'heading'])
    
    # Generate H3 patterns
    for _ in range(150):
        # H3: Smaller font, less likely bold, more indentation
        avg_size = np.random.uniform(11, 14)
        is_bold = np.random.choice([0, 1], p=[0.7, 0.3])
        x_indentation = np.random.uniform(40, 120)
        page_num = np.random.randint(1, 50)
        
        training_data.append([avg_size, is_bold, x_indentation, page_num, 'heading'])
    
    # Generate Other/Body text patterns
    for _ in range(300):
        # Body text: Small font, rarely bold, variable indentation
        avg_size = np.random.uniform(9, 12)
        is_bold = np.random.choice([0, 1], p=[0.9, 0.1])
        x_indentation = np.random.uniform(0, 150)
        page_num = np.random.randint(1, 50)
        
        training_data.append([avg_size, is_bold, x_indentation, page_num, 'other'])
    
    return np.array(training_data)

def generate_level_training_data():
    """Generate training data for heading level classification."""
    np.random.seed(42)
    
    # Features: [avg_size, is_bold, x_indentation, page_num]
    training_data = []
    
    # Generate H1 patterns
    for _ in range(200):
        avg_size = np.random.uniform(14, 18)
        is_bold = np.random.choice([0, 1], p=[0.3, 0.7])
        x_indentation = np.random.uniform(0, 50)
        page_num = np.random.randint(1, 50)
        
        training_data.append([avg_size, is_bold, x_indentation, page_num, 'H1'])
    
    # Generate H2 patterns
    for _ in range(250):
        avg_size = np.random.uniform(12, 16)
        is_bold = np.random.choice([0, 1], p=[0.5, 0.5])
        x_indentation = np.random.uniform(20, 80)
        page_num = np.random.randint(1, 50)
        
        training_data.append([avg_size, is_bold, x_indentation, page_num, 'H2'])
    
    # Generate H3 patterns
    for _ in range(200):
        avg_size = np.random.uniform(11, 14)
        is_bold = np.random.choice([0, 1], p=[0.7, 0.3])
        x_indentation = np.random.uniform(40, 120)
        page_num = np.random.randint(1, 50)
        
        training_data.append([avg_size, is_bold, x_indentation, page_num, 'H3'])
    
    return np.array(training_data)

def train_block_model():
    """Train the block classification model."""
    print("Generating block classification training data...")
    data = generate_training_data()
    
    # Prepare features and labels
    X = data[:, :4].astype(float)
    y = data[:, 4]
    
    # Encode labels
    le_block = LabelEncoder()
    y_encoded = le_block.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Create LightGBM datasets
    train_data = lgb.Dataset(X_train, label=y_train)
    valid_data = lgb.Dataset(X_test, label=y_test, reference=train_data)
    
    # Parameters for LightGBM
    params = {
        'objective': 'multiclass',
        'num_class': len(le_block.classes_),
        'metric': 'multi_logloss',
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.1,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': 0
    }
    
    # Train model
    print("Training block classification model...")
    model = lgb.train(
        params,
        train_data,
        valid_sets=[valid_data],
        num_boost_round=100,
        callbacks=[lgb.early_stopping(10), lgb.log_evaluation(0)]
    )
    
    return model, le_block

def train_level_model():
    """Train the heading level classification model."""
    print("Generating level classification training data...")
    data = generate_level_training_data()
    
    # Prepare features and labels
    X = data[:, :4].astype(float)
    y = data[:, 4]
    
    # Encode labels
    le_level = LabelEncoder()
    y_encoded = le_level.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Create LightGBM datasets
    train_data = lgb.Dataset(X_train, label=y_train)
    valid_data = lgb.Dataset(X_test, label=y_test, reference=train_data)
    
    # Parameters for LightGBM
    params = {
        'objective': 'multiclass',
        'num_class': len(le_level.classes_),
        'metric': 'multi_logloss',
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.1,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': 0
    }
    
    # Train model
    print("Training level classification model...")
    model = lgb.train(
        params,
        train_data,
        valid_sets=[valid_data],
        num_boost_round=100,
        callbacks=[lgb.early_stopping(10), lgb.log_evaluation(0)]
    )
    
    return model, le_level

def main():
    """Main training function."""
    print("Starting model training...")
    
    # Train block classification model
    block_model, le_block = train_block_model()
    
    # Train level classification model
    level_model, le_level = train_level_model()
    
    # Save models
    print("Saving models...")
    block_model.save_model('block_model.lgb')
    level_model.save_model('level_model.lgb')
    
    # Save label encoders
    joblib.dump(le_block, 'block_label_encoder.joblib')
    joblib.dump(le_level, 'level_label_encoder.joblib')
    
    print("Training completed!")
    print(f"Block classes: {le_block.classes_}")
    print(f"Level classes: {le_level.classes_}")
    print("\nModel files created:")
    print("- block_model.lgb")
    print("- level_model.lgb") 
    print("- block_label_encoder.joblib")
    print("- level_label_encoder.joblib")

if __name__ == "__main__":
    main()
