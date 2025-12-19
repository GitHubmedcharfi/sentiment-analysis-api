from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.feedback import FeedbackRequest, FeedbackResponse
from app.services.ml_service import predict_sentiment
from app.services.db_service import save_feedback, get_db

router = APIRouter(
    tags=["Sentiment Analysis"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/predict",
    response_model=FeedbackResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze text sentiment",
    description="Predicts the sentiment (Positive or Negative) of the input text using a machine learning model. The result is automatically saved to the database.",
    response_description="Returns the predicted sentiment and confidence score",
    responses={
        200: {
            "description": "Successful prediction",
            "content": {
                "application/json": {
                    "example": {
                        "sentiment": "Positive",
                        "score": 0.95
                    }
                }
            }
        }
    }
)
def predict_feedback(feedback: FeedbackRequest, db: Session = Depends(get_db)):
    """
    Analyze text sentiment and save to database.
    
    - **text**: The text to analyze for sentiment
    - Returns sentiment prediction (Positive/Negative) and confidence score (0-1)
    - Automatically saves the result to the database
    """
    sentiment, score = predict_sentiment(feedback.text)
    # Save to DB
    save_feedback(db, feedback.text, sentiment, score)
    return {"sentiment": sentiment, "score": score}
