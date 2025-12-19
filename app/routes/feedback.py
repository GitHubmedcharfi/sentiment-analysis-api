from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.feedback import FeedbackRequest, FeedbackResponse
from app.services.ml_service import predict_sentiment
from app.services.db_service import (
    save_feedback, get_db, delete_feedback, delete_all_feedbacks,
    get_feedbacks_by_sentiment, get_all_feedbacks
)

router = APIRouter()

@router.post("/predict", response_model=FeedbackResponse)
def predict_feedback(feedback: FeedbackRequest, db: Session = Depends(get_db)):
    sentiment, score = predict_sentiment(feedback.text)
    # Save to DB
    save_feedback(db, feedback.text, sentiment, score)
    return {"sentiment": sentiment, "score": score}

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    feedbacks = get_all_feedbacks(db)
    return {"feedbacks": feedbacks}

@router.get("/filter/{sentiment}")
def filter_by_sentiment(sentiment: str, db: Session = Depends(get_db)):
    if sentiment.lower() not in ["positive", "negative"]:
        raise HTTPException(status_code=400, detail="Sentiment must be 'positive' or 'negative'")
    feedbacks = get_feedbacks_by_sentiment(db, sentiment.capitalize())
    return {"sentiment": sentiment, "count": len(feedbacks), "feedbacks": feedbacks}

@router.delete("/{feedback_id}")
def delete_single(feedback_id: int, db: Session = Depends(get_db)):
    success = delete_feedback(db, feedback_id)
    if not success:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"message": f"Feedback {feedback_id} deleted successfully"}

@router.delete("/")
def delete_all(db: Session = Depends(get_db)):
    delete_all_feedbacks(db)
    return {"message": "All feedbacks deleted successfully"}
