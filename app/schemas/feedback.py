from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List

class FeedbackRequest(BaseModel):
    """Request model for sentiment analysis"""
    text: str = Field(..., description="The text to analyze for sentiment", example="I love this product! It's amazing.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "I love this product! It's amazing."
            }
        }
    )

class FeedbackResponse(BaseModel):
    """Response model for sentiment prediction"""
    sentiment: str = Field(..., description="Predicted sentiment: 'Positive' or 'Negative'", example="Positive")
    score: float = Field(..., description="Confidence score between 0 and 1", example=0.95, ge=0, le=1)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "sentiment": "Positive",
                "score": 0.95
            }
        }
    )

class FeedbackDB(BaseModel):
    """Database model for feedback with all fields"""
    id: int = Field(..., description="Unique identifier for the feedback", example=1)
    text: str = Field(..., description="The analyzed text", example="I love this product!")
    sentiment: str = Field(..., description="Predicted sentiment", example="Positive")
    score: float = Field(..., description="Confidence score", example=0.95)
    created_at: datetime = Field(..., description="Timestamp when the feedback was created", example="2024-01-15T10:30:00")

    model_config = ConfigDict(from_attributes=True)

class FeedbackListResponse(BaseModel):
    """Response model for list of feedbacks"""
    feedbacks: List[FeedbackDB] = Field(..., description="List of all feedback entries")

    model_config = ConfigDict(
        json_schema_extra={
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
    )

class FilteredFeedbackResponse(BaseModel):
    """Response model for filtered feedbacks by sentiment"""
    sentiment: str = Field(..., description="The sentiment filter applied", example="positive")
    count: int = Field(..., description="Number of feedbacks matching the sentiment", example=5)
    feedbacks: List[FeedbackDB] = Field(..., description="List of feedbacks matching the sentiment")

    model_config = ConfigDict(
        json_schema_extra={
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
    )

class DeleteResponse(BaseModel):
    """Response model for delete operations"""
    message: str = Field(..., description="Success message", example="Feedback 1 deleted successfully")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Feedback 1 deleted successfully"
            }
        }
    )

class StatsResponse(BaseModel):
    """Response model for feedback statistics"""
    total_feedbacks: int = Field(..., description="Total number of feedbacks in the database", example=100)
    positive: int = Field(..., description="Number of positive feedbacks", example=65)
    negative: int = Field(..., description="Number of negative feedbacks", example=35)
    positive_percentage: float = Field(..., description="Percentage of positive feedbacks", example=65.0)
    negative_percentage: float = Field(..., description="Percentage of negative feedbacks", example=35.0)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_feedbacks": 100,
                "positive": 65,
                "negative": 35,
                "positive_percentage": 65.0,
                "negative_percentage": 35.0
            }
        }
    )
