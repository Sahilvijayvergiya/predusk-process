# Render Deployment Troubleshooting Guide

## 🚨 Common Deployment Issues & Solutions

### 1. **Build Failures**

#### Issue: Missing Dependencies
**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**:
- Ensure `requirements.txt` includes all dependencies
- Check that directory structure is correct
- Verify Python version compatibility

#### Issue: PostgreSQL Driver Installation
**Error**: `psycopg2-binary installation failed`

**Solution**:
```python
# In requirements.txt, use:
psycopg2-binary==2.9.9
# NOT: psycopg2 (requires compilation)
```

### 2. **Database Connection Issues**

#### Issue: Database Connection String
**Error**: `OperationalError: could not connect to server`

**Solution**:
1. **Create PostgreSQL instance first** on Render
2. **Connect database** in web service settings
3. **Verify connection string format**:
   ```
   postgresql://user:password@host:5432/database_name
   ```

#### Issue: Table Creation Failure
**Error**: `OperationalError: relation "documents" does not exist`

**Solution**:
- SQLAlchemy creates tables automatically via `lifespan`
- Check logs for table creation errors
- Verify database permissions

### 3. **Environment Variable Issues**

#### Issue: Missing Environment Variables
**Error**: `KeyError: 'DATABASE_URL'`

**Solution**:
```env
# Required environment variables:
DATABASE_URL=postgresql://user:password@host:5432/document_processor
SECRET_KEY=your-secure-secret-key
FRONTEND_URL=https://your-frontend-domain.onrender.com
PORT=10000
```

### 4. **Runtime Errors**

#### Issue: Port Binding
**Error**: `Address already in use`

**Solution**:
- Use `$PORT` variable provided by Render
- Don't hardcode port numbers
- Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Issue: Module Import Errors
**Error**: `ImportError: cannot import name 'BaseSettings'`

**Solution**:
```python
# Use pydantic v1 syntax:
from pydantic import BaseSettings
# NOT: from pydantic_settings import BaseSettings
```

## 🔍 Debugging Steps

### Step 1: Check Build Logs
1. Go to Render Dashboard → Your Service → Events
2. Look for build errors
3. Check dependency installation failures

### Step 2: Check Runtime Logs
1. Go to Render Dashboard → Your Service → Logs
2. Look for startup errors
3. Check database connection messages

### Step 3: Test Health Endpoint
```bash
curl https://your-service.onrender.com/health
```

### Step 4: Verify Database
1. Go to Render Dashboard → Your Database
2. Check connection status
3. Verify table creation

## 🛠️ Quick Fixes

### Fix 1: Update Requirements
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1
celery==5.3.4
redis==5.0.1
python-multipart==0.0.6
pydantic==1.10.13
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
websockets==12.0
aiofiles==23.2.1
```

### Fix 2: Environment Variables Setup
```python
# In config.py - use os.getenv()
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./document_processor.db")
SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
```

### Fix 3: Production Start Command
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## 📋 Pre-Deployment Checklist

### ✅ Before Deploying:
- [ ] Push latest code to GitHub
- [ ] Verify requirements.txt is complete
- [ ] Test locally with PostgreSQL
- [ ] Check environment variables
- [ ] Create PostgreSQL instance on Render

### ✅ During Deployment:
- [ ] Monitor build logs
- [ ] Check for dependency installation
- [ ] Verify database connection
- [ ] Test health endpoint

### ✅ After Deployment:
- [ ] Test API endpoints
- [ ] Check CORS configuration
- [ ] Verify frontend connectivity
- [ ] Monitor error logs

## 🚨 Specific Error Messages

### `ModuleNotFoundError: No module named 'app'`
**Cause**: Incorrect directory structure or import path
**Fix**: Ensure `app/` directory is in root of repository

### `OperationalError: could not connect to server`
**Cause**: Database connection string incorrect
**Fix**: Use Render's automatic database connection

### `AttributeError: 'Settings' object has no attribute 'DATABASE_URL'`
**Cause**: Pydantic configuration issue
**Fix**: Use `os.getenv()` for environment variables

### `TypeError: 'NoneType' object has no attribute '__getitem__'`
**Cause**: Missing required environment variables
**Fix**: Set all required environment variables in Render

## 🎯 Best Practices

1. **Always use environment variables** for configuration
2. **Test locally** with same database type
3. **Monitor logs** during and after deployment
4. **Use health checks** for monitoring
5. **Keep requirements.txt updated**
6. **Use specific version numbers** in dependencies

---

**Still having issues? Check Render logs and compare with common errors above!** 🚀
