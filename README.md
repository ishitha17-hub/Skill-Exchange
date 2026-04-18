# 🎓 Skill-Exchange Platform

## Overview

A unified platform for skill-sharing and learning where users can:
- 📚 **Upload & Share** custom skill courses
- ✅ **Create Mock Tests** with questions
- 🏆 **Earn Certificates** for passing tests (70%+)
- 👨‍💼 **Manage Content** (Admin dashboard)
- 📱 **Responsive Design** (works on all devices)

---

## 🚀 Quick Start

### Option 1: Live Online (Recommended for Team)
```
🌐 Visit: https://skill-exchange-xxxxx.onrender.com
(Replace xxxxx with your actual Render ID)

Demo Credentials:
- Admin: admin@site.com / admin123
- User: user@site.com / user123
```

### Option 2: Local Development (For Development)

#### Prerequisites
- Python 3.11+
- MongoDB (local or Atlas)
- Git

#### Setup
```bash
# Clone or extract project
cd skill-exchange

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
copy .env.example .env
# Then edit .env with your MongoDB URI

# Run application
cd backend
python app.py

# Visit: http://localhost:5005
```

---

## 📁 Project Structure

```
skill-exchange/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── models/                # Database models
│   │   ├── user.py
│   │   └── admin.py
│   ├── routes/                # API endpoints
│   │   ├── auth_routes.py
│   │   ├── user_routes.py
│   │   ├── admin_routes.py
│   │   └── course_routes.py
│   ├── utils/
│   │   └── pdf_generator.py   # Certificate generation
│   └── static/
│       └── certificates/      # Generated certificates
│
├── frontend/
│   ├── templates/             # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── Upload_skill.html
│   │   ├── manage_tests.html
│   │   ├── Manage_questions.html
│   │   └── mock_test.html
│   └── static/
│       ├── css/style.css
│       └── js/main.js
│
├── requirements.txt           # Python dependencies
├── runtime.txt               # Python version
├── Procfile                  # Deployment configuration
├── .env.example             # Environment template
└── DEPLOY_STEP_BY_STEP.md   # Deployment guide
```

---

## 🔐 Features & Access Levels

### Public User
- Browse available courses
- View skills uploaded by others
- Create and upload custom skill courses
- Take mock tests
- View test results and certificates

### Admin User
- All public user features PLUS:
- Dashboard with statistics
- Manage all users (suspend/delete)
- Create mock tests for skills
- Add questions to tests
- View all certificates
- Manage and moderate content

---

## 📊 Database Schema (MongoDB)

### Collections:

**users**
```javascript
{
  _id: ObjectId,
  name: String,
  email: String (unique),
  password_hash: String,
  role: String ("user" or "admin"),
  is_suspended: Boolean,
  skills_interests: Array,
  created_at: Date
}
```

**skills**
```javascript
{
  skill_id: String (UUID),
  user_id: ObjectId,
  title: String,
  description: String,
  resources: Array,
  created_at: Date
}
```

**mock_tests**
```javascript
{
  _id: ObjectId,
  skill_id: String,
  title: String,
  created_at: Date
}
```

**questions**
```javascript
{
  _id: ObjectId,
  test_id: String,
  question_text: String,
  optionA, optionB, optionC, optionD: String,
  correct_answer: String ("A", "B", "C", or "D"),
  created_at: Date
}
```

**certificates**
```javascript
{
  cert_id: String (UUID),
  user_id: ObjectId,
  course_id or skill_id: String,
  user_name: String,
  skill_name: String,
  source: String ("course" or "skill"),
  date: Date,
  file_path: String
}
```

---

## 🔑 Demo Credentials

### Admin Account
```
Email: admin@site.com
Password: admin123
```
Access: Full admin dashboard, create tests, manage users

### Regular User Account
```
Email: user@site.com
Password: user123
```
Access: Create skills, take tests, view dashboard

---

## 🛠️ Tech Stack

**Backend:**
- Flask 3.0.2 - Web framework
- pymongo 4.6.1 - MongoDB driver
- Flask-Login - Authentication

**Frontend:**
- Bootstrap 5 - UI framework
- Jinja2 - Template engine
- Vanilla JavaScript - Interactivity

**Database:**
- MongoDB - NoSQL database

**Deployment:**
- Render.com - Hosting
- MongoDB Atlas - Cloud database
- Gunicorn - Production server

---

## 📈 Key Workflows

### 1️⃣ User Creates Skill Course
```
User → Dashboard → Upload Skill → Form → Save to DB
```

### 2️⃣ Admin Creates Test for Skill
```
Admin → Manage Tests → Create Test → Select Skill → Generate Test
```

### 3️⃣ Admin Adds Questions to Test
```
Admin → Manage Tests → Click "Questions" → Add Question Form → Save
```

### 4️⃣ User Takes Test
```
User → Mock Tests → Select Test → Answer Questions → Submit → Get Score
```

### 5️⃣ User Earns Certificate (If 70%+)
```
Score ≥ 70% → Certificate Generated → Download PDF → Add to Portfolio
```

---

## 🚀 Deployment

### Live Site: Render.com
**Duration**: 3-5 minutes setup  
**Cost**: Free for 3 months, then $7/month  
**Steps**: See [DEPLOY_STEP_BY_STEP.md](DEPLOY_STEP_BY_STEP.md)

### Local Development
**Duration**: 5 minutes  
**Cost**: Free  
**Steps**: See Quick Start section above

---

## 🐛 Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "Cannot connect to MongoDB" | Connection URI wrong | Check MONGO_URI in .env |
| "Port 5005 already in use" | Process running on port | Kill process or use different port |
| "Static files not loading" | Wrong paths | Check frontend/static/ exists |
| "Login not working" | User not created | Create via MongoDB or use demo creds |
| "502 Bad Gateway (cloud)" | API crashed | Check Render logs |

---

## 👥 Team Collaboration

### Sharing the Platform
Send this link to team:
```
https://skill-exchange-xxxxx.onrender.com
```

### How Team Uses It
1. **Sign Up** with email
2. **Create Skill Course** (Upload_skill page)
3. **Admin Creates Tests** (for that skill)
4. **Admin Adds Questions** (Question management)
5. **Team Members Take Tests**
6. **Download Certificate** if they pass (≥70%)

---

## 📝 Environment Variables

Required for deployment:

```env
# Flask
SECRET_KEY=your-random-secret-key

# MongoDB (use Atlas free tier)
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name

# Python
FLASK_ENV=production (or development)
```

---

## 📞 Support

**Documentation:**
- Flask: https://flask.palletsprojects.com
- MongoDB: https://docs.mongodb.com
- Render: https://render.com/docs

**Issues:**
- Check project logs
- Review DEPLOYMENT.md
- Check MongoDB Atlas dashboard

---

## 📋 Checklist for Team

- [ ] Received deployment link
- [ ] Can login with demo accounts
- [ ] Can browse courses
- [ ] Can upload skill
- [ ] Can create test (admin)
- [ ] Can add questions (admin)
- [ ] Can take test (user)
- [ ] Can download certificate

---

## 🎯 Next Steps

1. Deploy to Render (DEPLOY_STEP_BY_STEP.md)
2. Share link with team
3. Test all features
4. Add custom admin users
5. Create skill courses
6. Launch tests

---

**Ready to go live? Follow [DEPLOY_STEP_BY_STEP.md](DEPLOY_STEP_BY_STEP.md) now!** 🚀

---

*Skill-Exchange Platform | Built with Flask, MongoDB, Bootstrap*
