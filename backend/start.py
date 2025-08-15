#!/usr/bin/env python3
"""
AI Business System - FastAPI Backend Startup Script
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    print("🚀 Starting AI Business System Backend...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 ReDoc Documentation: http://localhost:8000/redoc")
    print("💡 Health Check: http://localhost:8000/health")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )



