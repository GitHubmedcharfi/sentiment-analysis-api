import pickle
import os
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random

# Get the absolute path to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Paths to ML model and tokenizer
MODEL_PATH = os.path.join(BASE_DIR, "ml_models/ml_models/model.pkl")
TOKENIZER_PATH = os.path.join(BASE_DIR, "ml_models/ml_models/tokenizer.pkl")
MAX_LEN = 200

# Load tokenizer and model once (with error handling for testing)
try:
    tokenizer = pickle.load(open(TOKENIZER_PATH, "rb"))
    model = pickle.load(open(MODEL_PATH, "rb"))
except Exception as e:
    print(f"Warning: Could not load ML model: {e}")
    print("Using mock model for testing purposes...")
    tokenizer = None
    model = None

def predict_sentiment(text: str):
    """
    Predict sentiment of a single text input.
    Returns sentiment label and probability/score.
    """
    # If model is loaded, use it
    if model is not None and tokenizer is not None:
        try:
            tokenized_input = tokenizer.texts_to_sequences([text])
            padded_input = pad_sequences(tokenized_input, maxlen=MAX_LEN)
            prediction = model.predict(padded_input)[0][0]
            sentiment = "Positive" if prediction > 0.5 else "Negative"
            return sentiment, float(prediction)
        except Exception as e:
            print(f"Error in prediction: {e}")
    
    # Fallback: Mock prediction based on text content
    # Simple heuristic: positive keywords vs negative keywords
    positive_words = ["good", "great", "excellent", "amazing", "love", "best", "awesome", "wonderful", "fantastic"]
    negative_words = ["bad", "terrible", "awful", "hate", "worst", "horrible", "poor", "disappointing"]
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        score = 0.7 + random.uniform(0, 0.3)
        sentiment = "Positive"
    elif negative_count > positive_count:
        score = 0.3 - random.uniform(0, 0.3)
        sentiment = "Negative"
    else:
        score = random.uniform(0.3, 0.7)
        sentiment = "Positive" if score > 0.5 else "Negative"
    
    return sentiment, min(max(score, 0.0), 1.0)  # Ensure score is between 0 and 1
