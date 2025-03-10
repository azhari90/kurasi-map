from supabase import create_client, Client
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.core.config import settings
from app.db.models import Location, Category, SubscriptionPlan, UserSubscription

# Initialize Supabase client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

async def get_categories() -> List[Dict[str, Any]]:
    """Get all location categories."""
    response = supabase.table("categories").select("*").execute()
    return response.data

async def get_category(category_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific category by ID."""
    response = supabase.table("categories").select("*").eq("id", category_id).execute()
    if response.data and len(response.data) > 0:
        return response.data[0]
    return None

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

async def get_location(location_id: int) -> Optional[Dict[str, Any]]:
    """Get a specific location by ID."""
    response = supabase.table("locations").select("*").eq("id", location_id).execute()
    if response.data and len(response.data) > 0:
        return response.data[0]
    return None

async def create_location(location_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new location."""
    # Add timestamps
    location_data["created_at"] = datetime.now().isoformat()
    location_data["updated_at"] = location_data["created_at"]
    
    response = supabase.table("locations").insert(location_data).execute()
    if response.data and len(response.data) > 0:
        return response.data[0]
    return {}

async def update_location(location_id: int, location_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing location."""
    # Update timestamp
    location_data["updated_at"] = datetime.now().isoformat()
    
    response = supabase.table("locations").update(location_data).eq("id", location_id).execute()
    if response.data and len(response.data) > 0:
        return response.data[0]
    return {}

async def delete_location(location_id: int) -> bool:
    """Delete a location."""
    response = supabase.table("locations").delete().eq("id", location_id).execute()
    return len(response.data) > 0

async def get_subscription_plans() -> List[Dict[str, Any]]:
    """Get all subscription plans."""
    response = supabase.table("subscription_plans").select("*").execute()
    return response.data

async def get_user_subscription(user_id: str) -> Optional[Dict[str, Any]]:
    """Get a user's subscription."""
    response = supabase.table("user_subscriptions").select("*, subscription_plans(*)").eq("user_id", user_id).eq("is_active", True).execute()
    if response.data and len(response.data) > 0:
        return response.data[0]
    return None