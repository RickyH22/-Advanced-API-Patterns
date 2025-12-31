"""Dependencies for authentication and authorization"""
from fastapi import Depends, Header
from typing import Optional
from app.auth import decode_access_token
from app.database import db
from app.models import User, UserRole
from app.exceptions import UnauthorizedException, ForbiddenException

async def get_current_user(authorization: Optional[str] = Header(None)) -> User:
    """Get the current authenticated user"""
    if not authorization:
        raise UnauthorizedException("Missing authorization header")
    
    if not authorization.startswith("Bearer "):
        raise UnauthorizedException("Invalid authorization header format")
    
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    
    if not payload:
        raise UnauthorizedException("Invalid or expired token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token payload")
    
    user_data = db.get_user_by_id(int(user_id))
    if not user_data:
        raise UnauthorizedException("User not found")
    
    return User(**user_data)

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin role"""
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenException("Admin access required")
    return current_user
