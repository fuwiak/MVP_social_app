"""
AI Business System - FastAPI Backend
Main application entry point with all API routes
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

# Import our modules
from app.routers import (
    dashboard,
    social_media,
    ai_services,
    analytics,
    automation,
    brand_assets,
    cash_flow,
    ad_campaigns
)
from app.core.database import init_db
from app.core.config import settings

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting AI Business System Backend...")
    await init_db()
    print("✅ Database initialized")
    yield
    # Shutdown
    print("🛑 Shutting down AI Business System Backend...")

# Create FastAPI app
app = FastAPI(
    title="AI Business System API",
    description="Complete AI-powered business management system backend",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extract user from JWT token - simplified for demo"""
    # In production, verify JWT token here
    return {"id": "demo-user", "email": "demo@example.com"}

# Health check
@app.get("/health")
async def health_check():
    """System health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Business System Backend",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Business System API",
        "description": "FastAPI backend for intelligent business management",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0"
    }

# Include all routers
app.include_router(
    dashboard.router,
    prefix="/api/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    social_media.router,
    prefix="/api/social-media",
    tags=["Social Media"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    ai_services.router,
    prefix="/api/ai",
    tags=["AI Services"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    analytics.router,
    prefix="/api/analytics",
    tags=["Analytics"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    automation.router,
    prefix="/api/automation",
    tags=["Automation"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    brand_assets.router,
    prefix="/api/brand-assets",
    tags=["Brand Assets"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    cash_flow.router,
    prefix="/api/cash-flow",
    tags=["Cash Flow"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    ad_campaigns.router,
    prefix="/api/ad-campaigns",
    tags=["Ad Campaigns"],
    dependencies=[Depends(get_current_user)]
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )



