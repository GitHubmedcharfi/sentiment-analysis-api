# ml_models/download_model.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment"
LOCAL_DIR = "./ml_models"

# Download tokenizer and model locally
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=LOCAL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, cache_dir=LOCAL_DIR)

print("Twitter RoBERTa model downloaded locally in:", LOCAL_DIR)
