import pickle
import os
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Get the absolute path to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Paths to ML model and tokenizer
MODEL_PATH = os.path.join(BASE_DIR, "ml_models/ml_models/model.pkl")
TOKENIZER_PATH = os.path.join(BASE_DIR, "ml_models/ml_models/tokenizer.pkl")
MAX_LEN = 200

# Load tokenizer and model once
tokenizer = pickle.load(open(TOKENIZER_PATH, "rb"))
model = pickle.load(open(MODEL_PATH, "rb"))

def predict_sentiment(text: str):
    """
    Predict sentiment of a single text input.
    Returns sentiment label and probability/score.
    """
    tokenized_input = tokenizer.texts_to_sequences([text])
    padded_input = pad_sequences(tokenized_input, maxlen=MAX_LEN)
    prediction = model.predict(padded_input)[0][0]
    sentiment = "Positive" if prediction > 0.5 else "Negative"
    return sentiment, float(prediction)
