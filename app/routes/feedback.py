from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session
from app.schemas.feedback import (
    FeedbackRequest, FeedbackResponse, FeedbackListResponse,
    FilteredFeedbackResponse, DeleteResponse
)
from app.services.ml_service import predict_sentiment
from app.services.db_service import (
    save_feedback, get_db, delete_feedback, delete_all_feedbacks,
    get_feedbacks_by_sentiment, get_all_feedbacks
)

router = APIRouter(
    tags=["Feedback Management"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/predict",
    response_model=FeedbackResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze text sentiment and save feedback",
    description="Predicts the sentiment of the input text and saves it to the database. This endpoint is similar to the sentiment analysis endpoint but is part of the feedback management module.",
    response_description="Returns the predicted sentiment and confidence score",
    responses={
        200: {
            "description": "Successful prediction and save",
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
    - Automatically saves the result to the database for later retrieval
    """
    sentiment, score = predict_sentiment(feedback.text)
    # Save to DB
    save_feedback(db, feedback.text, sentiment, score)
    return {"sentiment": sentiment, "score": score}

@router.get(
    "/",
    response_model=FeedbackListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all feedbacks",
    description="Retrieves all feedback entries from the database with their sentiment analysis results.",
    response_description="Returns a list of all feedback entries",
    responses={
        200: {
            "description": "List of all feedbacks retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "feedbacks": [
                            {
                                "id": 1,
                                "text": "I love this product!",
                                "sentiment": "Positive",
                                "score": 0.95,
                                "created_at": "2024-01-15T10:30:00"
                            }
                        ]
                    }
                }
            }
        }
    }
)
def get_all(db: Session = Depends(get_db)):
    """
    Retrieve all feedback entries from the database.
    
    Returns all feedbacks with their:
    - ID
    - Original text
    - Predicted sentiment
    - Confidence score
    - Creation timestamp
    """
    feedbacks = get_all_feedbacks(db)
    return {"feedbacks": feedbacks}

@router.get(
    "/filter/{sentiment}",
    response_model=FilteredFeedbackResponse,
    status_code=status.HTTP_200_OK,
    summary="Filter feedbacks by sentiment",
    description="Retrieves all feedback entries that match the specified sentiment (positive or negative).",
    response_description="Returns filtered feedbacks with count",
    responses={
        200: {
            "description": "Filtered feedbacks retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "sentiment": "positive",
                        "count": 5,
                        "feedbacks": [
                            {
                                "id": 1,
                                "text": "I love this product!",
                                "sentiment": "Positive",
                                "score": 0.95,
                                "created_at": "2024-01-15T10:30:00"
                            }
                        ]
                    }
                }
            }
        },
        400: {
            "description": "Invalid sentiment value",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Sentiment must be 'positive' or 'negative'"
                    }
                }
            }
        }
    }
)
def filter_by_sentiment(
    sentiment: str = Path(
        ...,
        description="Sentiment to filter by (must be 'positive' or 'negative')",
        example="positive"
    ),
    db: Session = Depends(get_db)
):
    """
    Filter feedbacks by sentiment type.
    
    - **sentiment**: Must be either 'positive' or 'negative' (case-insensitive)
    - Returns all feedbacks matching the specified sentiment along with the count
    """
    if sentiment.lower() not in ["positive", "negative"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sentiment must be 'positive' or 'negative'"
        )
    feedbacks = get_feedbacks_by_sentiment(db, sentiment.capitalize())
    return {"sentiment": sentiment, "count": len(feedbacks), "feedbacks": feedbacks}

@router.delete(
    "/{feedback_id}",
    response_model=DeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a single feedback",
    description="Deletes a specific feedback entry by its ID from the database.",
    response_description="Returns a success message",
    responses={
        200: {
            "description": "Feedback deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Feedback 1 deleted successfully"
                    }
                }
            }
        },
        404: {
            "description": "Feedback not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Feedback not found"
                    }
                }
            }
        }
    }
)
def delete_single(
    feedback_id: int = Path(..., description="ID of the feedback to delete", example=1, gt=0),
    db: Session = Depends(get_db)
):
    """
    Delete a specific feedback entry.
    
    - **feedback_id**: The unique identifier of the feedback to delete
    - Returns success message if deletion is successful
    - Returns 404 if feedback ID doesn't exist
    """
    success = delete_feedback(db, feedback_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    return {"message": f"Feedback {feedback_id} deleted successfully"}

@router.delete(
    "/",
    response_model=DeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete all feedbacks",
    description="Deletes all feedback entries from the database. This operation cannot be undone.",
    response_description="Returns a success message",
    responses={
        200: {
            "description": "All feedbacks deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "All feedbacks deleted successfully"
                    }
                }
            }
        }
    }
)
def delete_all(db: Session = Depends(get_db)):
    """
    Delete all feedback entries from the database.
    
    **Warning**: This operation permanently removes all feedback data.
    Use with caution as this action cannot be undone.
    """
    delete_all_feedbacks(db)
    return {"message": "All feedbacks deleted successfully"}
