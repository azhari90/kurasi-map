import os
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from dotenv import load_dotenv
from pathlib import Path

from app.core.config import settings
from app.api.routes import api_router
from app.core.auth import get_current_user

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
async def home(request: Request):
    """Render the home page with the map."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.APP_NAME,
            "default_lat": settings.DEFAULT_LAT,
            "default_lng": settings.DEFAULT_LNG,
            "default_zoom": settings.DEFAULT_ZOOM,
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)