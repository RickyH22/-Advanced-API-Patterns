"""Middleware for request ID tracking, logging, and rate limiting"""
import time
import uuid
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.exceptions import TooManyRequestsException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add request ID to all requests"""
    
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all API requests and responses"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = getattr(request.state, "request_id", "unknown")
        
        # Log request
        logger.info(f"Request {request_id}: {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(f"Response {request_id}: {response.status_code} - {process_time:.3f}s")
        
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting using Redis"""
    
    def __init__(self, app, redis_client, limit_per_minute: int = 60):
        super().__init__(app)
        self.redis_client = redis_client
        self.limit_per_minute = limit_per_minute
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path.startswith("/health"):
            return await call_next(request)
        
        # Get client identifier (use IP or user ID if authenticated)
        client_id = request.client.host
        
        # Check authorization header for user-based rate limiting
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            client_id = f"user:{auth_header}"
        
        # Rate limit key
        key = f"rate_limit:{client_id}:{int(time.time() // 60)}"
        
        try:
            # Increment counter
            current = self.redis_client.incr(key)
            
            # Set expiry on first request
            if current == 1:
                self.redis_client.expire(key, 60)
            
            # Check limit
            if current > self.limit_per_minute:
                remaining = 0
                retry_after = 60 - (int(time.time()) % 60)
                
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": {
                            "code": "RATE_LIMIT_EXCEEDED",
                            "message": "Too many requests. Please try again later.",
                            "retry_after": retry_after
                        }
                    },
                    headers={
                        "X-RateLimit-Limit": str(self.limit_per_minute),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(time.time()) + retry_after),
                        "Retry-After": str(retry_after)
                    }
                )
            
            # Add rate limit headers
            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(self.limit_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(self.limit_per_minute - current)
            response.headers["X-RateLimit-Reset"] = str(int(time.time()) + (60 - (int(time.time()) % 60)))
            
            return response
            
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            # If Redis fails, allow the request through
            return await call_next(request)
