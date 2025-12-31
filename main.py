"""Main FastAPI application"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import redis
import logging

from app.config import settings
from app.middleware import RequestIDMiddleware, LoggingMiddleware, RateLimitMiddleware
from app.exceptions import APIException
from app.routes import auth, tasks, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A production-ready Task Management API with authentication, rate limiting, and async capabilities"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis client for rate limiting
try:
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    redis_client.ping()
    logger.info("Connected to Redis")
except Exception as e:
    logger.warning(f"Could not connect to Redis: {e}. Rate limiting will be disabled.")
    redis_client = None

# Add custom middleware
app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)

if redis_client:
    app.add_middleware(
        RateLimitMiddleware,
        redis_client=redis_client,
        limit_per_minute=settings.RATE_LIMIT_PER_MINUTE
    )

# Global exception handler
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    """Handle custom API exceptions"""
    request_id = getattr(request.state, "request_id", "unknown")
    
    logger.error(f"Request {request_id} failed: {exc.detail}")
    
    response_content = {
        "error": {
            "code": exc.error_code,
            "message": exc.detail,
            "request_id": request_id
        }
    }
    
    headers = {}
    if hasattr(exc, "retry_after"):
        headers["Retry-After"] = str(exc.retry_after)
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_content,
        headers=headers
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    request_id = getattr(request.state, "request_id", "unknown")
    
    logger.exception(f"Request {request_id} encountered unexpected error: {exc}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "request_id": request_id
            }
        }
    )

# Include routers with versioning
api_v1 = FastAPI()
api_v1.include_router(auth.router)
api_v1.include_router(tasks.router)

app.mount(settings.API_V1_PREFIX, api_v1)

# Health check routes (no versioning)
app.include_router(health.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Task Management API",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
