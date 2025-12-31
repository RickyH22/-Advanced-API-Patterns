"""Health check and async endpoints"""
from fastapi import APIRouter, BackgroundTasks
from typing import Dict
import httpx
import time
import redis
from app.config import settings
import logging

router = APIRouter(tags=["Health & Async"])
logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": str(time.time())
    }

@router.get("/health/detailed")
async def detailed_health_check() -> Dict:
    """Detailed health check with dependency status"""
    health_status = {
        "status": "healthy",
        "timestamp": str(time.time()),
        "dependencies": {}
    }
    
    # Check Redis
    try:
        r = redis.from_url(settings.REDIS_URL, decode_responses=True)
        r.ping()
        health_status["dependencies"]["redis"] = {"status": "healthy"}
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["dependencies"]["redis"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # Check database (in-memory, always healthy)
    health_status["dependencies"]["database"] = {"status": "healthy"}
    
    return health_status

@router.get("/async/external")
async def fetch_external_data() -> Dict:
    """Async endpoint that fetches data from external API"""
    async with httpx.AsyncClient() as client:
        try:
            # Fetch data from a public API
            response = await client.get("https://api.github.com/repos/fastapi/fastapi", timeout=5.0)
            data = response.json()
            
            return {
                "source": "GitHub API",
                "repository": data.get("full_name"),
                "stars": data.get("stargazers_count"),
                "description": data.get("description")
            }
        except Exception as e:
            logger.error(f"Failed to fetch external data: {e}")
            return {
                "error": "Failed to fetch external data",
                "message": str(e)
            }

def process_heavy_task(task_name: str):
    """Background task simulation"""
    logger.info(f"Starting background task: {task_name}")
    time.sleep(2)  # Simulate heavy processing
    logger.info(f"Completed background task: {task_name}")

@router.post("/async/background-task")
async def trigger_background_task(
    task_name: str,
    background_tasks: BackgroundTasks
) -> Dict:
    """Trigger a background task"""
    background_tasks.add_task(process_heavy_task, task_name)
    
    return {
        "message": "Background task triggered",
        "task_name": task_name
    }
