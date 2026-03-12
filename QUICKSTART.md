# Quick Start: Deploy to Vercel + Supabase

## 🎯 5-Minute Quick Start

### Step 1: Set Up Supabase
```bash
# 1. Go to https://supabase.com and create a project
# 2. Copy these values from Settings > API:
#    - Project URL (SUPABASE_URL)
#    - Anon Public Key (SUPABASE_KEY)
# 3. Go to Settings > Database to get DATABASE_URL
```

### Step 2: Configure Environment
```bash
# Copy the template file
cp .env.example .env.local

# Edit .env.local with your Supabase credentials
# Update these:
# - DATABASE_URL (from Supabase Settings > Database)
# - SUPABASE_URL (from Settings > API)
# - SUPABASE_KEY (from Settings > API)
# - SECRET_KEY (keep it secret!)
```

### Step 3: Deploy Backend
```bash
# Push your code to GitHub first
git push origin main

# Option A: Deploy API separately (Recommended)
# - Create a Vercel project for your backend
# - Set root directory to `.` or ensure api/ folder is at root
# - Add all environment variables from .env.local
# - Vercel will auto-detect FastAPI and use api/index.py

# Option B: Deploy full-stack on Vercel
# - Include backend in same project
# - Point to repo root
```

### Step 4: Deploy Frontend
```bash
# Create a Vercel project for frontend
# Add these env vars:
VITE_SUPABASE_URL=your-supabase-url
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_API_URL=your-backend-vercel-url
```

### Step 5: Update CORS
Edit `api/main.py` and add your Vercel frontend URL:
```python
origins = [
    "http://localhost:5173",
    "https://your-frontend-app.vercel.app",  # Add this
]
```

---

## 📋 Deployment Checklist

- [ ] Created Supabase project
- [ ] Copied DATABASE_URL, SUPABASE_URL, SUPABASE_KEY
- [ ] Updated .env.local with credentials
- [ ] Pushed code to GitHub
- [ ] Created Vercel project(s)
- [ ] Added environment variables to Vercel
- [ ] Updated CORS origins in api/main.py
- [ ] First deployment completed
- [ ] Tested backend API endpoints
- [ ] Tested database connections
- [ ] Tested file uploads to Supabase Storage

---

## 🔧 Useful Commands

```bash
# Local development
npm run dev              # Start frontend dev server

# Backend in separate terminal
source venv/bin/activate  # Windows: venv\Scripts\activate
cd api
uvicorn main:app --reload

# Build for production
npm run build
tsc -b

# Test Vercel locally
npm i -g vercel
vercel env pull .env.production.local
vercel dev
```

---

## 🐛 Common Issues & Fixes

### "Cannot connect to database"
- Check DATABASE_URL format in .env
- Verify Supabase project is running
- Ensure firewall allows port 5432

### "CORS error when calling API"
- Add frontend URL to `origins` in api/main.py
- Redeploy backend after changes
- Check CORS middleware is enabled

### "Environment variables not loading"
- Redeploy Vercel project after adding env vars
- Use `vercel env pull` to test locally
- Check variable names are correct

### "Supabase storage errors"
- Verify bucket name in .env matches actual bucket
- Check bucket is public or has correct policies
- Ensure SUPABASE_BUCKET_NAME is set

---

## 📚 Full Documentation
See [DEPLOYMENT.md](./DEPLOYMENT.md) for comprehensive setup guide.
