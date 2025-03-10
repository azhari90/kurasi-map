from supabase import create_client, Client
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
import json
import os

from app.core.config import settings
from app.db.models import Location, Category, SubscriptionPlan, UserSubscription

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize Supabase client with error handling
try:
    if settings.SUPABASE_URL and settings.SUPABASE_KEY:
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    else:
        logger.warning("Supabase credentials not configured. Using mock data.")
        supabase = None
except Exception as e:
    logger.error(f"Failed to initialize Supabase client: {str(e)}")
    supabase = None

# Sample data for development when Supabase is not configured
SAMPLE_CATEGORIES = [
    {"id": "restaurants", "name": "Restaurants", "description": "Places to eat", "icon": "utensils", "premium_only": False},
    {"id": "cafes", "name": "Cafes", "description": "Coffee shops and cafes", "icon": "coffee", "premium_only": False},
    {"id": "sports", "name": "Sports Venues", "description": "Sports and fitness locations", "icon": "volleyball-ball", "premium_only": True},
    {"id": "hospitals", "name": "Hospitals", "description": "Medical facilities", "icon": "hospital", "premium_only": True},
    {"id": "shopping", "name": "Shopping", "description": "Retail stores and malls", "icon": "shopping-bag", "premium_only": True}
]

SAMPLE_LOCATIONS = [
    {
        "id": 1,
        "name": "Warung Tekko",
        "description": "A cozy Indonesian restaurant with authentic flavors.",
        "category_id": "restaurants",
        "latitude": -6.2088,
        "longitude": 106.8456,
        "address": "Jl. Senopati No. 42, Jakarta Selatan",
        "operating_hours": {"Monday": "11:00 - 22:00", "Tuesday": "11:00 - 22:00", "Wednesday": "11:00 - 22:00", "Thursday": "11:00 - 22:00", "Friday": "11:00 - 23:00", "Saturday": "11:00 - 23:00", "Sunday": "11:00 - 22:00"},
        "instagram": "warungtekko",
        "phone": "+62212751234",
        "website": "https://warungtekko.com",
        "typical_spending": "Rp 100,000 - Rp 200,000 per person",
        "images": ["https://example.com/images/warung-tekko-1.jpg", "https://example.com/images/warung-tekko-2.jpg"],
        "premium_only": False,
        "created_at": "2025-03-10T00:00:00Z",
        "updated_at": "2025-03-10T00:00:00Z"
    },
    {
        "id": 2,
        "name": "Sushi Tei",
        "description": "Japanese restaurant with a wide variety of sushi and sashimi.",
        "category_id": "restaurants",
        "latitude": -6.2100,
        "longitude": 106.8470,
        "address": "Pacific Place Mall, Jl. Jend. Sudirman, Jakarta Selatan",
        "operating_hours": {"Monday": "10:00 - 22:00", "Tuesday": "10:00 - 22:00", "Wednesday": "10:00 - 22:00", "Thursday": "10:00 - 22:00", "Friday": "10:00 - 23:00", "Saturday": "10:00 - 23:00", "Sunday": "10:00 - 22:00"},
        "instagram": "sushitei_id",
        "phone": "+62215701234",
        "website": "https://sushitei.co.id",
        "typical_spending": "Rp 150,000 - Rp 300,000 per person",
        "images": ["https://example.com/images/sushi-tei-1.jpg", "https://example.com/images/sushi-tei-2.jpg"],
        "premium_only": False,
        "created_at": "2025-03-10T00:00:00Z",
        "updated_at": "2025-03-10T00:00:00Z"
    },
    {
        "id": 3,
        "name": "Djournal Coffee",
        "description": "Specialty coffee shop with cozy atmosphere.",
        "category_id": "cafes",
        "latitude": -6.2095,
        "longitude": 106.8230,
        "address": "Jl. Wijaya No. 45, Jakarta Selatan",
        "operating_hours": {"Monday": "07:00 - 22:00", "Tuesday": "07:00 - 22:00", "Wednesday": "07:00 - 22:00", "Thursday": "07:00 - 22:00", "Friday": "07:00 - 23:00", "Saturday": "08:00 - 23:00", "Sunday": "08:00 - 22:00"},
        "instagram": "djournalcoffee",
        "phone": "+62217231234",
        "website": "https://djournalcoffee.com",
        "typical_spending": "Rp 50,000 - Rp 100,000 per person",
        "images": ["https://example.com/images/djournal-1.jpg", "https://example.com/images/djournal-2.jpg"],
        "premium_only": False,
        "created_at": "2025-03-10T00:00:00Z",
        "updated_at": "2025-03-10T00:00:00Z"
    }
]

