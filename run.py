#!/usr/bin/env python3
"""
Vytrix Insurance Platform - Flask Startup Script
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from app.main import app
    port = int(os.environ.get("PORT", 5000))

    print("🛡️ Starting Vytrix Insurance Platform (Flask)...")
    print(f"📍 App will be available at: http://0.0.0.0:{port}")
    print("=" * 50)

    app.run(host="0.0.0.0", port=port)