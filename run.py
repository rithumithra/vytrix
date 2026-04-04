#!/usr/bin/env python3
"""
Vytrix Insurance Platform - Startup Script
"""

import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🛡️ Starting Vytrix Insurance Platform...")
    print("📍 API will be available at: http://localhost:8000")
    print("🌐 Frontend will be available at: frontend/index.html")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )