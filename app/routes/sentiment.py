from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.feedback import FeedbackRequest, FeedbackResponse
from app.services.ml_service import predict_sentiment
from app.services.db_service import save_feedback, get_db

router = APIRouter()

@router.post("/predict", response_model=FeedbackResponse)
def predict_feedback(feedback: FeedbackRequest, db: Session = Depends(get_db)):
    sentiment, score = predict_sentiment(feedback.text)
    # Save to DB
    save_feedback(db, feedback.text, sentiment, score)
    return {"sentiment": sentiment, "score": score}
