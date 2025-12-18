from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import sentiment, feedback, stats

app = FastAPI(title="Sentiment Analysis API", version="1.0")

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

@app.get("/")
def root():
    return {"message": "Welcome to Sentiment Analysis API!"}
