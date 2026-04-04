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
    port = int(os.environ.get("PORT", 8000))
    
    print("🛡️ Starting Vytrix Insurance Platform...")
    print(f"📍 API will be available at: http://0.0.0.0:{port}")
    print("🌐 Frontend will be available at: frontend/index.html")
    print(f"📚 API Documentation: http://0.0.0.0:{port}/docs")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )