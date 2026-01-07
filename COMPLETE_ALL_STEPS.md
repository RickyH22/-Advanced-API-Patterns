# 🚀 COMPLETE ALL 3 STEPS - ACTION GUIDE

## ⚡ STEP 1: Start Docker & Test API (10 minutes)

### A. Start Docker Desktop
1. **Press Windows key** and type "Docker Desktop"
2. **Click** to open Docker Desktop
3. **Wait** for Docker to fully start (icon in system tray will stop animating)
4. **Verify**: Open your terminal and run: `docker --version`

### B. Start Your API
Open a terminal in your project folder and run:
```bash
cd "c:\Users\Administrator\OneDrive\Desktop\Workspace\AISE\New folder\task-api"
docker-compose up --build
```

Wait for messages like:
```
✓ Container task-api-redis-1  Started
✓ Container task-api-api-1    Started
```

### C. Test Your API
Open browser to: **http://localhost:8000/docs**

You should see the Swagger UI with all your endpoints!

**Test these endpoints in Swagger UI:**
1. ✅ Health check: `/health` (click Try it out → Execute)
2. ✅ Register: `/api/v1/auth/register` 
   ```json
   {
     "email": "test@example.com",
     "username": "testuser",
     "password": "SecurePass123"
   }
   ```
3. ✅ Login: `/api/v1/auth/login` (copy the access_token from response)
4. ✅ Create Task: `/api/v1/tasks` (click 🔒 Authorize, paste token)
   ```json
   {
     "title": "Test Task",
     "description": "Testing API",
     "status": "todo"
   }
   ```

**Once everything works, keep Docker running and move to Step 2!**

---

## 🎥 STEP 2: Record Demo Video (20 minutes)

### A. Set Up Recording (Choose One)

#### Option 1: Loom (RECOMMENDED - Easiest)
1. Go to: **https://www.loom.com/signup**
2. Sign up (free account)
3. Download desktop app
4. Open Loom → Click "Start Recording"
5. Choose "Screen Only" or "Screen + Camera"
6. Select your browser window
7. Click "Start Recording" (3-2-1 countdown)

#### Option 2: Windows Game Bar
1. Open browser to http://localhost:8000/docs
2. Press **Win + G**
3. Click the **Record button** (red circle)
4. When done, press **Win + Alt + R** to stop
5. Find video in: `C:\Users\Administrator\Videos\Captures\`

### B. Recording Script (5 minutes exactly)

**BEFORE YOU HIT RECORD:**
- ✅ Docker is running (docker-compose up)
- ✅ Browser open to http://localhost:8000/docs
- ✅ Close unnecessary tabs/windows
- ✅ Do a practice run!

**START RECORDING - FOLLOW THIS:**

**[00:00-00:30] Introduction**
> "Hi, I'm presenting my Task Management API. This is a production-ready API built with FastAPI featuring JWT authentication, rate limiting, async processing, and comprehensive testing. Let me show you the interactive API documentation."

**[00:30-01:30] Show Authentication**
1. Scroll through the endpoints
2. Open `/api/v1/auth/register` → Try it out
3. Enter:
   ```json
   {
     "email": "demo@example.com",
     "username": "demouser",
     "password": "SecurePass123"
   }
   ```
4. Execute → Show 201 response
5. Say: "User successfully registered with bcrypt-hashed password"
6. Open `/api/v1/auth/login` → Try it out
7. Enter:
   ```json
   {
     "username": "demouser",
     "password": "SecurePass123"
   }
   ```
8. Execute → **Copy the access_token**
9. Say: "JWT token generated, valid for 30 minutes"

**[01:30-02:30] Show Task Operations**
1. Click **Authorize** button (top right with lock icon)
2. Enter: `Bearer [paste-your-token]` (include the word "Bearer")
3. Click Authorize → Close
4. Say: "Now authenticated, let's create a task"
5. Open `/api/v1/tasks` POST → Try it out
6. Enter:
   ```json
   {
     "title": "Complete demo video",
     "description": "Record 5-minute API demonstration",
     "status": "in_progress"
   }
   ```
7. Execute → Show response
8. Open `/api/v1/tasks` GET → Execute
9. Say: "Task created and retrieved successfully"

**[02:30-03:30] Show Rate Limiting**
1. Open `/health` endpoint
2. Say: "Let me demonstrate rate limiting - watch the response headers"
3. Click Execute **multiple times rapidly** (10-15 times)
4. Point out the headers:
   - `X-RateLimit-Limit: 60`
   - `X-RateLimit-Remaining: [decreasing number]`
5. Keep clicking until you get **429 Too Many Requests**
6. Say: "Rate limit exceeded - this protects the API from abuse using Redis-backed sliding window algorithm"

**[03:30-04:30] Show Async & Load Testing**
1. Open `/async/external` → Execute
2. Say: "This demonstrates async processing - making external API calls without blocking"
3. Open terminal (don't stop recording)
4. Run: `python load_test.py`
5. Say: "Running load test with 100 concurrent requests"
6. Wait for results (takes ~10 seconds)
7. Point out:
   - Success rate
   - Average response time
   - Requests per second
8. Say: "API handles concurrent load efficiently thanks to FastAPI's async capabilities"

**[04:30-05:00] Conclusion**
1. Go back to http://localhost:8000/docs
2. Scroll to show all endpoints
3. Say: "This API demonstrates production-ready patterns including:
   - JWT authentication and RBAC
   - Redis-backed rate limiting  
   - Async/await processing
   - Comprehensive error handling
   - 80%+ test coverage
   - Complete Docker deployment
   Thanks for watching!"

**STOP RECORDING**

### C. Upload & Get Link
- **Loom**: Automatically uploads → Copy the link
- **Game Bar**: Upload to YouTube (unlisted) or Google Drive → Get shareable link

**Save the link - you'll add it to your README next!**

---

## 🌐 STEP 3: Deploy to Cloud (15 minutes)

### A. Sign Up for Render
1. Open: **https://render.com/**
2. Click **"Get Started for Free"**
3. Click **"GitHub"** button to sign in with GitHub
4. Authorize Render to access your repositories

### B. Deploy Redis (5 minutes)
1. In Render dashboard, click **"New +"** (top right corner)
2. Select **"Redis"**
3. Configure:
   - **Name**: `task-api-redis`
   - **Region**: Oregon (USA West) or closest to you
   - **Plan**: Select **"Free"**
4. Click **"Create Redis"**
5. **WAIT** for status to show "Available" (~2 minutes)
6. **CRITICAL**: Click on your Redis instance
7. Look for **"Internal Redis URL"** (looks like: `redis://red-xxxxx:6379`)
8. **COPY THIS URL** - you'll need it in the next step!

