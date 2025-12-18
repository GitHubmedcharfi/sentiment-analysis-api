from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.db_service import get_db
from app.models.db_models import Feedback

router = APIRouter()

@router.get("/")
def feedback_stats(db: Session = Depends(get_db)):
    total = db.query(Feedback).count()
    positive = db.query(Feedback).filter(Feedback.sentiment == "Positive").count()
    negative = db.query(Feedback).filter(Feedback.sentiment == "Negative").count()
    
    return {
        "total_feedbacks": total,
        "positive": positive,
        "negative": negative,
        "positive_percentage": (positive / total * 100) if total else 0,
        "negative_percentage": (negative / total * 100) if total else 0
    }
