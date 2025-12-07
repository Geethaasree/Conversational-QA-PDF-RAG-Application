# Render Deployment Guide - RAG Q&A Application

## **🎉 100% FREE Hosting with Render!**

### **Why Render?**
- ✅ **Completely FREE** tier available
- ✅ **No credit card required** for free tier
- ✅ **Auto-deploy from GitHub**
- ✅ **Free SSL/HTTPS** included
- ✅ **Easy Docker deployment**
- ✅ **750 hours/month free** (enough for 24/7!)

---

## **Quick Overview**

**Free Tier Includes:**
- 750 hours/month of runtime per service
- 512 MB RAM
- Shared CPU
- Free SSL certificates
- Auto-deploy from Git

**Perfect for your RAG Q&A app!**

---

## **Method 1: Deploy from GitHub (Recommended) ⭐**

### **Step 1: Push Your Code to GitHub**

1. **Create a GitHub repository:**
   - Go to https://github.com/new
   - Name it: `rag-qa-app`
   - Make it public or private
   - Click "Create repository"

2. **Push your code:**
   ```cmd
   cd C:\Users\koner\OneDrive\Desktop\Conversational-QA-PDF-RAG-Application-main
   
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/rag-qa-app.git
   git push -u origin main
   ```

### **Step 2: Sign Up for Render**

1. Go to https://render.com/
2. Click "Get Started"
3. **Sign up with GitHub** (easiest)
4. Authorize Render to access your repositories

### **Step 3: Deploy Backend**

1. **In Render Dashboard**, click "New +" → "Web Service"

2. **Connect your repository:**
   - Select `rag-qa-app` repository
   - Click "Connect"

3. **Configure Backend:**
   - **Name**: `rag-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Docker`
   - **Instance Type**: `Free`

4. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable"
   - `GROQ_API_KEY` = your_groq_key
   - `HF_TOKEN` = your_hf_token
   - `ALLOWED_ORIGINS` = `["*"]`

5. **Click "Create Web Service"**

6. **Wait for deployment** (~5-10 minutes)

7. **Copy the backend URL** (e.g., `https://rag-backend.onrender.com`)

### **Step 4: Deploy Frontend**

1. Click "New +" → "Web Service"

2. **Connect same repository** → "Connect"

3. **Configure Frontend:**
   - **Name**: `rag-frontend`
   - **Region**: Same as backend
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Runtime**: `Docker`
   - **Instance Type**: `Free`

4. **Add Environment Variable:**
   - `VITE_API_BASE` = `https://rag-backend.onrender.com` (paste your backend URL)

5. **Click "Create Web Service"**

6. **Wait for deployment** (~5-10 minutes)

### **Step 5: Access Your App!**

Your app will be live at:
- Frontend: `https://rag-frontend.onrender.com`
- Backend: `https://rag-backend.onrender.com`
- API Docs: `https://rag-backend.onrender.com/docs`

---

## **Method 2: Deploy Without GitHub (Manual)**

### **Step 1: Create Render Account**

1. Go to https://render.com/
2. Sign up with email (no credit card needed)
3. Verify your email

### **Step 2: Deploy Backend**

1. Click "New +" → "Web Service"
2. Click "Build and deploy from a Git repository" → "Public Git repository"
3. **Public Git URL**: Leave blank for now
4. Click "Connect"

**Alternative - Use Render CLI:**

```cmd
# Install Render CLI
npm install -g @render/cli

# Login
render login

# Deploy backend
cd backend
render up
```

### **Step 3: Use Render Blueprint (Easiest!)**

1. Click "New +" → "Blueprint"
2. **Connect repository** or upload `render.yaml`
3. Render will auto-detect both services
4. Add environment variables
5. Deploy both at once!

---

## **Important: Handle Cold Starts**

**Free tier services sleep after 15 minutes of inactivity.**

**Solutions:**

1. **Use a ping service (free):**
   - https://uptimerobot.com/ (free, pings every 5 minutes)
   - https://cron-job.org/ (free cron jobs)
   
   Set it to ping: `https://rag-backend.onrender.com/health`

2. **Accept the cold start:**
   - First request takes ~30 seconds
   - Subsequent requests are fast
   - Good for personal projects

3. **Upgrade to paid plan** ($7/month for always-on)

---

## **Configuration Files**

### **render.yaml** (Already created)
Blueprint file for deploying both services at once.

### **.gitignore** (Important!)
Make sure you have:
```
.env
__pycache__/
*.pyc
node_modules/
.venv/
venv/
```

---

## **Environment Variables Setup**

### **Backend Environment Variables:**
```
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
ALLOWED_ORIGINS=["*"]
```

### **Frontend Environment Variables:**
```
VITE_API_BASE=https://rag-backend.onrender.com
```

**Note:** Replace with your actual backend URL after backend is deployed.

---

## **Updating Your App**

### **Auto-deploy (if using GitHub):**
1. Make changes to your code
2. Commit and push to GitHub:
   ```cmd
   git add .
   git commit -m "Update app"
   git push
   ```
