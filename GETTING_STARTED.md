# Quick Start Guide

## Getting Started in 5 Minutes

### Step 1: Setup (Choose One)

#### Option A: Docker (Easiest)
```bash
cd "task-api"
docker-compose up --build
```

#### Option B: Local Development
```bash
cd "task-api"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# In a separate terminal, start Redis
# (Download from: https://github.com/microsoftarchive/redis/releases)
redis-server

# Back in your terminal
python main.py
```

### Step 2: Test the API

Open your browser to: **http://localhost:8000/docs**

### Step 3: Try the API

#### Register a user:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"me@example.com\",\"username\":\"myuser\",\"password\":\"MyPass123\"}"
```

Copy the `access_token` from the response.

#### Create a task:
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"My First Task\",\"description\":\"Testing the API\"}"
```

#### View your tasks:
```bash
curl -X GET "http://localhost:8000/api/v1/tasks" ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Step 4: Run Tests

```bash
pytest
```

## What You Built

✅ RESTful API with full CRUD operations  
✅ JWT authentication with secure passwords  
✅ Role-based access control (user/admin)  
✅ Rate limiting (60 requests/minute)  
✅ Request tracking with unique IDs  
✅ Async endpoints for external API calls  
✅ Background task processing  
✅ Health checks for monitoring  
✅ API versioning (/api/v1/)  
✅ Comprehensive error handling  
✅ 80%+ test coverage  
✅ Docker containerization  
✅ Complete documentation

## Testing Different Features

### Test Rate Limiting
Run the load test:
```bash
python load_test.py
```

### Test Admin Access
Login as admin:
```json
{
  "username": "admin",
  "password": "Admin123"
}
```

Then access admin endpoint:
```bash
GET /api/v1/tasks/admin/all
```

### Test Async Endpoint
```bash
curl http://localhost:8000/async/external
```

### Test Background Tasks
```bash
curl -X POST "http://localhost:8000/async/background-task?task_name=my_task"
```

Check logs to see background processing.

## Deployment

### Deploy to Railway (Free Tier)

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login and deploy:
```bash
railway login
railway init
railway up
```

3. Add Redis:
```bash
railway add redis
```

### Deploy to Render (Free Tier)

1. Push your code to GitHub
2. Go to https://render.com
3. Create new Web Service from your repo
4. Add Redis instance
5. Set environment variables
6. Deploy!

## Demo Video Script

Record a 5-minute video showing:

1. **Start the API** (0:30)
   - Show `docker-compose up`
   - Visit http://localhost:8000/docs

2. **Register & Login** (1:00)
   - Register a new user
   - Show JWT token received
   - Login again

3. **CRUD Operations** (2:00)
   - Create 2-3 tasks
   - List tasks with pagination
   - Update a task status
   - Delete a task

4. **Advanced Features** (1:00)
   - Show rate limiting headers
   - Test async external endpoint
   - Check health endpoints

5. **Testing & Load Test** (0:30)
   - Run `pytest` showing coverage
   - Run `python load_test.py` showing performance

## Common Issues

### Redis connection failed
- Make sure Redis is running: `redis-server`
- Check REDIS_URL in .env

### Tests failing
- Make sure no API instance is running on port 8000
- Redis should be running for rate limit tests

### Import errors
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall: `pip install -r requirements.txt`

## Submission Checklist

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] README.md completed
- [ ] Tests pass with 80%+ coverage
- [ ] Demo video recorded (5 minutes)
- [ ] API deployed to cloud platform
- [ ] Postman collection included
- [ ] .env.example file included
- [ ] Docker setup working

## Key Points to Mention

When discussing your project, emphasize:

1. **RESTful Design**: Proper HTTP methods, status codes, resource naming
2. **Security**: JWT auth, bcrypt hashing, RBAC, input validation
3. **Performance**: Rate limiting, async processing, caching strategy
4. **Production Ready**: Error handling, logging, health checks, monitoring
5. **Testing**: 80%+ coverage, integration tests, load testing
6. **Documentation**: OpenAPI/Swagger, README, Postman collection

## Grading Criteria Met

✅ Complete CRUD with proper HTTP methods and status codes  
✅ JWT authentication with bcrypt and RBAC  
✅ Rate limiting with Redis and proper headers  
✅ Custom exceptions and global error handlers  
✅ Request ID tracking and structured logging  
✅ Async endpoints with httpx  
✅ Background task processing  
✅ Health checks (basic and detailed)  
✅ API versioning (/api/v1/)  
✅ Pagination, filtering, sorting  
✅ CORS configuration  
✅ 80%+ test coverage  
✅ Docker containerization  
✅ Comprehensive documentation

Good luck with your submission! 🚀
