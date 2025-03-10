import os
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

from app.core.config import settings
from app.api.routes import api_router
from app.core.auth import get_current_user
from app.db import client

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A curated map application with freemium features",
    version="0.1.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

# Set up templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

# Include API routes
app.include_router(api_router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, user=Depends(get_current_user)):
    """Render the home page with the map."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.APP_NAME,
            "default_lat": settings.DEFAULT_LAT,
            "default_lng": settings.DEFAULT_LNG,
            "default_zoom": settings.DEFAULT_ZOOM,
            "user": user,
        },
    )

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Render the login page."""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    """Render the signup page."""
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request, user=Depends(get_current_user)):
    """Render the user profile page."""
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

@app.get("/location/{location_id}", response_class=HTMLResponse)
async def location_detail(request: Request, location_id: int, user=Depends(get_current_user)):
    """Render the location detail page."""
    # In a real app, we would fetch the location from the database
    # and check if the user has access to it based on their subscription
    return templates.TemplateResponse(
        "location_detail.html", 
        {"request": request, "location_id": location_id, "user": user}
    )

# Add admin routes
@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, user=Depends(get_current_user)):
    """Render the admin dashboard."""
    # For development, let's consider any logged-in user as admin
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse(
        "admin/dashboard.html", 
        {"request": request, "user": user}
    )

@app.get("/admin/users", response_class=HTMLResponse)
async def admin_users(request: Request, user=Depends(get_current_user)):
    """Render the admin users page."""
    # For development, let's consider any logged-in user as admin
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    # Get mock users for development
    mock_users = [
        {"id": "1", "email": "user1@example.com", "full_name": "User One", "role": "user", "subscription": "free"},
        {"id": "2", "email": "user2@example.com", "full_name": "User Two", "role": "user", "subscription": "premium"},
        {"id": "3", "email": "admin@example.com", "full_name": "Admin User", "role": "admin", "subscription": "premium"}
    ]
    
    return templates.TemplateResponse(
        "admin/users.html", 
        {"request": request, "user": user, "users": mock_users}
    )

@app.get("/admin/locations", response_class=HTMLResponse)
async def admin_locations(request: Request, user=Depends(get_current_user)):
    """Render the admin locations page."""
    # For development, let's consider any logged-in user as admin
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    # Get locations from the database
    locations = await client.get_locations()
    categories = await client.get_categories()
    
    return templates.TemplateResponse(
        "admin/locations.html", 
        {"request": request, "user": user, "locations": locations, "categories": categories}
    )

@app.get("/admin/login-activities", response_class=HTMLResponse)
async def admin_login_activities(request: Request, user=Depends(get_current_user)):
    """Render the admin login activities page."""
    # For development, let's consider any logged-in user as admin
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    # Get login activities from the database
    login_activities = await client.get_login_activities(limit=100)
    
    return templates.TemplateResponse(
        "admin/login_activities.html", 
        {"request": request, "user": user, "login_activities": login_activities}
    )

# Add a logout route
@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request, response: RedirectResponse = RedirectResponse(url="/")):
    """Log out the user and redirect to the home page."""
    response.delete_cookie(key="access_token")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)