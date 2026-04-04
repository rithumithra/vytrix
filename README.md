# Vytrix Insurance Platform (Flask)

AI-powered parametric insurance for gig workers - now built with Flask for easy deployment.

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   python run.py
   ```

3. Open http://localhost:5000 in your browser.

## Deploy to Render

1. Connect your GitHub repo to Render.
2. Create a new Web Service.
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python run.py`
5. Render will automatically detect Flask and set the PORT environment variable.

## Features

- User registration
- Premium calculation
- Simple HTML interface
- REST API endpoints

## API Endpoints

- `GET /` - Main page
- `GET /api/health` - Health check
- `POST /api/users/register` - Register user
- `POST /api/policies/calculate-premium` - Calculate premium
