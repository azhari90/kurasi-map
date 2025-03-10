from fastapi import APIRouter, HTTPException, status, Response, Cookie, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from app.core.auth import supabase
from app.core.config import settings

# Create auth router
auth_router = APIRouter()

# Security scheme for JWT tokens
security = HTTPBearer()

# Models
class LoginRequest(BaseModel):
    email: str
    password: str
    remember: bool = False

class SignupRequest(BaseModel):
    email: str
    password: str
    user_metadata: Optional[Dict[str, Any]] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    user: Dict[str, Any]

@auth_router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, response: Response):
    """Login with email and password."""
    try:
        # Authenticate with Supabase
        auth_response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password,
        })
        
        # Get token data
        session = auth_response.session
        user = auth_response.user
        
        # Set cookie if remember is True
        if request.remember:
            expires = datetime.now() + timedelta(days=30)
            response.set_cookie(
                key="access_token",
                value=session.access_token,
                httponly=True,
                expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                secure=not settings.DEBUG,  # Secure in production
                samesite="lax",
            )
        
        # Return token response
        return {
            "access_token": session.access_token,
            "token_type": "bearer",
            "expires_in": session.expires_in,
            "refresh_token": session.refresh_token,
            "user": user.model_dump(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest):
    """Create a new user account."""
    try:
        # Create user with Supabase
        auth_response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": request.user_metadata or {},
            }
        })
        
        return {
            "message": "User created successfully. Please check your email for verification.",
            "user_id": auth_response.user.id,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@auth_router.post("/logout")
async def logout(
    response: Response,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    access_token: Optional[str] = Cookie(None),
):
    """Logout and invalidate the session."""
    token = access_token or (credentials.credentials if credentials else None)
    
    if not token:
        return {"message": "No active session"}
    
    try:
        # Sign out with Supabase
        supabase.auth.sign_out()
        
        # Clear cookie
        response.delete_cookie(key="access_token")
        
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@auth_router.post("/refresh")
async def refresh_token(refresh_token: str):
    """Refresh the access token using a refresh token."""
    try:
        # Refresh token with Supabase
        auth_response = supabase.auth.refresh_session(refresh_token)
        
        # Get new session
        session = auth_response.session
        
        return {
            "access_token": session.access_token,
            "token_type": "bearer",
            "expires_in": session.expires_in,
            "refresh_token": session.refresh_token,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

@auth_router.post("/reset-password")
async def reset_password(email: str):
    """Send a password reset email."""
    try:
        # Send password reset email with Supabase
        supabase.auth.reset_password_email(email)
        
        return {"message": "Password reset email sent"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@auth_router.get("/user")
async def get_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get the current user's information."""
    try:
        # Get user with Supabase
        user = supabase.auth.get_user(credentials.credentials)
        
        return user.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )