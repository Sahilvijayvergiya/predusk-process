# Render Deployment Guide

## 🚀 Deploying Backend to Render with PostgreSQL

### Prerequisites
- Render account (free tier available)
- Git repository with the backend code
- Updated configuration for production
- PostgreSQL database setup on Render

### Step 1: Create PostgreSQL Database on Render

1. **Go to Render Dashboard** → https://dashboard.render.com
2. **Click "New +"** → "PostgreSQL"
3. **Configure Database**:
   - **Name**: document-processing-db
   - **Database Name**: document_processor
   - **User**: document_processor_user
   - **Plan**: Free tier (or paid based on needs)
4. **Save connection string** for later use

### Step 2: Prepare Repository

1. **Update requirements** to include PostgreSQL driver:
   ```bash
   # psycopg2-binary should be in requirements.txt
   ```

2. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for Render deployment with PostgreSQL"
   git push origin main
   ```

### Step 3: Deploy Backend Service

1. **Go to Render Dashboard** → "New +" → "Web Service"
2. **Connect Repository**:
   - Choose GitHub
   - Select your repository
   - Select the backend folder/sub-repo
3. **Configure Service**:
   - **Name**: document-processing-api
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/health`
4. **Environment Variables**:
   ```
   DATABASE_URL=postgresql://user:password@your-db-host:5432/document_processor
   SECRET_KEY=your-production-secret-key
   FRONTEND_URL=https://your-frontend-domain.onrender.com
   PORT=10000
   ```
5. **Connect Database**:
   - In "Add Database" section, select your PostgreSQL instance
   - This will automatically set DATABASE_URL

### Step 4: Post-Deployment

1. **Test API**:
   ```bash
   curl https://your-api-domain.onrender.com/health
   ```

2. **Check database connection** in Render logs
3. **Verify tables were created** automatically

## 🌐 Deploying Frontend to Render

### Option 1: Static Site (Recommended)

1. **Build frontend locally**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy as Static Site**:
   - In Render: "New +" → "Static Site"
   - Connect to your repository
   - Build command: `cd frontend && npm run build`
   - Publish directory: `frontend/out`
   - Add environment variable: `NEXT_PUBLIC_API_URL=https://your-api-domain.onrender.com/api/v1`

### Option 2: Web Service

For SPA with server-side features:
- **Runtime**: Node
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npm start`
- **Publish Directory**: `frontend/.next`

## 🔧 Configuration Updates Made

### Backend Changes:
✅ PostgreSQL dependency added (`psycopg2-binary`)
✅ Production CORS configuration
✅ Environment variable support
✅ Port configuration ($PORT)
✅ Health check endpoint
✅ Database connection string support

### Environment Variables for PostgreSQL:
```
# From Render PostgreSQL instance
DATABASE_URL=postgresql://document_processor_user:password@your-db-host:5432/document_processor

# Application configuration
SECRET_KEY=generate-secure-random-key
FRONTEND_URL=https://your-frontend-domain.onrender.com
PORT=10000
```

## 📋 Render Services Configuration

The `render.yaml` file includes:

1. **Web Service** (FastAPI Backend):
   - Python environment
   - PostgreSQL database connection
   - Health checks
   - Persistent disk for uploads

2. **PostgreSQL Database**:
   - Dedicated database instance
   - Automatic connection string injection
   - Free tier with 256MB storage

3. **Redis** (Optional for Celery):
   - For background task processing
   - Message broker functionality

## 🧪 Testing PostgreSQL Deployment

### Database Tests:
```bash
# Health check (includes database connectivity)
curl https://your-api-domain.onrender.com/health

# List jobs (tests database queries)
curl https://your-api-domain.onrender.com/api/v1/jobs

# Upload document (tests file + database)
curl -X POST https://your-api-domain.onrender.com/api/v1/documents/upload \
  -F "file=@test.txt"
```

### Frontend Tests:
- Open frontend URL in browser
- Test document upload
- Verify API calls in network tab
- Check console for errors

## 🐛 PostgreSQL Troubleshooting

### Common Issues:

1. **Database Connection Errors**:
   - Verify DATABASE_URL format is correct
   - Check database is running on Render
   - Ensure user permissions are correct

2. **Migration Issues**:
   - SQLAlchemy creates tables automatically
   - Check logs for table creation errors
   - Verify database schema matches models

3. **Build Failures**:
   - psycopg2-binary installation failed
   - Missing system dependencies
   - Review Render build logs

### Database Management:
- **Access**: Render Dashboard → Your Database → Connect
- **Backup**: Render provides automatic backups
- **Monitoring**: Check database metrics in dashboard

## 🎯 PostgreSQL Benefits

### Advantages over SQLite:
✅ **Better Performance** - Optimized for concurrent access
✅ **Scalability** - Handles larger datasets
✅ **ACID Compliance** - Reliable transactions
✅ **Backup & Recovery** - Automated by Render
✅ **Connection Pooling** - Better resource management
✅ **Full-text Search** - Available if needed

### Considerations:
- **Connection Limits**: Free tier has connection limits
- **Storage Limits**: Monitor database size
- **Query Optimization**: Index important columns
- **Migration Strategy**: Use Alembic for schema changes

---

**Your backend is now configured for PostgreSQL deployment on Render!** 🚀
