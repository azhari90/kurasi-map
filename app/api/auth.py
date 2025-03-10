from fastapi import APIRouter, HTTPException, status, Response, Cookie, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import logging
import uuid

from app.core.auth import supabase
from app.core.config import settings
from app.db.client import log_login_activity

# Initialize logger
logger = logging.getLogger(__name__)

# Create auth router
auth_router = APIRouter()

# Security scheme for JWT tokens
security = HTTPBearer(auto_error=False)

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
async def login(request: LoginRequest, response: Response, req: Request):
    """Login with email and password."""
    # Get client information
    ip_address = req.client.host if req.client else None
    user_agent = req.headers.get("user-agent")
    
    logger.info(f"Login attempt for email: {request.email}")
    
    # Check if Supabase is configured
    if not supabase:
        logger.error("Supabase not configured. Cannot authenticate users.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable. Please try again later.",
        )
    
    try:
        logger.info(f"Attempting Supabase authentication for: {request.email}")
        
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
        
        # Log login activity
        await log_login_activity(
            user_id=user.id,
            email=request.email,
            ip_address=ip_address,
            user_agent=user_agent,
            login_status="success"
        )
        
        logger.info(f"Supabase login successful for: {request.email}")
        
        # Return token response
        return {
            "access_token": session.access_token,
            "token_type": "bearer",
            "expires_in": session.expires_in,
            "refresh_token": session.refresh_token,
            "user": user.model_dump(),
        }
    except Exception as e:
        logger.error(f"Login error for {request.email}: {str(e)}")
        
        # Log failed login attempt
        await log_login_activity(
            user_id="unknown",  # We don't have a user ID for failed logins
            email=request.email,
            ip_address=ip_address,
            user_agent=user_agent,
            login_status="failed"
        )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
        )

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest):
    """Create a new user account."""
    # Check if Supabase is configured
    if not supabase:
        logger.error("Supabase not configured. Cannot create user accounts.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User registration service unavailable. Please try again later.",
        )
    
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
        logger.error(f"Signup error: {str(e)}")
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
    
    # Check if Supabase is configured
    if not supabase:
        # Just clear the cookie for development
        response.delete_cookie(key="access_token")
        return {"message": "Logged out successfully"}
    
    try:
        # Sign out with Supabase
        supabase.auth.sign_out()
        
        # Clear cookie
        response.delete_cookie(key="access_token")
        
        return {"message": "Logged out successfully"}
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        # Still clear the cookie even if there's an error
        response.delete_cookie(key="access_token")
        return {"message": "Logged out successfully"}

@auth_router.post("/refresh")
async def refresh_token(refresh_token: str):
    """Refresh the access token using a refresh token."""
    # Check if Supabase is configured
    if not supabase:
        logger.warning("Supabase not configured. Using mock token refresh.")
        # Create a mock token for development
        mock_token = f"mock_token_{uuid.uuid4()}"
        mock_refresh_token = f"mock_refresh_token_{uuid.uuid4()}"
        return {
            "access_token": mock_token,
            "token_type": "bearer",
            "expires_in": 3600,
            "refresh_token": mock_refresh_token,
        }
    
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
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

@auth_router.post("/reset-password")
async def reset_password(email: str):
    """Send a password reset email."""
    # Check if Supabase is configured
    if not supabase:
        logger.warning("Supabase not configured. Mock password reset.")
        return {"message": "Password reset email sent (mock)"}
    
    try:
        # Send password reset email with Supabase
        supabase.auth.reset_password_email(email)
        
        return {"message": "Password reset email sent"}
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@auth_router.get("/user")
async def get_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Get the current user's information."""
    # Check if credentials are provided
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    # Check if Supabase is configured
    if not supabase:
        logger.warning("Supabase not configured. Using mock user data.")
        # Create a mock user for development
        return {
            "id": str(uuid.uuid4()),
            "email": "test@example.com",
            "user_metadata": {"full_name": "Test User"},
            "app_metadata": {},
            "created_at": datetime.now().isoformat(),
        }
    
    try:
        # Get user with Supabase
        user = supabase.auth.get_user(credentials.credentials)
        
        return user.user
    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )