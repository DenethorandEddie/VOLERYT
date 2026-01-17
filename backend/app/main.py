from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import search, export
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="YouTube Niche Analyzer API",
    description="""
    Analyze YouTube niches to find low-competition opportunities.

    ## Features
    * Search channels by niche keyword
    * Filter by channel age (from first upload)
    * Filter by video count
    * Tier-based scoring (S+, Great, Good, etc.)
    * Niche pool analysis
    * Competition metrics
    * Viral video detection
    * CSV/JSON export

    ## Niche Criteria
    * **Ideal**: ≤5 channels AND ≤50 videos
    * **Good**: ≤10 channels AND ≤100 videos
    * **Channel Age**: From first upload (NOT channel creation)
    * **Tiers**: S+ (≤7 days), Great (≤30 days), Good (≤60 days), etc.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(search.router)
app.include_router(export.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "YouTube Niche Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info("Starting YouTube Niche Analyzer API")
    logger.info(f"CORS origins: {settings.cors_origins_list}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info("Shutting down YouTube Niche Analyzer API")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
