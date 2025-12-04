# Deployment Guide

## Deploy to Render (Free Tier)

Render offers free hosting for web services and PostgreSQL databases, perfect for this PQC Document Authentication application.

### Prerequisites
- GitHub account
- Render account (sign up at https://render.com)

### Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit with production configs"
   ```

2. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/pqc-document-auth.git
   git push -u origin main
   ```

### Step 2: Deploy on Render

#### Option A: Using Blueprint (Recommended - Automated)

1. Go to https://render.com/dashboard
2. Click **"New"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will detect `render.yaml` and automatically create:
   - PostgreSQL database (free tier: 90 days, then expires)
   - Web service connected to the database
5. Click **"Apply"** to start deployment

#### Option B: Manual Setup

1. **Create PostgreSQL Database**:
   - Dashboard → **"New"** → **"PostgreSQL"**
   - Name: `pqc-db`
   - Select **Free tier**
   - Click **"Create Database"**
   - Copy the **Internal Database URL**

2. **Create Web Service**:
   - Dashboard → **"New"** → **"Web Service"**
   - Connect your GitHub repository
   - Configure:
     - **Name**: `pqc-document-auth`
     - **Environment**: `Python 3`
     - **Build Command**: `./build.sh`
     - **Start Command**: `gunicorn wsgi:app`
   - Add Environment Variables:
     - `SECRET_KEY`: Generate a random string (e.g., use `openssl rand -hex 32`)
     - `DATABASE_URL`: Paste the Internal Database URL from step 1
   - Click **"Create Web Service"**

### Step 3: Make build.sh Executable

After first deployment, if the build fails, you may need to make the build script executable:

1. In your local repository:
   ```bash
   chmod +x build.sh
   git add build.sh
   git commit -m "Make build.sh executable"
   git push
   ```

2. Render will auto-redeploy

### Step 4: Verify Deployment

1. Once deployed, Render will provide a URL like: `https://pqc-document-auth.onrender.com`
2. Visit the URL and test:
   - Home page loads
   - Sign page works
   - Verify page works
   - Database persistence (create signature, verify it exists)

### Important Notes

**Free Tier Limitations**:
- **Web Service**: 
  - 750 hours/month (enough for one service)
  - Spins down after 15 minutes of inactivity
  - Takes ~30 seconds to spin back up
- **PostgreSQL**: 
  - 1 GB storage
  - Expires after 90 days (data will be deleted)
  - After expiry, create a new free database

**Production Considerations**:
- Generate a strong `SECRET_KEY` in production
- Consider upgrading to paid tier for:
  - Always-on service (no spin down)
  - Persistent database beyond 90 days
  - More resources

### Troubleshooting

**Build Fails**:
- Check build logs in Render dashboard
- Ensure `build.sh` is executable
- Verify all dependencies in `requirements.txt` are correct

**Database Connection Issues**:
- Verify `DATABASE_URL` environment variable is set correctly
- Check database is in "Available" status
- Ensure database and web service are in the same region

**Application Errors**:
- View logs in Render dashboard
- Check environment variables are set
- Verify directories (uploads, keys) are created

### Alternative Free Hosting Options

1. **Railway** (https://railway.app)
   - 500 hours/month free
   - PostgreSQL included
   - Similar setup process

2. **Fly.io** (https://fly.io)
   - 3 shared-cpu VMs free
   - PostgreSQL available
   - Requires `fly.toml` configuration

3. **PythonAnywhere** (https://www.pythonanywhere.com)
   - Free tier available
   - MySQL instead of PostgreSQL
   - More manual setup required

### Monitoring

Render provides:
- Automatic HTTPS
- Health checks
- Deploy logs
- Application logs
- Metrics dashboard

### Updates

To deploy updates:
```bash
git add .
git commit -m "Your update message"
git push
```

Render automatically redeploys on every push to your main branch.

---

## Local Production Testing

Test production configuration locally:

```bash
# Set environment variables
export SECRET_KEY="your-secret-key-here"
export DATABASE_URL="sqlite:///test.db"  # or PostgreSQL URL

# Run with Gunicorn
gunicorn wsgi:app
```

Access at: http://localhost:8000
