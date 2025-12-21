from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
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

# Mount static files directory for CSS, JS, and other assets
frontend_path = Path(__file__).parent.parent / "frontend"
assets_path = frontend_path / "assets"

if assets_path.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")

# Enable CORS for frontend apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def serve_frontend():
    """Serve the frontend HTML file"""
    frontend_file = frontend_path / "index.html"
    if frontend_file.exists():
        return FileResponse(str(frontend_file))
    return {
        "message": "Welcome to Sentiment Analysis API!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get(
    "/api",
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
def api_root():
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
