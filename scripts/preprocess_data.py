import os

import json

import re

import nltk

import pandas as pd

from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords


import nltk

nltk.data.path.append("/home/s.obellaneni/nltk_data")  # Ensure correct lookup path


nltk.download("punkt")

nltk.download("stopwords")



# Define paths

RAW_DATA_PATH = "../data/raw/"

PROCESSED_DATA_PATH = "../data/processed/"



# Create processed data directory

os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)



def load_data():

    """Load raw financial text data (earnings transcripts & SEC filings)."""

    raw_texts = []



    for filename in os.listdir(RAW_DATA_PATH):

        if filename.endswith(".txt") or filename.endswith(".json"):

            file_path = os.path.join(RAW_DATA_PATH, filename)

            with open(file_path, "r", encoding="utf-8") as f:

                try:

                    if filename.endswith(".json"):

                        data = json.load(f)

                        raw_texts.append(" ".join([str(value) for value in data.values()]))  # Convert JSON dict to string

                    else:

                        raw_texts.append(f.read())  # Read text file

                except Exception as e:

                    print(f"Error loading {filename}: {e}")



    return raw_texts



# Load the raw data

raw_texts = load_data()

print(f"Loaded {len(raw_texts)} documents.")

def clean_text(text):

    """Cleans text by removing special characters, numbers, and stopwords."""

    text = re.sub(r"<.*?>", "", text)  # Remove HTML tags

    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Keep only letters

    text = text.lower()  # Convert to lowercase



    words = word_tokenize(text)

    words = [word for word in words if word not in stopwords.words("english")]



    return " ".join(words)



# Apply cleaning function to all documents

cleaned_texts = [clean_text(text) for text in raw_texts]



print("Text cleaning complete.")

from transformers import AutoTokenizer



# Load tokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf", use_auth_token=True)



# Fix: Add a padding token if missing

if tokenizer.pad_token is None:

    tokenizer.pad_token = tokenizer.eos_token  # Use EOS token as padding



def tokenize_text(text):

    """Tokenizes text using Llama 2 tokenizer."""

    tokens = tokenizer(text, truncation=True, padding="max_length", max_length=512, return_tensors="pt")

    return tokens



# Tokenize all cleaned texts

tokenized_data = [tokenize_text(text) for text in cleaned_texts]



print("Tokenization complete.")

# Convert processed data into a DataFrame

df = pd.DataFrame({"cleaned_text": cleaned_texts})



# Save to CSV

df.to_csv(os.path.join(PROCESSED_DATA_PATH, "processed_data.csv"), index=False)



print("Processed data saved successfully.")


