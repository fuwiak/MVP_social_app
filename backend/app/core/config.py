"""
Configuration settings for the AI Business System
"""

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # App settings
    APP_NAME: str = "AI Business System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    
    # AI Services
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Social Media APIs
    FACEBOOK_ACCESS_TOKEN: Optional[str] = os.getenv("FACEBOOK_ACCESS_TOKEN")
    INSTAGRAM_ACCESS_TOKEN: Optional[str] = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    TWITTER_BEARER_TOKEN: Optional[str] = os.getenv("TWITTER_BEARER_TOKEN")
    TWITTER_API_KEY: Optional[str] = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET: Optional[str] = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN: Optional[str] = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_SECRET: Optional[str] = os.getenv("TWITTER_ACCESS_SECRET")
    LINKEDIN_ACCESS_TOKEN: Optional[str] = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    # N8N Integration
    N8N_WEBHOOK_URL: Optional[str] = os.getenv("N8N_WEBHOOK_URL")
    N8N_API_KEY: Optional[str] = os.getenv("N8N_API_KEY")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis for caching and background tasks
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # API Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

