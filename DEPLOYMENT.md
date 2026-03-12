# Deployment Guide: Supabase + Vercel

This guide covers deploying your full-stack application with:
- **Frontend:** React + Vite → Vercel
- **Backend:** FastAPI → Vercel Serverless Functions
- **Database:** PostgreSQL via Supabase

## Prerequisites

1. **Supabase Account**: https://supabase.com
2. **Vercel Account**: https://vercel.com
3. **Git Repository**: Push your code to GitHub
4. **Node.js 18+** and **Python 3.9+** installed locally

---

## Step 1: Set Up Supabase Database

### 1.1 Create Supabase Project
1. Go to [supabase.com](https://supabase.com) and create a new project
2. Save your **Project URL** and **Anon Public Key** (from Settings > API)
3. Note your **Database Password** (save it securely)

### 1.2 Configure Database Connection
1. In Supabase Dashboard, go to **Settings > Database** to find your connection string
2. Format: `postgresql://postgres:PASSWORD@db.PROJECT_ID.supabase.co:5432/postgres`

### 1.3 Run Migrations
If you have any database migrations, run them against your Supabase database:
```bash
python -m alembic upgrade head
```
Or manually create tables using the Supabase dashboard SQL editor.

### 1.4 Set Up Supabase Storage
1. In Supabase, go to **Storage**
2. Create a bucket named `post-media`
3. Make it public (set access policies as needed)

---

## Step 2: Configure Environment Variables

### 2.1 Local Development
Copy `.env.example` to `.env.local` and fill in your values:
```bash
cp .env.example .env.local
```

Edit `.env.local` with your Supabase credentials:
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_ID.supabase.co:5432/postgres
SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
SUPABASE_KEY=YOUR_ANON_PUBLIC_KEY
SECRET_KEY=your-very-secure-random-key-change-this
```

### 2.2 Vercel Environment Variables
1. Go to your Vercel project settings
2. Navigate to **Settings > Environment Variables**
3. Add all variables from `.env.example` (without `VITE_` prefix for backend endpoints)

**Critical variables for Vercel:**
- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_BUCKET_NAME`
- `SECRET_KEY` (use `openssl rand -hex 32` to generate)
- `ALGORITHM` (set to `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` (set to `30`)

---

## Step 3: Update API Configuration

### 3.1 Update CORS Origins in Backend
Edit `api/main.py` and update the `origins` list with your Vercel deployment URLs:

```python
origins = [
    "http://localhost:5173",  # Local development
    "https://your-app.vercel.app",  # Your Vercel frontend URL
]
```

### 3.2 Update Frontend API Endpoint
In your frontend code, update API calls to use the backend URL:

```typescript
// src/config.ts or equivalent
export const API_URL = process.env.VITE_API_URL || "https://your-api.vercel.app";
```

---

## Step 4: Deploy to Vercel

### 4.1 Frontend Deployment (Recommended: Separate Project)
**Option A: Frontend-only on Vercel**
1. Create a new Vercel project pointing to your repo
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Add environment variables from `.env.example` (prefix with `VITE_`)
5. Deploy!

**Option B: Full-stack on one Vercel project (more complex)**

### 4.2 Backend Deployment
If deploying backend separately:
1. Create API routes in `api/` folder structured for Vercel serverless functions
2. Or use a separate platform (Render, Railway, Heroku) for FastAPI

### 4.3 API Routes for Vercel (Serverless)
Vercel handles Python serverless functions in the `api/` folder:
- Files in `api/` become serverless functions
- `api/index.py` handles all requests and forwards to FastAPI

Update your `api/index.py`:
```python
from fastapi import FastAPI
from main import app  # Import from your main app

# Vercel will use this as the handler
```

---

## Step 5: Verify Deployment

### 5.1 Test Backend
```bash
curl https://your-api.vercel.app/docs
```

### 5.2 Test Database Connection
Hit an endpoint that queries the database and verify it works.

### 5.3 Test Authentication
Test login/signup endpoints to ensure JWT tokens work correctly.

### 5.4 Test File Uploads
Upload a file through the UI and verify it appears in Supabase Storage.

---

## Local Development

### 5.1 Install Dependencies
```bash
# Frontend
npm install

# Backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5.2 Start Backend
```bash
cd api
uvicorn main:app --reload --port 8000
```

### 5.3 Start Frontend
```bash
npm run dev
```

---

## Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` is correct
- Check that PostgreSQL port 5432 is accessible
- Ensure SSL mode is enabled for Supabase

### CORS Errors
- Add your frontend URL to the `origins` list in `api/main.py`
- Check that `allow_credentials=True` is set

### Supabase Storage Issues
- Verify bucket name matches `SUPABASE_BUCKET_NAME`
- Check bucket is public or has correct access policies

### Environment Variables Not Loading
- Vercel caches environment variables; restart deployment after adding them
- Use Vercel CLI to test locally: `vercel env pull`

---

## Additional Resources

- [Vercel Docs](https://vercel.com/docs)
- [Supabase Docs](https://supabase.com/docs)
- [FastAPI + Vercel](https://vercel.com/guides/using-fastapi-with-vercel)
- [SQLAlchemy + PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)

---

## Production Checklist

- [ ] Set strong `SECRET_KEY` using `openssl rand -hex 32`
- [ ] Enable database backups in Supabase
- [ ] Set up database access restrictions
- [ ] Enable CORS only for your frontend domain
- [ ] Set `DEBUG=False` in production
- [ ] Use HTTPS everywhere (Vercel & Supabase do this automatically)
- [ ] Set up error monitoring (Sentry, LogRocket, etc.)
- [ ] Test all critical workflows before going live
