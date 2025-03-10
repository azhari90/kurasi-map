import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings."""
    
    # App settings
    APP_NAME: str = os.getenv("APP_NAME", "Kurasi Map")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key-for-dev")
    
    # Supabase settings
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")
    
    # Map settings - Jakarta, Indonesia coordinates
    DEFAULT_LAT: float = float(os.getenv("DEFAULT_LAT", "-6.2088"))  # Jakarta latitude
    DEFAULT_LNG: float = float(os.getenv("DEFAULT_LNG", "106.8456"))  # Jakarta longitude
    DEFAULT_ZOOM: int = int(os.getenv("DEFAULT_ZOOM", "13"))
    
    # Subscription plans
    FREE_PLAN_ID: str = "free"
    PREMIUM_PLAN_ID: str = "premium"
    
    # Category access (which categories are accessible to free users)
    FREE_CATEGORIES: list = ["restaurants", "cafes"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()