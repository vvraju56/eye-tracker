# Eye Tracker Deployment Guide

## Architecture

```
┌─────────────────┐     HTTP      ┌─────────────────┐
│  Laptop Browser │◄─────────────►│  Render API     │
│  - MediaPipe    │               │  - FastAPI      │
│  - Webcam       │               │  - SQLite DB    │
│  - Mouse Ctrl   │               └─────────────────┘
└─────────────────┘
    (Frontend)              (Backend)
```

## Deploy Backend to Render

### Option 1: Render Blueprint (Recommended)

1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Create a new **Web Service**
4. Settings:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 8000`
5. Add environment variable:
   - `PYTHONUNBUFFERED = true`
6. Create PostgreSQL database:
   - **Name:** `eyetracker`
   - **Plan:** Free
7. Deploy

### Option 2: Manual Deploy

```bash
cd backend
git init
git add .
git commit -m "Add backend"
git remote add origin https://github.com/vvraju56/eye-tracker.git
git push -u origin main
```

Then on Render:
1. Create Web Service from repo
2. Set root directory to `backend`
3. Connect PostgreSQL database
4. Set `DATABASE_URL` from the database connection string

## Deploy Frontend

### Option 1: Static Site on Render

1. Go to [render.com](https://render.com)
2. Create **Static Site**
3. Connect `eye-tracker-react` repo
4. Settings:
   - **Build Command:** `npm install && npm run build`
   - **Output Directory:** `dist`
5. Add environment variable:
   - `VITE_API_URL = https://your-api.onrender.com` (your backend URL)
6. Deploy

### Option 2: GitHub Pages

```bash
cd eye-tracker-react
npm run build
# Upload dist/ folder to gh-pages branch
```

### Option 3: Netlify

1. `npm run build`
2. Drag `dist/` folder to [netlify.com](https://netlify.com)

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgres://user:pass@host:5432/eyetracker
PYTHONUNBUFFERED=true
```

### Frontend (.env.production)
```
VITE_API_URL=https://your-backend.onrender.com
```

## Verify Deployment

Backend: `https://your-backend.onrender.com/` → `{"message":"Eye Tracker API","status":"running"}`

Frontend: Visit the static site URL and start tracking!

## Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (new terminal)
cd eye-tracker-react
npm install
npm run dev
```

## Database Schema

- **sessions**: id, device_id, start_time, end_time, total_focus_time, total_distracted_time
- **focus_logs**: id, session_id, timestamp, status, duration_ms, gaze_x, gaze_y, reason