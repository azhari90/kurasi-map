from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Any, Optional

from app.core.auth import get_current_user, can_access_category
from app.db import client
from app.db.models import Location, LocationCreate, LocationUpdate, Category
from app.api.auth import auth_router

# Create API router
api_router = APIRouter()

# Include auth routes
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

@api_router.get("/categories", response_model=List[Dict[str, Any]])
async def get_categories(user: Optional[Dict[str, Any]] = Depends(get_current_user)):
    """Get all categories."""
    categories = await client.get_categories()
    
    # Filter out premium categories for free users
    if user is None:
        categories = [cat for cat in categories if not cat.get("premium_only", False)]
    
    return categories

@api_router.get("/locations", response_model=List[Dict[str, Any]])
async def get_locations(
    category_id: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: Optional[Dict[str, Any]] = Depends(get_current_user),
):
    """
    Get locations with optional filtering.
    
    Free users can only access non-premium locations in free categories.
    """
    # Check if the user can access the requested category
    if category_id and not can_access_category(user, category_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You need a premium subscription to access this category",
        )
    
    # Get locations
    locations = await client.get_locations(
        category_id=category_id,
        search_query=search,
        limit=limit,
        offset=offset,
    )
    
    # Filter out premium locations for free users
    if user is None:
        locations = [loc for loc in locations if not loc.get("premium_only", False)]
    
    return locations

@api_router.get("/locations/{location_id}", response_model=Dict[str, Any])
async def get_location(
    location_id: int,
    user: Optional[Dict[str, Any]] = Depends(get_current_user),
):
    """Get a specific location by ID."""
    location = await client.get_location(location_id)
    
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    
    # Check if the user can access this location
    if location.get("premium_only", False) and user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You need a premium subscription to access this location",
        )
    
    # Check if the user can access this category
    if not can_access_category(user, location["category_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You need a premium subscription to access this category",
        )
    
    return location

@api_router.post("/locations", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def create_location(
    location: LocationCreate,
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Create a new location (admin only)."""
    # Check if user is admin (in a real app, you would have proper admin checks)
    if not user or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create locations",
        )
    
    # Create the location
    new_location = await client.create_location(location.dict())
    return new_location

@api_router.put("/locations/{location_id}", response_model=Dict[str, Any])
async def update_location(
    location_id: int,
    location: LocationUpdate,
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Update an existing location (admin only)."""
    # Check if user is admin
    if not user or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update locations",
        )
    
    # Check if location exists
    existing_location = await client.get_location(location_id)
    if not existing_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    
    # Update the location
    updated_location = await client.update_location(location_id, location.dict(exclude_unset=True))
    return updated_location

@api_router.delete("/locations/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: int,
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Delete a location (admin only)."""
    # Check if user is admin
    if not user or user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete locations",
        )
    
    # Check if location exists
    existing_location = await client.get_location(location_id)
    if not existing_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    
    # Delete the location
    success = await client.delete_location(location_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete location",
        )

@api_router.get("/subscription-plans", response_model=List[Dict[str, Any]])
async def get_subscription_plans():
    """Get all subscription plans."""
    plans = await client.get_subscription_plans()
    return plans

@api_router.get("/user/subscription", response_model=Dict[str, Any])
async def get_user_subscription(user: Dict[str, Any] = Depends(get_current_user)):
    """Get the current user's subscription."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    subscription = await client.get_user_subscription(user["id"])
    if not subscription:
        return {"plan_id": "free", "name": "Free Plan"}
    
    return subscription