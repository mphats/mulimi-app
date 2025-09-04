# 🗄️ MySQL Database Setup Guide for Agri AI Backend

## 🚀 Quick Start

### Step 1: Install MySQL Server
1. Download MySQL Community Server from: https://dev.mysql.com/downloads/mysql/
2. Install with default settings
3. Remember your root password during installation

### Step 2: Create Environment File
Create a `.env` file in your project root with this content:

```bash
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings - MySQL
DB_ENGINE=django.db.backends.mysql
DB_NAME=agri_ai_db
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_HOST=localhost
DB_PORT=3306

# CORS Settings
CORS_ALLOW_ALL=true
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# API Keys (comma-separated)
API_KEYS=dev-key-123,your-api-key-here

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=
EMAIL_PORT=
EMAIL_USE_TLS=false
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@mlimiapp.com
FRONTEND_BASE_URL=http://localhost:8000

# Celery Settings
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
CELERY_TASK_ALWAYS_EAGER=false

# Redis Settings
REDIS_URL=redis://redis:6379/1

# AI Model Settings (optional)
OPENAI_API_KEY=your-openai-api-key-here
PLANTVILLAGE_API_KEY=your-plantvillage-api-key-here
```

**⚠️ Important:** Replace `your_mysql_password_here` with your actual MySQL root password!

### Step 3: Run MySQL Setup Script
```bash
python setup_mysql.py
```

This script will:
- Create the `agri_ai_db` database
- Test the connection
- Show you available databases

### Step 4: Run Django Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Test the Application
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/login/

## 🔧 Troubleshooting

### Common Issues:

#### 1. "Access denied for user 'root'@'localhost'"
**Solution:** 
- Make sure MySQL is running
- Check your password in the `.env` file
- Try connecting manually: `mysql -u root -p`

#### 2. "Can't connect to MySQL server"
**Solution:**
- Start MySQL service
- Check if MySQL is running on port 3306
- Verify firewall settings

#### 3. "Unknown database 'agri_ai_db'"
**Solution:**
- Run the setup script: `python setup_mysql.py`
- Check database creation logs

#### 4. Django Migration Errors
**Solution:**
- Delete all migration files (except `__init__.py`)
- Delete the database
- Run: `python manage.py makemigrations`
- Run: `python manage.py migrate`

## 📊 Database Schema

After successful migration, you'll have these tables:
- `auth_user` - User accounts
- `api_product` - Marketplace products
- `api_marketprice` - Market prices
- `api_weatherdata` - Weather information
- `api_communitypost` - Forum posts
- `api_newsletter` - Newsletters
- `api_pestdiagnosis` - AI pest diagnosis
- And more...

## 🧪 Testing Database Connection

You can test the connection manually:

```python
import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="agri_ai_db"
    )
    print("✅ Connected successfully!")
    connection.close()
except Error as e:
    print(f"❌ Error: {e}")
```

## 🔒 Security Notes

1. **Never commit your `.env` file** to version control
2. **Change default passwords** in production
3. **Use environment variables** for sensitive data
4. **Restrict database access** to necessary users only

## 📝 Next Steps

After successful MySQL setup:

1. **Test the login page** - should work without the magic link error
2. **Create a superuser**: `python manage.py createsuperuser`
3. **Test API endpoints** at: http://127.0.0.1:8000/api/
4. **Connect your Flutter app** to the Django backend

## 🆘 Need Help?

If you encounter issues:

1. Check MySQL service status
2. Verify credentials in `.env` file
3. Check Django error logs
4. Ensure all required packages are installed

## 📦 Required Packages

Make sure these are installed:
```bash
pip install mysqlclient
pip install django-mysql
pip install mysql-connector-python
pip install python-dotenv
```

---

**🎉 Congratulations!** Your Django backend is now connected to MySQL and ready to work with your Flutter mobile app!
