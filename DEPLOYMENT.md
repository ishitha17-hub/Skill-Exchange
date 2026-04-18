# Skill-Exchange Project Root

This directory contains the complete Skill-Exchange application ready for deployment.

## Project Structure
```
skill-exchange/
├── backend/              # Flask API server
│   ├── app.py           # Main application
│   ├── config.py        # Configuration
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   └── utils/           # Utility functions
├── frontend/            # HTML templates & static files
│   ├── templates/       # Jinja2 templates
│   └── static/          # CSS, JS, images
├── requirements.txt     # Python dependencies
├── runtime.txt         # Python version
└── Procfile            # Deployment command
```

## Quick Start (Local Development)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up MongoDB Locally
```bash
# Make sure MongoDB is running on localhost:27017
mongod
```

### 3. Run Application
```bash
cd backend
python app.py
```

Visit: `http://localhost:5005`

---

## Cloud Deployment Guide (Recommended: Render.com - Free Tier)

### Step 1: Prepare MongoDB (Cloud)
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up (free account)
3. Create a cluster (free tier available)
4. Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/smart_skill_exchange?retryWrites=true&w=majority`

### Step 2: Deploy to Render
1. Push your project to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/skill-exchange.git
   git push -u origin main
   ```

2. Go to [Render.com](https://render.com)
3. Sign up with GitHub account
4. Click "New +" → "Web Service"
5. Select your GitHub repository
6. Fill in settings:
   - **Name**: skill-exchange
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
   
7. Add Environment Variables:
   - `MONGO_URI`: Your MongoDB Atlas connection string
   - `SECRET_KEY`: Generate a random string (e.g., use `python -c "import secrets; print(secrets.token_hex(32))"`)

8. Click "Create Web Service"
9. Wait 3-5 minutes for deployment
10. View live at: `https://skill-exchange.onrender.com`

### Step 3: Share with Team
Send this link to your team: `https://skill-exchange.onrender.com`

**Demo Credentials:**
- Admin: admin@site.com / admin123
- User: user@site.com / user123

---

## Alternative Hosting Options

### Railway.app (Also Free)
- Go to [Railway.app](https://railway.app)
- Connect GitHub
- Select project
- Auto-deploys on push
- Similar setup to Render

### Heroku (Paid, but has free tier equivalent on alternatives)
- Previously had free tier, now paid
- Still viable option if you want Heroku ecosystem

---

## Environment Variables Needed

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with:
- `SECRET_KEY`: Any random string
- `MONGO_URI`: Your MongoDB Atlas connection

---

## Troubleshooting

### Issue: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Issue: MongoDB Connection Error
- Verify MONGO_URI is correct
- Check firewall allows remote connections (Atlas settings)
- Ensure IP whitelist includes host (Atlas → Network Access)

### Issue: Port Already in Use
```bash
# Kill process on port 5005
lsof -ti:5005 | xargs kill -9
```

### Issue: Static Files Not Loading
- Check `frontend/static/` exists
- Verify paths in templates are relative

---

## Features

✅ **User Authentication** - Login/Register/Reset Password  
✅ **Create Skill Courses** - Upload custom courses  
✅ **Mock Tests** - Create & take tests with questions  
✅ **Question Management** - Add multiple choice questions  
✅ **Certificates** - Earn certificates on 70%+ score  
✅ **Admin Dashboard** - Manage users, skills, tests  
✅ **Responsive Design** - Works on desktop & mobile  

---

## File Sizes & Performance

- Total Size: ~5MB
- Database: Minimal (under 100MB with free MongoDB)
- Static Assets: ~2MB
- Perfect for small to medium teams

---

## Security Notes

⚠️ **IMPORTANT for Production:**
1. Change `SECRET_KEY` to a random string
2. Set strong `MONGO_URI` credentials
3. Enable MongoDB IP whitelist (Atlas)
4. Use HTTPS (automatic on Render/Railway)
5. Never commit `.env` to git

---

## Support & Documentation

- **MongoDB Docs**: https://docs.mongodb.com
- **Flask Docs**: https://flask.palletsprojects.com
- **Render Docs**: https://render.com/docs
- **Bootstrap Docs**: https://getbootstrap.com/docs

---

## Next Steps

1. ✅ Install requirements.txt
2. ✅ Set up MongoDB Atlas
3. ✅ Deploy to Render/Railway
4. ✅ Share link with team
5. ✅ Monitor logs in hosting dashboard

**All files are ready! Your deployment link will be generated after you follow the Render setup.**
