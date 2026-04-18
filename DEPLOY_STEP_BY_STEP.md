# 🚀 Skill-Exchange Cloud Deployment Guide

## Quick Summary
Your Skill-Exchange project is ready to deploy! Follow these exact steps to get it live with a shareable link for your team.

---

## ⏱️ Time Required: ~15 minutes

**What you'll get:**
- ✅ Live website on the internet
- ✅ Shareable link: `https://skill-exchange-XXXXX.onrender.com`
- ✅ Accessible from anywhere to your team
- ✅ Free hosting (no credit card for 3 months, then $7/month)

---

## 📋 Prerequisites

You need:
1. **GitHub account** (free) - [Sign up](https://github.com/signup)
2. **MongoDB Atlas account** (free) - [Sign up](https://www.mongodb.com/cloud/atlas)
3. **Git installed** on your computer - [Download](https://git-scm.com/)

---

## 🗂️ Step 1: Prepare Project for GitHub (5 min)

### 1.1 Open Terminal/Command Prompt
```bash
# Navigate to project directory
cd "d:\skill exchange"
```

### 1.2 Initialize Git
```bash
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 1.3 Create `.env` file (Local Development)
```bash
# Copy the template
copy .env.example .env

# Edit .env and add values (we'll get MongoDB URI next)
# For now, just change SECRET_KEY to something random
```

### 1.4 Add Files to Git
```bash
git add .
git commit -m "Initial commit: Skill Exchange Platform"
```

---

## 🗄️ Step 2: Set Up MongoDB Atlas (Free Cloud Database) (3 min)

### 2.1 Create MongoDB Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Click "Sign Up"
3. Create account (use GitHub for faster signup)

### 2.2 Create Free Cluster
1. Click "Create" next to "Database"
2. Select **"M0 Free"** tier
3. Choose region closest to you
4. Click "Create Cluster" (wait 3-5 min)

### 2.3 Create Database User
1. In MongoDB Atlas, go to **"Database Access"** (left sidebar)
2. Click **"Add New Database User"**
3. Enter username: `admin`
4. Set password: Generate secure password or create custom (save this!)
5. Click "Add User"

### 2.4 Get Connection String
1. Go back to **"Clusters"** 
2. Click **"Connect"** button on your cluster
3. Choose **"Drivers"** (node.js or python)
4. Copy connection string:
   ```
   mongodb+srv://admin:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<password>` with your actual password

### 2.5 Set IP Whitelist
1. Go to **"Network Access"**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (for now; you can restrict later)
4. Click **"Confirm"**

---

## 📦 Step 3: Create GitHub Repository (2 min)

### 3.1 On GitHub Website
1. Go to [github.com/new](https://github.com/new)
2. Repository name: `skill-exchange`
3. Description: "Unified platform for skill-sharing and learning"
4. Make it **Public** (so Render can access it)
5. Click **"Create repository"**

### 3.2 Push to GitHub from Terminal
```bash
cd "d:\skill exchange"

git branch -M main

git remote add origin https://github.com/YOUR_USERNAME/skill-exchange.git
# Replace YOUR_USERNAME with your GitHub username

git push -u origin main
```

**Done!** Your code is now on GitHub.

---

## 🌐 Step 4: Deploy on Render (Cloud Hosting) (3 min)

### 4.1 Create Render Account
1. Go to [Render.com](https://render.com)
2. Click **"Sign Up"**
3. Choose **"Continue with GitHub"**
4. Authorize Render to access your GitHub

### 4.2 Create Web Service
1. On Render dashboard, click **"New +"** → **"Web Service"**
2. Select your `skill-exchange` repository
3. Click **"Connect"**

### 4.3 Configure Service
Fill in the form:

| Field | Value |
|-------|-------|
| **Name** | `skill-exchange` |
| **Environment** | `Python 3` |
| **Region** | Choose closest to you |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT app:app` |
| **Instance Type** | `Free` |

### 4.4 Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add these variables:

**Variable 1: MONGO_URI**
- **Key**: `MONGO_URI`
- **Value**: Your MongoDB connection string from Step 2:
  ```
  mongodb+srv://admin:YOURPASSWORD@cluster.mongodb.net/smart_skill_exchange?retryWrites=true&w=majority
  ```
  Replace `YOURPASSWORD` with actual password!

**Variable 2: SECRET_KEY**
- **Key**: `SECRET_KEY`
- **Value**: Generate random string (copy-paste this in terminal):
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```

**Variable 3: FLASK_ENV**
- **Key**: `FLASK_ENV`
- **Value**: `production`

### 4.5 Deploy
1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. You'll see **"Your service is live"** message

---

## 🎉 Step 5: Your Deployment is Live!

### 5.1 Get Your Live Link
In Render dashboard:
1. Your service name: `skill-exchange`
2. Click on it to see **live deployment URL**
3. Format: `https://skill-exchange-xxxxx.onrender.com`

### 5.2 Add Custom Domain (Optional)
If you have a domain, you can add it in Render settings.

---

## 👥 Step 6: Share with Team

Send this to your team:

```
🎓 Skill-Exchange Platform

Live Link: https://skill-exchange-xxxxx.onrender.com
(Replace xxxxx with your actual ID from Render)

Demo Accounts:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Admin Account:
   Email: admin@site.com
   Password: admin123
   
   (Can create tests, manage users, moderate content)

👤 User Account:
   Email: user@site.com
   Password: user123
   
   (Can create courses, take tests, earn certificates)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Features:
✅ Create and share skill courses
✅ Create mock tests with questions
✅ Take tests and earn certificates
✅ Admin dashboard for management
✅ Responsive design (works on mobile too!)

Questions? See DEPLOYMENT.md for troubleshooting.
```

---

## 🔄 Making Updates

After deployment, if you make changes:

### To Update Live Site:
```bash
cd "d:\skill exchange"

# Make your changes...
git add .
git commit -m "Your commit message"
git push origin main

# Render automatically redeploys within 1-2 minutes!
```

No need to do anything else - just push to GitHub!

---

## 🐛 Troubleshooting

### Issue: "503 Service Unavailable"
**Cause**: Deployment still in progress or MongoDB connection failed  
**Solution**:
1. Wait 2-3 minutes
2. Check Render logs: Click service → "Logs" tab
3. Verify MONGO_URI is correct in environment variables

### Issue: "Cannot GET /"
**Cause**: App started but routes not working  
**Solution**:
1. Open Render logs
2. Look for errors
3. If MongoDB error, check connection string format
4. Restart service: Click "Restart Instance"

### Issue: "Authentication failed"
**Cause**: MongoDB password has special characters  
**Solution**:
1. Regenerate MongoDB password without special chars
2. Update MONGO_URI in Render
3. Restart service

### Issue: Static files (CSS/JS) not loading
**Solution**: Already handled in code! But if broken:
```bash
# Verify files exist:
ls -la frontend/static/
ls -la frontend/templates/
```

### Issue: "Can't push to GitHub"
**Solution**:
```bash
# Generate SSH key first:
ssh-keygen -t ed25519 -C "your.email@example.com"
# Add key to GitHub: Settings → SSH Keys
```

---

## 📊 Performance & Limits

**Free Tier:**
- ✅ Uptime: 95% (good for teams)
- ✅ Database: 512MB MongoDB (plenty for small teams)
- ✅ Web service: 0.5 CPU, 512MB RAM
- ⚠️ Spins down after 15 min inactivity (takes 30 sec to restart)

**For Production:**
- Upgrade to Starter plan ($7/month for always-on)
- Higher resource limits

---

## 📝 Useful Commands Reference

```bash
# Git commands
git init                     # Initialize repo
git add .                    # Add all changes
git commit -m "message"      # Commit
git push origin main         # Push to GitHub
git status                   # Check status

# Local development
cd backend
python app.py               # Run locally
pip install -r requirements.txt  # Install dependencies

# View deployed logs
# (Use Render dashboard → Logs tab)
```

---

## ✅ Checklist Before Demo

- [ ] GitHub repo created and code pushed
- [ ] MongoDB Atlas cluster created
- [ ] Database user created
- [ ] IP whitelist enabled
- [ ] Render deployment complete
- [ ] Environment variables set (MONGO_URI, SECRET_KEY)
- [ ] Live link working
- [ ] Can login with demo credentials
- [ ] Can create skills
- [ ] Can create tests
- [ ] Can add questions
- [ ] Can take test and see results

---

## 🎓 Next Steps

1. ✅ Deploy to Render (today)
2. Test with team (today)
3. Gather feedback
4. Make improvements (update via git push)
5. Scale as needed (upgrade Render tier)

---

## 📞 Support Resources

- **Render Docs**: https://render.com/docs
- **MongoDB Docs**: https://docs.mongodb.com
- **Flask Docs**: https://flask.palletsprojects.com
- **GitHub Help**: https://docs.github.com

---

**🚀 You're all set! Your Skill-Exchange platform is going live!**

Questions? Check the logs in Render dashboard or search for specific error messages above.
