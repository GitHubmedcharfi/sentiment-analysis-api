from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes import sentiment, feedback, stats

app = FastAPI(
    title="Sentiment Analysis API",
    version="1.0.0",
    description="""
    ## Sentiment Analysis API
    
    A comprehensive REST API for analyzing text sentiment using machine learning models.
    
    ### Features
    
    * **Sentiment Analysis**: Analyze text and predict sentiment (Positive/Negative)
    * **Feedback Management**: Store, retrieve, filter, and delete feedback entries
    * **Statistics**: Get comprehensive statistics about feedback data
    
    ### Endpoints
    
    * `/api/predict` - Analyze text sentiment
    * `/api/feedbacks/` - Manage feedback entries (CRUD operations)
    * `/api/stats/` - Get feedback statistics
    
    ### Documentation
    
    * **Swagger UI**: Available at `/docs`
    * **ReDoc**: Available at `/redoc`
    * **OpenAPI Schema**: Available at `/openapi.json`
    """,
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Include routers
app.include_router(sentiment.router, prefix="/api")
app.include_router(feedback.router, prefix="/api/feedbacks")
app.include_router(stats.router, prefix="/api/stats")

# Enable CORS for frontend apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="API Root",
    description="Welcome endpoint that provides basic information about the API",
    tags=["General"],
    responses={
        200: {
            "description": "Welcome message",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Welcome to Sentiment Analysis API!"
                    }
                }
            }
        }
    }
)
def root():
    """
    API root endpoint.
    
    Returns a welcome message and basic information about the API.
    Access the interactive documentation at `/docs` for Swagger UI or `/redoc` for ReDoc.
    """
    return {
        "message": "Welcome to Sentiment Analysis API!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }
