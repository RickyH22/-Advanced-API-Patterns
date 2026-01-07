# 🎥 SIMPLE 5-MINUTE DEMO SCRIPT

## Recording Setup (Choose One Tool)

**Windows Game Bar (Easiest - Built-in)**
1. Press `Win + G` to open
2. Click the record button (red circle)
3. Record your screen
4. Press `Win + Alt + R` to stop
5. Videos saved in: `C:\Users\[YourName]\Videos\Captures\`

**OR Loom (Free, Easy Upload)**
1. Go to https://www.loom.com/signup (free account)
2. Download desktop app
3. Click "Start Recording" → Choose "Screen + Camera" or "Screen Only"
4. Automatically uploads and gives you a link!

---

## 🎬 YOUR 5-MINUTE SCRIPT

### Before Recording:
✅ API is running (docker-compose up -d) ✅
✅ Open browser to http://localhost:8000/docs
✅ Close unnecessary tabs/windows
✅ Practice once!

---

### 🎤 SCENE 1: Introduction (30 seconds)

**Say:**
> "Hello, I'm presenting my Task Management API. This is a production-ready API built with FastAPI that demonstrates JWT authentication, rate limiting, async processing, and comprehensive testing."

**Show:**
- Browser at http://localhost:8000/docs
- Scroll down showing all the endpoints
- Point out: Authentication, Tasks, Health checks

---

### 🎤 SCENE 2: Authentication (1 minute)

**In Swagger UI:**

1. **Register a User**
   - Click on `POST /api/v1/auth/register`
   - Click "Try it out"
   - Use this JSON:
   ```json
   {
     "email": "demo@example.com",
     "username": "demouser",
     "password": "DemoPass123"
   }
   ```
   - Click "Execute"
   
   **Say:**
   > "First, I'll register a new user. Notice the password requires uppercase, digits, and minimum length for security."

2. **Copy the Token**
   - In the response, find `access_token`
   - Copy the entire token (without quotes)
   
   **Say:**
   > "The API returns a JWT token that I'll use for authentication."

3. **Authorize**
   - Click the green "Authorize" button at the top
   - Paste your token in the "Value" field
   - Click "Authorize" then "Close"
   
   **Say:**
   > "Now I'm authenticated and can access protected endpoints."

---

### 🎤 SCENE 3: CRUD Operations (1.5 minutes)

**Create Tasks:**

1. Click `POST /api/v1/tasks`
2. Click "Try it out"
3. Create first task:
   ```json
   {
     "title": "Complete API documentation",
     "description": "Write comprehensive README",
     "status": "todo"
   }
   ```
   - Click "Execute"
   
   **Say:**
   > "Creating a task. Notice it returns 201 Created status."

4. Create second task:
   ```json
   {
     "title": "Deploy to production",
     "description": "Deploy API to cloud platform",
     "status": "in_progress"
   }
   ```

**List Tasks:**

5. Click `GET /api/v1/tasks`
6. Click "Try it out"
7. Try with pagination: `skip=0`, `limit=10`
8. Click "Execute"

   **Say:**
   > "Here's the list with pagination. I can also filter by status."

9. Change `status` to "todo" and execute again
   
   **Say:**
   > "Now filtering to show only todo tasks."

**Update a Task:**

10. Click `PATCH /api/v1/tasks/{task_id}`
11. Use task_id `1`
12. Body:
    ```json
    {
      "status": "done"
    }
    ```
13. Execute

    **Say:**
    > "Updating the task status to done. Notice it's a PATCH for partial updates."

---

### 🎤 SCENE 4: Advanced Features (1 minute)

**Health Checks:**

1. Click `GET /health/detailed`
2. Execute

   **Say:**
   > "The health endpoint shows the status of all dependencies including Redis."

**Async Endpoint:**

3. Click `GET /async/external`
4. Execute

   **Say:**
   > "This demonstrates async HTTP calls to external APIs using httpx."

**Show Headers:**

5. Scroll to Response headers
6. Point out:
   - `x-request-id` - for tracking
   - `x-ratelimit-limit` - rate limiting
   - `x-ratelimit-remaining` - requests left
   - `x-process-time` - performance monitoring

   **Say:**
   > "Every response includes tracking headers, rate limit info, and processing time for observability."

---

### 🎤 SCENE 5: Testing & Load Test (1 minute)

**Switch to Terminal (or show in split screen):**

1. Run tests:
   ```bash
   docker-compose exec api pytest --cov=app
   ```
   
   **Say:**
   > "Let me show the test coverage. All tests pass with over 80% coverage as required."

2. Show the coverage report (wait for output)

3. Run load test:
   ```bash
   docker-compose exec api python load_test.py
   ```
   
   **Say:**
   > "Now testing with 100 concurrent requests to demonstrate performance and rate limiting."

4. Wait for results to show

   **Say:**
   > "The API handles high load smoothly, with rate limiting protecting against abuse."

---

### 🎤 SCENE 6: Conclusion (30 seconds)

**Show browser again at /docs**

**Say:**
> "In summary, this API demonstrates:
> - Secure JWT authentication with bcrypt
> - Full REST CRUD operations with proper status codes
> - Rate limiting with Redis
> - Role-based access control
> - Comprehensive error handling
> - Over 80% test coverage
> - Production-ready with health checks and monitoring
> 
> The complete code, tests, and documentation are available on GitHub. Thank you!"

---

## 📤 After Recording:

### If you used Windows Game Bar:
1. Find video in `C:\Users\[YourName]\Videos\Captures\`
2. Upload to:
   - **YouTube**: https://youtube.com/upload (set to "Unlisted")
   - **Google Drive**: Upload and share link
   - **OneDrive**: Upload and get share link

### If you used Loom:
- Automatically uploaded! Just copy the link.

---

## 🎯 Quick Tips:

1. **Practice once** - Do a dry run before recording
2. **Speak clearly** - Don't rush, explain what you're doing
3. **Show, don't just tell** - Execute the requests, show the responses
4. **Keep it simple** - Stick to the script
5. **Don't worry about perfection** - Minor mistakes are fine!

---

**Ready to record? Follow this script and you'll have a great demo! 🎬**
