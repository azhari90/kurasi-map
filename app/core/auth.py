from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from typing import Optional, Dict, Any
import logging

from app.core.config import settings

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize Supabase client with error handling
try:
    if settings.SUPABASE_URL and settings.SUPABASE_KEY:
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    else:
        logger.warning("Supabase credentials not configured. Using mock client.")
        supabase = None
except Exception as e:
    logger.error(f"Failed to initialize Supabase client: {str(e)}")
    supabase = None

# Security scheme for JWT tokens
security = HTTPBearer(auto_error=False)

async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[Dict[str, Any]]:
    """
    Get the current authenticated user from the JWT token.
    
    Returns None if no valid token is found (unauthenticated).
    Raises HTTPException if token is invalid.
    """
    # If Supabase is not configured, return None (unauthenticated)
    if not supabase:
        return None
        
    # Check for token in cookies first (for browser sessions)
    token = request.cookies.get("access_token")
    
    # If not in cookies, check for token in Authorization header
    if not token and credentials:
        token = credentials.credentials
    
    # If no token found, return None (unauthenticated)
    if not token:
        return None
    
    try:
        # Verify the token with Supabase
        user = supabase.auth.get_user(token)
        return user.dict()["user"]
    except Exception as e:
        logger.error(f"Error verifying token: {str(e)}")
        # Invalid token
        return None

async def get_subscription_plan(user_id: str) -> str:
    """Get the user's subscription plan."""
    if not user_id or not supabase:
        return settings.FREE_PLAN_ID
    
    try:
        # Query the user's subscription from Supabase
        response = supabase.table("user_subscriptions").select("plan_id").eq("user_id", user_id).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]["plan_id"]
        else:
            # Default to free plan if no subscription found
            return settings.FREE_PLAN_ID
    except Exception as e:
        logger.error(f"Error getting subscription plan: {str(e)}")
        # On error, default to free plan
        return settings.FREE_PLAN_ID

def has_premium_access(user: Optional[Dict[str, Any]]) -> bool:
    """Check if the user has premium access."""
    if not user:
        return False
    
    # Get the user's subscription plan
    plan_id = get_subscription_plan(user["id"])
    
    # Check if the plan is premium
    return plan_id == settings.PREMIUM_PLAN_ID

def can_access_category(user: Optional[Dict[str, Any]], category: str) -> bool:
    """Check if the user can access a specific category."""
    # Premium users can access all categories
    if has_premium_access(user):
        return True
    
    # Free users can only access certain categories
    return category in settings.FREE_CATEGORIES