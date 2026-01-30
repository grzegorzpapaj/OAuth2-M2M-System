"""
User authentication routes
"""
from fastapi import APIRouter, HTTPException, Cookie, Response
from pydantic import BaseModel
from typing import Optional
from .database import db

router = APIRouter(tags=["User Authentication"])


class LoginRequest(BaseModel):
    """User login request"""
    username: str
    password: str


class RegisterUserRequest(BaseModel):
    """User registration request (admin only)"""
    username: str
    password: str
    email: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None


class UserResponse(BaseModel):
    """User data response"""
    id: int
    username: str
    email: Optional[str]
    is_admin: bool


@router.post("/auth/login")
async def login(request: LoginRequest, response: Response):
    """
    User login - returns session token
    """
    # Verify credentials
    user = db.verify_user(request.username, request.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Create session
    session_token = db.create_session(user["id"])
    
    # Set HTTP-only cookie
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=86400,  # 24 hours
        samesite="lax"
    )
    
    return {
        "status": "success",
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "is_admin": user["is_admin"]
        },
        "session_token": session_token,
        "client_credentials": {
            "client_id": user["client_id"],
            "client_secret": user["client_secret"]
        } if user["client_id"] and user["client_secret"] else None
    }


@router.post("/auth/logout")
async def logout(response: Response, session_token: Optional[str] = Cookie(None)):
    """
    User logout - destroys session
    """
    if session_token:
        db.delete_session(session_token)
    
    # Clear cookie
    response.delete_cookie("session_token")
    
    return {
        "status": "success",
        "message": "Logged out successfully"
    }


@router.get("/auth/me")
async def get_current_user(session_token: Optional[str] = Cookie(None)):
    """
    Get current logged-in user
    """
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user = db.verify_session(session_token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    return {
        "user": {
            "id": user["user_id"],
            "username": user["username"],
            "email": user["email"],
            "is_admin": user["is_admin"]
        },
        "client_credentials": {
            "client_id": user["client_id"],
            "client_secret": user["client_secret"]
        } if user["client_id"] and user["client_secret"] else None
    }


@router.post("/auth/register-user")
async def register_user(request: RegisterUserRequest, session_token: Optional[str] = Cookie(None)):
    """
    Register a new user (admin only for now, later can be protected)
    """
    # For now, allow anyone to register the first user
    # Later you can add admin-only check
    
    try:
        user = db.create_user(
            username=request.username,
            password=request.password,
            email=request.email,
            client_id=request.client_id,
            client_secret=request.client_secret
        )
        
        return {
            "status": "success",
            "message": "User created successfully",
            "user": user
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
