# Render Deployment - Quick Start

## **🚀 Deploy in 3 Simple Steps - 100% FREE!**

### **Why Render?**
✅ Completely FREE  
✅ No credit card needed  
✅ Auto-deploy from GitHub  
✅ Free SSL/HTTPS  
✅ Easy setup  

---

## **Step 1: Push to GitHub**

```cmd
cd C:\Users\koner\OneDrive\Desktop\Conversational-QA-PDF-RAG-Application-main

git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/rag-qa-app.git
git push -u origin main
```

**Create repo first at:** https://github.com/new

---

## **Step 2: Deploy on Render**

1. **Sign up:** https://render.com/ (use GitHub login)

2. **Deploy Backend:**
   - New + → Web Service
   - Connect your `rag-qa-app` repo
   - **Name**: `rag-backend`
   - **Root Directory**: `backend`
   - **Runtime**: Docker
   - **Plan**: Free
   - **Environment Variables:**
     - `GROQ_API_KEY` = your_key
     - `HF_TOKEN` = your_token
     - `ALLOWED_ORIGINS` = `["*"]`
   - Create Service

3. **Copy Backend URL** (e.g., `https://rag-backend.onrender.com`)

4. **Deploy Frontend:**
   - New + → Web Service
   - Connect same repo
   - **Name**: `rag-frontend`
   - **Root Directory**: `frontend`
   - **Runtime**: Docker
   - **Plan**: Free
   - **Environment Variable:**
     - `VITE_API_BASE` = paste_backend_url_here
   - Create Service

---

## **Step 3: Access Your App!**

- **Frontend**: `https://rag-frontend.onrender.com`
- **Backend**: `https://rag-backend.onrender.com/docs`

**Done! Your app is live! 🎉**

---

## **Important: Keep Service Awake**

Free tier sleeps after 15 min inactivity.

**Solution - Use UptimeRobot (FREE):**
1. Go to https://uptimerobot.com/
2. Sign up free
3. Add monitor:
   - Type: HTTP(s)
   - URL: `https://rag-backend.onrender.com/health`
   - Interval: 5 minutes
4. Your service stays awake 24/7!

---

## **Updating Your App**

```cmd
# Make changes, then:
git add .
git commit -m "Update"
git push
```

Render auto-deploys! 🚀

---

## **Troubleshooting**

**Slow first load?**
- Normal for free tier (30 sec cold start)
- Use UptimeRobot to keep warm

**Build failed?**
- Check logs in Render dashboard
- Verify environment variables

**Frontend can't connect?**
- Check `VITE_API_BASE` matches backend URL

---

## **Cost**

**FREE Forever:**
- 750 hours/month per service
- Perfect for personal projects
- Free SSL
- Auto-deploy

**Optional Paid:** $7/month for always-on

---

## **Quick Links**

- **Render Dashboard**: https://dashboard.render.com/
- **Create GitHub Repo**: https://github.com/new
- **UptimeRobot**: https://uptimerobot.com/
- **Full Guide**: See `RENDER_DEPLOYMENT.md`

---

**That's it! Easiest deployment ever! 🎉**