### C. Deploy Your API (10 minutes)
1. Click **"New +"** again (top right)
2. Select **"Web Service"**
3. Click **"Connect Git Repository"**
4. If your repo isn't listed:
   - Click "Configure Account"
   - Grant Render access to your specific repository
5. Find and select your `task-api` repository
6. Click **"Connect"**

7. Configure the service:
   - **Name**: `task-management-api` (or any name you like)
   - **Region**: Same as your Redis (Oregon USA West)
   - **Branch**: `main` (or `master` if that's your branch name)
   - **Runtime**: **Docker** (IMPORTANT!)
   - **Plan**: **Free**
   - Leave other settings as default

8. **BEFORE CLICKING CREATE**, scroll down to **"Environment Variables"**

9. Click **"Add Environment Variable"** and add these:

   **Variable 1:**
   - Key: `REDIS_URL`
   - Value: [Paste the Internal Redis URL from step B.8]
   
   **Variable 2:**
   - Key: `SECRET_KEY`
   - Value: `your-super-secret-key-change-in-production-12345`
   
   **Variable 3:**
   - Key: `RATE_LIMIT_PER_MINUTE`
   - Value: `60`

10. Click **"Create Web Service"**

11. **WAIT** for deployment (5-10 minutes)
    - You'll see logs streaming
    - Wait for "Build successful" and "Deploy live"

12. **YOUR API IS LIVE!** 🎉
    - Copy the URL at the top (looks like: `https://task-management-api-xxxx.onrender.com`)

### D. Test Your Live Deployment
1. Open: `https://your-url.onrender.com/health`
   - Should return: `{"status": "healthy"}`
2. Open: `https://your-url.onrender.com/docs`
   - Should show Swagger UI
3. Test register endpoint in the live docs!

**Save your live URL - you'll add it to README!**

---

## 📝 STEP 4: Update Documentation (5 minutes)

Now add everything to your README.md:

### A. Open README.md

Add this section at the very top (after the title):

```markdown
## 🚀 Live Submission

### 📺 Demo Video
🎥 **5-Minute Walkthrough**: [Watch Here](YOUR-VIDEO-LINK)
- Authentication flow demonstration
- Rate limiting in action
- Load testing results
- All API endpoints

### 🌐 Live Deployment
🔗 **Live API**: https://your-app.onrender.com
📖 **Interactive Docs**: https://your-app.onrender.com/docs
🏥 **Health Check**: https://your-app.onrender.com/health

**Try it now**: Visit the docs and test the API!

### 📬 Postman Collection
📦 **File**: `postman_collection.json` (included in repository)
- All endpoints with examples
- Environment variables configured
- Ready to import and test

---
```

### B. Update Postman Collection (Optional)
Add your live URL as an environment variable option:

Open `postman_collection.json` and find the `variable` section (at the bottom).
You can add a comment or second variable for the live URL.

---

## ✅ FINAL CHECKLIST

Before submitting, verify:

- [ ] ✅ **Demo Video**: Recorded, uploaded, link added to README
- [ ] ✅ **Live Deployment**: API deployed to Render, live URL added to README
- [ ] ✅ **Postman Collection**: `postman_collection.json` exists in repository
- [ ] ✅ **Documentation Updated**: README.md has all three items
- [ ] ✅ **Tested Live API**: Visited your-url.onrender.com/health
- [ ] ✅ **Tested Live Docs**: Opened your-url.onrender.com/docs

---

## 🆘 Troubleshooting

### Docker won't start
- Make sure Docker Desktop is installed
- Restart Docker Desktop
- Check if port 8000 is already in use: `netstat -ano | findstr :8000`

### Video is too large
- Loom automatically compresses
- For Game Bar: Use Windows Photos app to trim
- Upload to YouTube as unlisted if file is large

### Render deployment fails
- Check the logs in Render dashboard
- Verify your Dockerfile builds locally: `docker build -t test .`
- Make sure REDIS_URL environment variable is set correctly
- Check that your repo is public or Render has access

### API returns errors on Render
- Check environment variables are set correctly
- View logs: Click on your service → "Logs" tab
- Redis URL must be the Internal URL, not External
- Wait a few minutes - first deploy can take time

---

## 🎯 Quick Reference

### Your Local API
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

### Time Estimates
- Docker setup & testing: 10 minutes
- Record video: 20 minutes
- Deploy to Render: 15 minutes  
- Update docs: 5 minutes
**Total**: ~50 minutes

### Key Commands
```bash
# Start API locally
docker-compose up --build

# Run load test
python load_test.py

# Stop API
docker-compose down
```

---

## 🎓 You've Got This!

Follow each step carefully, don't skip the testing phases, and you'll have everything submitted in under an hour. Good luck! 🚀