3. Render automatically rebuilds and deploys!

### **Manual deploy:**
1. Go to Render dashboard
2. Select your service
3. Click "Manual Deploy" → "Deploy latest commit"

---

## **Monitoring & Logs**

### **View Logs:**
1. Go to your service in Render dashboard
2. Click "Logs" tab
3. See real-time logs

### **Check Status:**
- Green dot = Running
- Yellow dot = Building
- Red dot = Failed

### **Metrics:**
- Click "Metrics" tab
- See CPU, memory usage
- Response times

---

## **Custom Domain (Optional)**

### **Add Your Domain:**

1. **In Render dashboard:**
   - Go to your frontend service
   - Click "Settings" → "Custom Domain"
   - Add your domain (e.g., `myapp.com`)

2. **Update DNS:**
   - Add CNAME record:
   - `www` → `rag-frontend.onrender.com`

3. **SSL is automatic!** Render provides free SSL.

---

## **Cost & Limits**

### **Free Tier:**
- ✅ 750 hours/month per service
- ✅ 2 services = 1500 hours total
- ✅ Enough for 24/7 with ping service
- ✅ 512 MB RAM per service
- ✅ Shared CPU
- ✅ Free SSL

### **Limitations:**
- ⚠️ Services sleep after 15 min inactivity
- ⚠️ Cold start time ~30 seconds
- ⚠️ Limited to 100 GB bandwidth/month
- ⚠️ Shared resources (slower than paid)

### **Paid Plans (Optional):**
- **Starter**: $7/month per service
  - Always-on (no sleeping)
  - Faster response
  - More RAM (512 MB - 8 GB)

---

## **Troubleshooting**

### **Build Failed:**
```
# Check logs in Render dashboard
# Common issues:
1. Missing dependencies in requirements.txt
2. Docker build errors
3. Wrong root directory
```

### **Service Won't Start:**
```
# Check environment variables
1. Verify GROQ_API_KEY is set
2. Verify HF_TOKEN is set
3. Check logs for errors
```

### **CORS Errors:**
```
# Update backend ALLOWED_ORIGINS
ALLOWED_ORIGINS=["https://rag-frontend.onrender.com","http://localhost"]
```

### **Frontend Can't Connect to Backend:**
```
# Check VITE_API_BASE in frontend
VITE_API_BASE=https://rag-backend.onrender.com
# Must match backend URL exactly
```

### **Slow Response:**
```
# This is normal for free tier on cold start
# First request: ~30 seconds
# Subsequent requests: Fast
# Solution: Use ping service (uptimerobot.com)
```

---

## **Best Practices**

1. **Use environment variables** for all secrets
2. **Never commit .env** to GitHub
3. **Enable auto-deploy** from GitHub
4. **Set up ping service** to keep free tier warm
5. **Monitor logs** regularly
6. **Use health check endpoint** (`/health`)

---

## **Comparison with Other Platforms**

| Feature | Render | GCP | AWS | Azure |
|---------|--------|-----|-----|-------|
| **Free Tier** | ✅ Always | 90 days | 12 months | 30 days |
| **No Credit Card** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Auto-deploy** | ✅ Yes | Manual | Manual | Manual |
| **SSL/HTTPS** | ✅ Free | ✅ Free | Manual | ✅ Free |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Best for** | Personal/Demo | Production | Enterprise | Enterprise |

**Winner for free hosting: Render!**

---

## **Quick Commands**

### **Git Commands:**
```cmd
# Initialize repo
git init
git add .
git commit -m "Initial commit"

# Connect to GitHub
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main

# Update deployment
git add .
git commit -m "Update"
git push
```

### **Render CLI:**
```cmd
# Install
npm install -g @render/cli

# Login
render login

# List services
render services list

# View logs
render logs [service-id]
```

---

## **Step-by-Step Checklist**

- [ ] Create GitHub account (if needed)
- [ ] Push code to GitHub repository
- [ ] Sign up for Render (free, no credit card)
- [ ] Deploy backend service
- [ ] Copy backend URL
- [ ] Deploy frontend service with backend URL
- [ ] Test the application
- [ ] (Optional) Set up uptimerobot.com ping
- [ ] (Optional) Add custom domain

---

## **Support & Resources**

- **Render Dashboard**: https://dashboard.render.com/
- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com/
- **GitHub**: https://github.com/
- **UptimeRobot**: https://uptimerobot.com/ (keep service warm)

---

## **Alternative Free Platforms**

If Render doesn't work:

1. **Railway.app**
   - $5/month free credit
   - Easy deployment
   - Good for small apps

2. **Fly.io**
   - Free tier available
   - Docker-friendly
   - Fast edge network

3. **Cyclic.sh**
   - Free tier
   - Great for Node.js
   - Limited for Python/Docker

---

**🎉 Congratulations! Your RAG Q&A app is now on Render for FREE!**

**Enjoy your free hosting with auto-deploy and SSL!**
