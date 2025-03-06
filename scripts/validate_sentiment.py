import torch

import json

import pandas as pd

from transformers import BertTokenizer, BertForSequenceClassification, pipeline



# Load preprocessed dataset

DATA_PATH = "../data/processed/processed_data.csv"

OUTPUT_JSON_PATH = "../data/processed/validated_train.json"

OUTPUT_CSV_PATH = "../data/processed/validated_train.csv"



# Load CSV properly as a DataFrame

df = pd.read_csv(DATA_PATH)



# Update expected column to match actual dataset

expected_col = "cleaned_text"  # Since "text" is missing

if expected_col not in df.columns:

    raise ValueError(f"❌ ERROR: Expected column '{expected_col}' not found! Available: {df.columns.tolist()}")



# Load FinBERT model

model_name = "ProsusAI/finbert"

tokenizer = BertTokenizer.from_pretrained(model_name)

model = BertForSequenceClassification.from_pretrained(model_name)

sentiment_pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer)



# Function to analyze sentiment

def analyze_sentiment(text):

    if isinstance(text, str):  # Ensure valid text

        result = sentiment_pipeline(text[:512])  # Limit to 512 tokens

        return result[0]["label"]

    return "Neutral"  # Default if text is missing



# Apply sentiment analysis

df["predicted_sentiment"] = df[expected_col].apply(analyze_sentiment)



# Save validated dataset as JSON & CSV

df.to_json(OUTPUT_JSON_PATH, orient="records", indent=4)

df.to_csv(OUTPUT_CSV_PATH, index=False)



print(f"✅ Sentiment validation complete.")

print(f"📂 JSON saved to: {OUTPUT_JSON_PATH}")

print(f"📂 CSV saved to: {OUTPUT_CSV_PATH}")


