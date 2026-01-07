# 🚀 SIMPLE DEPLOYMENT GUIDE

## Deploy to Render (Easiest - No CLI needed!)

### Step 1: Prepare Your Code (Already Done!)
✅ Your code is on GitHub
✅ Dockerfile exists
✅ Requirements are listed

### Step 2: Sign Up for Render

1. Go to: **https://render.com/**
2. Click "Get Started for Free"
3. Sign up with GitHub (click "GitHub" button)
4. Authorize Render to access your repositories

### Step 3: Deploy Redis (5 minutes)

1. In Render dashboard, click **"New +"** (top right)
2. Select **"Redis"**
3. Fill in:
   - **Name**: `task-api-redis`
   - **Region**: Choose closest to you (e.g., Oregon USA)
   - **Plan**: **Free**
4. Click **"Create Redis"**
5. Wait 2 minutes for it to start
6. **IMPORTANT**: Copy the **"Internal Redis URL"** - it looks like:
   ```
   redis://task-api-redis:6379
   ```
   Save this somewhere - you'll need it in a moment!

### Step 4: Deploy Your API (5 minutes)

1. Click **"New +"** again
2. Select **"Web Service"**
3. Find your repository: `RickyH22/-Advanced-API-Patterns`
4. Click **"Connect"**

5. Configure the service:
   - **Name**: `task-management-api`
   - **Region**: Same as Redis
   - **Branch**: `main`
   - **Runtime**: **Docker**
   - **Plan**: **Free**

6. Click **"Create Web Service"**

### Step 5: Add Environment Variables (2 minutes)

While your service is deploying:

1. Scroll down to **"Environment Variables"**
2. Click **"Add Environment Variable"**
3. Add these THREE variables:

   **Variable 1:**
   - Key: `SECRET_KEY`
   - Value: `super-secret-production-key-change-this-12345`

   **Variable 2:**
   - Key: `REDIS_URL`
   - Value: `redis://task-api-redis:6379` (the URL you copied from step 3)

   **Variable 3:**
   - Key: `RATE_LIMIT_PER_MINUTE`
   - Value: `60`

4. Click **"Save Changes"**

This will trigger a redeploy (that's normal!)

### Step 6: Wait for Deployment (3-5 minutes)

Watch the **"Logs"** tab - you'll see:
```
==> Building...
==> Deploying...
==> Your service is live 🎉
```

### Step 7: Get Your URL

1. At the top of the page, you'll see your URL:
   ```
   https://task-management-api.onrender.com
   ```
   Or similar - copy this!

2. Click the URL to open it

3. Add `/docs` to the end:
   ```
   https://task-management-api.onrender.com/docs
   ```

4. You should see your Swagger documentation! 🎉

### Step 8: Test Your Deployment

In the Swagger UI:

1. Try the health check:
   - Click `GET /health`
   - Click "Try it out"
   - Click "Execute"
   - Should return: `{"status": "healthy", ...}`

2. Register a user:
   - Click `POST /api/v1/auth/register`
   - Try it out with:
   ```json
   {
     "email": "test@example.com",
     "username": "testuser",
     "password": "TestPass123"
   }
   ```

3. If both work - **YOU'RE DEPLOYED!** ✅

---

## 🎯 Your Submission URLs

After deployment, you have:

1. **GitHub Repository**: 
   ```
   https://github.com/RickyH22/-Advanced-API-Patterns
   ```

2. **Live API**:
   ```
   https://task-management-api.onrender.com
   ```

3. **Live API Docs**:
   ```
   https://task-management-api.onrender.com/docs
   ```

---

## ⚠️ Important Notes

### Free Tier Limitations:
- ✅ API sleeps after 15 mins of inactivity
- ✅ First request might take 30-60 seconds to wake up
- ✅ This is NORMAL and acceptable for the assignment
- ✅ Tell your professor: "Free tier may need 30s to wake up"

### If Deployment Fails:

**Check Logs:**
1. Go to your service in Render
2. Click "Logs" tab
3. Look for errors

**Common Issues:**

**1. "Redis connection failed"**
- Make sure you copied the Internal Redis URL correctly
- Format should be: `redis://task-api-redis:6379`

**2. "Build failed"**
- Check that Dockerfile is in your repo root
- Verify by going to GitHub and seeing Dockerfile in main folder

**3. "Health check failed"**
- This is normal during initial deployment
- Wait 2-3 minutes for everything to start

---

## 🎥 For Your Demo Video

When showing the deployed API:

1. Open: `https://your-app.onrender.com/docs`
2. Show the health check working
3. Register a user on the LIVE API
4. Create a task on the LIVE API
5. Say: "This is deployed on Render's free tier with Redis for rate limiting"

---

## ✅ Deployment Checklist

- [ ] Render account created
- [ ] Redis service created and running
- [ ] Copied Internal Redis URL
- [ ] Web service connected to GitHub
- [ ] Environment variables added (3 variables)
- [ ] Service deployed successfully
- [ ] Can access /docs endpoint
- [ ] Health check returns healthy
- [ ] Can register a user

---

## 📝 What to Submit

1. **Live URL**: `https://task-management-api.onrender.com`
2. **Mention in README**: Add this at the top of your README:
   ```markdown
   ## 🌐 Live Demo
   - **API**: https://task-management-api.onrender.com
   - **Docs**: https://task-management-api.onrender.com/docs
   ```

---

**That's it! Simple deployment with no command line needed! 🚀**

Need help? The Render dashboard shows everything visually and has great error messages.
