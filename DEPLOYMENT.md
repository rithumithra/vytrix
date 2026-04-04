# 🚀 Vytrix Platform Deployment Guide

## Quick Deploy Options (Choose One)

### 🎯 **Option 1: Render (Recommended - Free)**

**Step 1: Deploy Backend**
1. Go to [render.com](https://render.com) → Sign up/Login
2. Click "New" → "Web Service"
3. Connect GitHub → Select `vytrix` repository
4. Configure:
   ```
   Name: vytrix-backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python run.py
   ```
5. Click "Create Web Service"
6. **Copy the backend URL** (e.g., `https://vytrix-backend.onrender.com`)

**Step 2: Deploy Frontend**
1. Create "New" → "Static Site"
2. Select same `vytrix` repository
3. Configure:
   ```
   Name: vytrix-frontend
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: build
   ```
4. **Update API URL in frontend** (see below)
5. Click "Create Static Site"

**Step 3: Connect Frontend to Backend**
Update `frontend/src/App.js`:
```javascript
// Replace localhost with your Render backend URL
const API_BASE_URL = 'https://vytrix-backend.onrender.com';
```

---

### 🎯 **Option 2: Railway (One-Click)**

1. Go to [railway.app](https://railway.app)
2. Click "Deploy from GitHub repo"
3. Select your `vytrix` repository
4. Railway auto-detects and deploys both frontend and backend
5. Get your live URLs from Railway dashboard

---

### 🎯 **Option 3: Vercel + Railway**

**Backend (Railway):**
1. Deploy backend on Railway (as above)
2. Get backend URL

**Frontend (Vercel):**
1. Go to [vercel.com](https://vercel.com)
2. Import GitHub repository
3. Set Root Directory: `frontend`
4. Update API URL in code
5. Deploy

---

### 🎯 **Option 4: Heroku (If you have account)**

**Backend:**
```bash
# Install Heroku CLI, then:
heroku create vytrix-backend
git subtree push --prefix=. heroku main
```

**Frontend:**
```bash
heroku create vytrix-frontend
heroku buildpacks:set mars/create-react-app
git subtree push --prefix=frontend heroku main
```

---

## 🔧 **Important Configuration Updates**

### **1. Update CORS Settings**
In `app/main.py`, update allowed origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-url.com",  # Add your frontend URL
        "http://localhost:3000"  # Keep for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **2. Update Frontend API URL**
In `frontend/src/App.js`, replace:
```javascript
// Change this:
const API_BASE_URL = 'http://localhost:8000';

// To your deployed backend URL:
const API_BASE_URL = 'https://your-backend-url.com';
```

### **3. Environment Variables (Optional)**
Set these in your deployment platform if you need to override defaults:
```
PORT=8000
DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<dbname>
SECRET_KEY=your-secret-key-here
```

> Note: For Railway deployment, add a PostgreSQL database to your project, and Railway will automatically set `DATABASE_URL`. The app also supports a root-level `config.json` for local development. In production, use `DATABASE_URL` with your managed database.

---

## 🧪 **Test Your Deployment**

After deployment, test these URLs:

**Backend Health Check:**
```
https://your-backend-url.com/health
```

**API Documentation:**
```
https://your-backend-url.com/docs
```

**Frontend App:**
```
https://your-frontend-url.com
```

**Test Scenarios:**
1. Register a user
2. Calculate premium
3. Test rain scenario → Should get ₹400 payout
4. Test fraud scenario → Should get ₹0 payout

---

## 🎯 **Expected Live URLs**

After deployment, you'll have:
- **Frontend**: `https://vytrix-frontend.onrender.com` (or similar)
- **Backend API**: `https://vytrix-backend.onrender.com`
- **API Docs**: `https://vytrix-backend.onrender.com/docs`

---

## 🐛 **Troubleshooting**

**Build Fails:**
- Check Python version in `runtime.txt`
- Ensure all dependencies in `requirements.txt`

**CORS Errors:**
- Update allowed origins in `main.py`
- Check frontend API URL configuration

**Database Issues:**
- SQLite works for demo, but consider PostgreSQL for production
- Database resets on each deployment (normal for demo)

**Frontend Not Loading:**
- Check build command: `npm install && npm run build`
- Verify publish directory: `build`

---

## 🚀 **Go Live Checklist**

✅ Backend deployed and health check passes  
✅ Frontend deployed and loads  
✅ API documentation accessible  
✅ CORS configured for frontend domain  
✅ Test scenarios work end-to-end  
✅ Share live URLs with users  

---

## 📱 **Share Your Live Demo**

Once deployed, share these links:
- **Live App**: `https://your-frontend-url.com`
- **API Docs**: `https://your-backend-url.com/docs`
- **GitHub**: `https://github.com/7032678/vytrix`

**Your Vytrix Insurance Platform will be live and accessible to everyone! 🛡️**