SAMPLE_SUBSCRIPTION_PLANS = [
    {"id": "free", "name": "Free Plan", "description": "Basic access to the map", "price": 0.00, "features": ["Access to basic categories", "Limited location details"]},
    {"id": "premium", "name": "Premium Plan", "description": "Full access to all features", "price": 9.99, "features": ["Access to all categories", "All location details", "No advertisements", "Offline maps"]}
]

async def get_categories() -> List[Dict[str, Any]]:
    """Get all location categories."""
    if not supabase:
        return SAMPLE_CATEGORIES
    
    try:
        response = supabase.table("categories").select("*").execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}")
        return SAMPLE_CATEGORIES

async def get_category(category_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific category by ID."""
    if not supabase:
        return next((cat for cat in SAMPLE_CATEGORIES if cat["id"] == category_id), None)
    
    try:
        response = supabase.table("categories").select("*").eq("id", category_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        logger.error(f"Error getting category: {str(e)}")
        return next((cat for cat in SAMPLE_CATEGORIES if cat["id"] == category_id), None)

async def get_locations(
    category_id: Optional[str] = None,
    premium_only: Optional[bool] = None,
    search_query: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    """
    Get locations with optional filtering.
    
    Args:
        category_id: Filter by category ID
        premium_only: Filter by premium status
        search_query: Search in name and description
        limit: Maximum number of results
        offset: Pagination offset
    """
    if not supabase:
        # Filter sample data
        filtered_locations = SAMPLE_LOCATIONS
        
        if category_id:
            filtered_locations = [loc for loc in filtered_locations if loc["category_id"] == category_id]
        
        if premium_only is not None:
            filtered_locations = [loc for loc in filtered_locations if loc["premium_only"] == premium_only]
        
        if search_query:
            search_query = search_query.lower()
            filtered_locations = [
                loc for loc in filtered_locations 
                if search_query in loc["name"].lower() or 
                   (loc["description"] and search_query in loc["description"].lower())
            ]
        
        # Apply pagination
        return filtered_locations[offset:offset + limit]
    
    try:
        query = supabase.table("locations").select("*")
        
        # Apply filters
        if category_id:
            query = query.eq("category_id", category_id)
        
        if premium_only is not None:
            query = query.eq("premium_only", premium_only)
        
        if search_query:
            query = query.or_(f"name.ilike.%{search_query}%,description.ilike.%{search_query}%")
        
        # Apply pagination
        query = query.range(offset, offset + limit - 1)
        
        # Execute query
        response = query.execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting locations: {str(e)}")
        return SAMPLE_LOCATIONS

async def get_location(location_id: int) -> Optional[Dict[str, Any]]:
    """Get a specific location by ID."""
    if not supabase:
        return next((loc for loc in SAMPLE_LOCATIONS if loc["id"] == location_id), None)
    
    try:
        response = supabase.table("locations").select("*").eq("id", location_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        logger.error(f"Error getting location: {str(e)}")
        return next((loc for loc in SAMPLE_LOCATIONS if loc["id"] == location_id), None)

async def create_location(location_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new location."""
    if not supabase:
        logger.warning("Cannot create location: Supabase not configured")
        return {}
    
    try:
        # Add timestamps
        location_data["created_at"] = datetime.now().isoformat()
        location_data["updated_at"] = location_data["created_at"]
        
        response = supabase.table("locations").insert(location_data).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return {}
    except Exception as e:
        logger.error(f"Error creating location: {str(e)}")
        return {}

async def update_location(location_id: int, location_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing location."""
    if not supabase:
        logger.warning("Cannot update location: Supabase not configured")
        return {}
    
    try:
        # Update timestamp
        location_data["updated_at"] = datetime.now().isoformat()
        
        response = supabase.table("locations").update(location_data).eq("id", location_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return {}
    except Exception as e:
        logger.error(f"Error updating location: {str(e)}")
        return {}

async def delete_location(location_id: int) -> bool:
    """Delete a location."""
    if not supabase:
        logger.warning("Cannot delete location: Supabase not configured")
        return False
    
    try:
        response = supabase.table("locations").delete().eq("id", location_id).execute()
        return len(response.data) > 0
    except Exception as e:
        logger.error(f"Error deleting location: {str(e)}")
        return False

async def get_subscription_plans() -> List[Dict[str, Any]]:
    """Get all subscription plans."""
    if not supabase:
        return SAMPLE_SUBSCRIPTION_PLANS
    
    try:
        response = supabase.table("subscription_plans").select("*").execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting subscription plans: {str(e)}")
        return SAMPLE_SUBSCRIPTION_PLANS

async def get_user_subscription(user_id: str) -> Optional[Dict[str, Any]]:
    """Get a user's subscription."""
    if not supabase:
        # Return free plan for development
        return {"plan_id": "free", "name": "Free Plan"}
    
    try:
        response = supabase.table("user_subscriptions").select("*, subscription_plans(*)").eq("user_id", user_id).eq("is_active", True).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        logger.error(f"Error getting user subscription: {str(e)}")
        return {"plan_id": "free", "name": "Free Plan"}

async def log_login_activity(
    user_id: str,
    email: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    device_info: Optional[str] = None,
    login_status: str = "success",
    location: Optional[str] = None
) -> Dict[str, Any]:
    """
    Log a user login activity.
    
    Args:
        user_id: The user's ID
        email: The user's email
        ip_address: The user's IP address
        user_agent: The user's browser/device user agent
        device_info: Additional device information
        login_status: "success" or "failed"
        location: Approximate location based on IP
        
    Returns:
        The created login activity record
    """
    # Create login activity data
    login_data = {
        "id": 0,
        "user_id": user_id,
        "email": email,
        "ip_address": ip_address,
        "user_agent": user_agent,
        "device_info": device_info,
        "login_status": login_status,
        "login_time": datetime.now().isoformat(),
        "location": location
    }
    
    if not supabase:
        logger.warning("Cannot log login activity: Supabase not configured")
        return login_data
    
    try:
        # Always try to insert login activity
        logger.info(f"Logging login activity for {email} ({login_status})")
        
        # In development mode, just log locally and return
        if settings.DEBUG:
            logger.info(f"DEBUG mode: Login activity logged locally for {email} ({login_status})")
            return login_data
        
        # Try with regular client in production
        try:
            response = supabase.table("login_activities").insert(login_data).execute()
            
            if response.data and len(response.data) > 0:
                logger.info(f"Login activity recorded with ID: {response.data[0].get('id')}")
                return response.data[0]
        except Exception as insert_error:
            logger.error(f"Error inserting login activity: {str(insert_error)}")
            # Continue with local logging
        
        # If insert fails or returns no data, just log and return the data
        logger.info(f"Login activity: {login_data['email']} ({login_data['login_status']})")
        return login_data
    except Exception as e:
        # Check if it's an RLS error
        if "violates row-level security policy" in str(e):
            logger.warning(f"RLS policy prevented login activity logging. This is expected if you haven't set up the proper policies.")
            # Still log the activity locally
            logger.info(f"Login activity (local only): {login_data['email']} ({login_data['login_status']})")
        else:
            logger.error(f"Error logging login activity: {str(e)}")
        
        return login_data

async def get_login_activities(
    user_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Get login activities with optional filtering by user.
    
    Args:
        user_id: Filter by user ID (optional)
        limit: Maximum number of results
        offset: Pagination offset
        
    Returns:
        List of login activities
    """
    if not supabase or settings.DEBUG:
        logger.info("Using mock login activities in development mode")
        # Return mock data for development
        return [
            {
                "id": 1,
                "user_id": "1",
                "email": "user1@example.com",
                "ip_address": "192.168.1.1",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "login_status": "success",
                "login_time": (datetime.now() - timedelta(hours=1)).isoformat(),
            },
            {
                "id": 2,
                "user_id": "2",
                "email": "user2@example.com",
                "ip_address": "192.168.1.2",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
                "login_status": "success",
                "login_time": (datetime.now() - timedelta(hours=2)).isoformat(),
            },
            {
                "id": 3,
                "user_id": "unknown",
                "email": "invalid@example.com",
                "ip_address": "192.168.1.3",
                "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
                "login_status": "failed",
                "login_time": (datetime.now() - timedelta(hours=3)).isoformat(),
            }
        ]
    
    try:
        query = supabase.table("login_activities").select("*")
        
        # Filter by user_id if provided
        if user_id:
            query = query.eq("user_id", user_id)
        
        # Order by login_time descending (most recent first)
        query = query.order("login_time", desc=True)
        
        # Apply pagination
        query = query.range(offset, offset + limit - 1)
        
        # Execute query
        response = query.execute()
        return response.data
    except Exception as e:
        logger.error(f"Error getting login activities: {str(e)}")
        # Return empty list on error
        return []