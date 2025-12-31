"""Authentication routes"""
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from app.models import UserCreate, UserLogin, Token, User
from app.database import db
from app.auth import hash_password, verify_password, create_access_token
from app.exceptions import BadRequestException, UnauthorizedException
import logging

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)

def send_welcome_email(email: str, username: str):
    """Background task to send welcome email (simulated)"""
    logger.info(f"Sending welcome email to {email} for user {username}")
    # In production, this would send an actual email

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, background_tasks: BackgroundTasks):
    """Register a new user"""
    # Check if username exists
    if db.username_exists(user_data.username):
        raise BadRequestException("Username already exists")
    
    # Check if email exists
    if db.email_exists(user_data.email):
        raise BadRequestException("Email already exists")
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    
    # Create user
    user = db.create_user(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )
    
    # Send welcome email in background
    background_tasks.add_task(send_welcome_email, user_data.email, user_data.username)
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user["id"])})
    
    user_model = User(**user)
    
    return Token(access_token=access_token, user=user_model)

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login and get access token"""
    # Get user by username
    user = db.get_user_by_username(credentials.username)
    
    if not user:
        raise UnauthorizedException("Invalid username or password")
    
    # Verify password
    if not verify_password(credentials.password, user["hashed_password"]):
        raise UnauthorizedException("Invalid username or password")
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user["id"])})
    
    user_model = User(**user)
    
    return Token(access_token=access_token, user=user_model)
