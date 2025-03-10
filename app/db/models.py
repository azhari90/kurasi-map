from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class Category(BaseModel):
    """Location category model."""
    id: str
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    premium_only: bool = False

class Location(BaseModel):
    """Location model."""
    id: int
    name: str
    description: Optional[str] = None
    category_id: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    operating_hours: Optional[Dict[str, str]] = None
    instagram: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    typical_spending: Optional[str] = None
    images: Optional[List[str]] = None
    premium_only: bool = False
    created_at: datetime
    updated_at: datetime

class LocationCreate(BaseModel):
    """Model for creating a new location."""
    name: str
    description: Optional[str] = None
    category_id: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    operating_hours: Optional[Dict[str, str]] = None
    instagram: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    typical_spending: Optional[str] = None
    images: Optional[List[str]] = None
    premium_only: bool = False

class LocationUpdate(BaseModel):
    """Model for updating an existing location."""
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    operating_hours: Optional[Dict[str, str]] = None
    instagram: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    typical_spending: Optional[str] = None
    images: Optional[List[str]] = None
    premium_only: Optional[bool] = None

class SubscriptionPlan(BaseModel):
    """Subscription plan model."""
    id: str
    name: str
    description: Optional[str] = None
    price: float
    features: List[str]

class UserSubscription(BaseModel):
    """User subscription model."""
    id: int
    user_id: str
    plan_id: str
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool = True

class UserProfile(BaseModel):
    """User profile model."""
    id: str
    email: str
    full_name: Optional[str] = None
    subscription: Optional[SubscriptionPlan] = None

class LoginActivity(BaseModel):
    """Login activity model for tracking user logins."""
    id: Optional[int] = None
    user_id: str
    email: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_info: Optional[str] = None
    login_status: str  # "success" or "failed"
    login_time: datetime = Field(default_factory=datetime.now)
    location: Optional[str] = None  # Approximate location based on IP