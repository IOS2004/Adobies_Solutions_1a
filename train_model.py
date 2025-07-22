import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

def train_model():
    # Load the dataset
    df = pd.read_csv("training_data.csv")

    # Preprocessing
    df = df.dropna()
    
    # Block Classifier Model
    df['block_label'] = df['label'].apply(lambda x: 'heading' if x in ['H1', 'H2', 'H3', 'H4'] else x)
    le_block = LabelEncoder()
    df['block_label_encoded'] = le_block.fit_transform(df['block_label'])
    
    features = ['avg_size', 'is_bold', 'x_indentation', 'page_num']
    target_block = 'block_label_encoded'

    X = df[features]
    y_block = df[target_block]

    X_train, X_test, y_block_train, y_block_test = train_test_split(X, y_block, test_size=0.2, random_state=42, stratify=y_block)

    model_block = lgb.LGBMClassifier(random_state=42)
    model_block.fit(X_train, y_block_train)

    y_block_pred = model_block.predict(X_test)
    print("--- Block Classifier Report ---")
    print(classification_report(y_block_test, y_block_pred, target_names=le_block.classes_, labels=range(len(le_block.classes_))))

    model_block.booster_.save_model('block_model.lgb')
    print("Block model saved successfully: block_model.lgb")

    # Heading Level Classifier Model
    df_headings = df[df['block_label'] == 'heading'].copy()
    le_level = LabelEncoder()
    df_headings['level_label_encoded'] = le_level.fit_transform(df_headings['label'])
    
    target_level = 'level_label_encoded'
    X_headings = df_headings[features]
    y_level = df_headings[target_level]

    X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(X_headings, y_level, test_size=0.2, random_state=42, stratify=y_level)

    model_level = lgb.LGBMClassifier(random_state=42)
    model_level.fit(X_train_h, y_train_h)

    y_level_pred = model_level.predict(X_test_h)
    print("\n--- Heading Level Classifier Report ---")
    print(classification_report(y_test_h, y_level_pred, target_names=le_level.classes_, labels=range(len(le_level.classes_))))

    model_level.booster_.save_model('level_model.lgb')
    print("Level model saved successfully: level_model.lgb")

if __name__ == "__main__":
    train_model()
