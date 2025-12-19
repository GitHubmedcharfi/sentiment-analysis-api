from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.services.db_service import get_db
from app.models.db_models import Feedback
from app.schemas.feedback import StatsResponse

router = APIRouter(
    tags=["Statistics"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/",
    response_model=StatsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get feedback statistics",
    description="Retrieves comprehensive statistics about all feedbacks in the database, including total count, positive/negative counts, and percentages.",
    response_description="Returns feedback statistics",
    responses={
        200: {
            "description": "Statistics retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "total_feedbacks": 100,
                        "positive": 65,
                        "negative": 35,
                        "positive_percentage": 65.0,
                        "negative_percentage": 35.0
                    }
                }
            }
        }
    }
)
def feedback_stats(db: Session = Depends(get_db)):
    """
    Get comprehensive feedback statistics.
    
    Returns:
    - **total_feedbacks**: Total number of feedback entries
    - **positive**: Count of positive feedbacks
    - **negative**: Count of negative feedbacks
    - **positive_percentage**: Percentage of positive feedbacks (0-100)
    - **negative_percentage**: Percentage of negative feedbacks (0-100)
    
    Percentages are calculated based on total feedbacks. If no feedbacks exist, percentages will be 0.
    """
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
