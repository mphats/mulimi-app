# 🗄️ Database Schema & Setup Guide

This document provides a complete guide to setting up the database for the Agri AI Django Backend application.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Database Files](#database-files)
3. [Quick Setup](#quick-setup)
4. [Detailed Setup](#detailed-setup)
5. [Database Schema](#database-schema)
6. [Functions & Views](#functions--views)
7. [Sample Data](#sample-data)
8. [Maintenance](#maintenance)
9. [Troubleshooting](#troubleshooting)

## 🎯 Overview

The Agri AI Django Backend uses a comprehensive database schema designed for agricultural applications. The database supports:

- **User Management**: Extended user profiles with roles (Admin, Agronomist, Trader, Farmer)
- **Product Marketplace**: Agricultural products with images and pricing
- **Market Data**: Real-time market prices and trends
- **Weather Information**: Weather forecasts and alerts
- **Community Forum**: Posts, replies, and discussions
- **AI Services**: Pest diagnosis and treatment advice
- **Newsletters**: Multilingual farming tips and updates

## 📁 Database Files

The database setup is organized into several files:

| File | Description |
|------|-------------|
| `database_schema.sql` | Main database schema with table definitions |
| `database_indexes_and_functions.sql` | Indexes, triggers, functions, and views |
| `sample_data_and_maintenance.sql` | Sample data and maintenance queries |
| `setup_database.py` | Automated setup script |

## ⚡ Quick Setup

### Option 1: Automated Setup (Recommended)

```bash
# Run the automated setup script
python setup_database.py
```

This script will:
- Create and apply Django migrations
- Collect static files
- Create a superuser account (admin / Admin123!)
- Set up the database schema

### Option 2: Manual Setup

```bash
# 1. Create migrations
python manage.py makemigrations

# 2. Apply migrations
python manage.py migrate

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Create superuser
python manage.py createsuperuser
```

## 🔧 Detailed Setup

### Prerequisites

1. **Python Environment**: Python 3.8+ with virtual environment
2. **Dependencies**: Install requirements with `pip install -r requirements.txt`
3. **Database**: Choose one of the supported databases

### Database Options

#### 1. SQLite (Default - Development)

```bash
# No additional setup required
# Database file: db.sqlite3
```

#### 2. PostgreSQL (Production Recommended)

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib  # Ubuntu/Debian
brew install postgresql  # macOS

# Create database and user
sudo -u postgres createdb agri_ai_db
sudo -u postgres createuser django_user
sudo -u postgres psql -c "ALTER USER django_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE agri_ai_db TO django_user;"

# Update .env file
DB_ENGINE=django.db.backends.postgresql
DB_NAME=agri_ai_db
DB_USER=django_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

#### 3. MySQL

```bash
# Install MySQL
sudo apt-get install mysql-server  # Ubuntu/Debian
brew install mysql  # macOS

# Create database
mysql -u root -p -e "CREATE DATABASE agri_ai_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Update .env file
DB_ENGINE=django.db.backends.mysql
DB_NAME=agri_ai_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

## 🏗️ Database Schema

### Core Tables

#### 1. User Management

```sql
-- Extended user profiles
users_profile (
    id, user_id, role, created_at, updated_at
)

-- Magic links for passwordless authentication
users_magiclink (
    id, token, user_id, created_at, used, expires_at
)
```

#### 2. Product Marketplace

```sql
-- Agricultural products
api_product (
    id, seller_id, name, category, description, quantity, unit,
    price_per_unit, harvest_date, location, contact_phone,
    is_active, created_at, updated_at
)

-- Product images
api_productimage (
    id, product_id, image, uploaded_at
)
```

#### 3. Market Data

```sql
-- Market prices
api_marketprice (
    id, product_category, market_name, location, price_per_unit,
    unit, currency, is_buying, source, recorded_at, is_active
)
```

#### 4. Weather Information

```sql
-- Weather data and forecasts
api_weatherdata (
    id, location, latitude, longitude, temperature, humidity,
    precipitation, wind_speed, description, forecast_date,
    is_alert, alert_message, recorded_at
)
```

#### 5. Community Forum

```sql
-- Community posts
api_communitypost (
    id, author_id, title, content, category, is_question,
    is_resolved, created_at, updated_at
)

-- Community replies
api_communityreply (
    id, post_id, author_id, content, is_solution,
    created_at, updated_at
)
```

#### 6. AI Services

```sql
-- Pest diagnosis results
api_pestdiagnosis (
    id, user_id, crop_type, symptoms, image, diagnosis,
    confidence_score, treatment_advice, created_at
)
```

#### 7. Content Management

```sql
-- Newsletters
api_newsletter (
    id, title, content, category, language, is_published,
    published_at, created_at, updated_at
)

-- API request logs
api_requestlog (
    id, endpoint, request_body, response_body, created_at
)
```

### Data Types & Constraints

- **Categories**: GRAINS, VEGETABLES, FRUITS, LIVESTOCK, DAIRY, OTHER
- **Roles**: ADMIN, AGRONOMIST, TRADER, FARMER
- **Languages**: EN (English), CH (Chichewa)
- **Currency**: MWK (Malawian Kwacha)
- **Validation**: Price >= 0, Quantity > 0, Humidity 0-100, Confidence 0-100

## 🔧 Functions & Views

### Built-in Functions

1. **`get_product_statistics()`**: Returns product analytics
2. **`get_market_price_trends(category, days)`**: Market price trends
3. **`get_weather_alerts(location)`**: Weather alerts
4. **`get_community_statistics()`**: Community activity stats
5. **`search_products(term, category, location, min_price, max_price)`**: Product search

### Database Views

1. **`active_products_view`**: Products with seller information
2. **`market_price_summary_view`**: Market price summaries
3. **`community_posts_summary_view`**: Posts with reply counts
4. **`user_activity_summary_view`**: User activity statistics

### Triggers

- **`update_updated_at_column()`**: Automatically updates `updated_at` timestamps

## 📊 Sample Data

The application includes sample data for testing:

### Users
- **admin** / Admin123! (Superuser)
- **farmer1** / Password123! (Farmer)
- **trader1** / Password123! (Trader)
- **agronomist1** / Password123! (Agronomist)

### Sample Products
- Fresh Maize (100kg, MWK 500/kg)
- Tomatoes (50kg, MWK 800/kg)
- Beans (200kg, MWK 1200/kg)

### Sample Market Prices
- Grains: MWK 550/kg (Lilongwe Market)
- Vegetables: MWK 750/kg (Blantyre Market)
- Fruits: MWK 1200/kg (Mzuzu Market)

### Sample Weather Data
- Lilongwe: 25.5°C, Partly cloudy
- Blantyre: 28.0°C, Light rain (Alert)
- Mzuzu: 22.0°C, Sunny

## 🛠️ Maintenance

### Regular Maintenance Tasks

```sql
-- Clean up expired magic links
DELETE FROM users_magiclink WHERE expires_at < CURRENT_TIMESTAMP;

-- Clean up old request logs (older than 30 days)
DELETE FROM api_requestlog WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '30 days';

-- Archive old market prices (older than 1 year)
CREATE TABLE IF NOT EXISTS api_marketprice_archive AS 
SELECT * FROM api_marketprice WHERE recorded_at < CURRENT_TIMESTAMP - INTERVAL '1 year';
DELETE FROM api_marketprice WHERE recorded_at < CURRENT_TIMESTAMP - INTERVAL '1 year';
```

### Performance Optimization

```sql
-- Analyze tables for better query planning (PostgreSQL)
ANALYZE users_profile;
ANALYZE api_product;
ANALYZE api_marketprice;
ANALYZE api_weatherdata;
ANALYZE api_communitypost;
ANALYZE api_communityreply;
ANALYZE api_pestdiagnosis;

-- Vacuum tables to reclaim storage (PostgreSQL)
VACUUM ANALYZE users_profile;
VACUUM ANALYZE api_product;
VACUUM ANALYZE api_marketprice;
VACUUM ANALYZE api_weatherdata;
VACUUM ANALYZE api_communitypost;
VACUUM ANALYZE api_communityreply;
VACUUM ANALYZE api_pestdiagnosis;
```

### Backup & Restore

#### PostgreSQL
```bash
# Backup
pg_dump -h localhost -U django_user -d agri_ai_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
psql -h localhost -U django_user -d agri_ai_db < backup_file.sql
```

#### MySQL
```bash
# Backup
mysqldump -h localhost -u root -p agri_ai_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
mysql -h localhost -u root -p agri_ai_db < backup_file.sql
```

#### SQLite
```bash
# Backup
cp db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Restore
cp backup_file.sqlite3 db.sqlite3
```

## 🔍 Monitoring Queries

### Database Statistics

```sql
-- User statistics
SELECT 
    COUNT(*) as total_users,
    COUNT(*) FILTER (WHERE is_active = true) as active_users,
    COUNT(*) FILTER (WHERE date_joined >= CURRENT_DATE - INTERVAL '30 days') as new_users_30_days
FROM auth_user;

-- Product statistics
SELECT 
    COUNT(*) as total_products,
    COUNT(*) FILTER (WHERE is_active = true) as active_products,
    COUNT(DISTINCT seller_id) as unique_sellers,
    AVG(price_per_unit) as average_price
FROM api_product;

-- Community activity
SELECT 
    COUNT(*) as total_posts,
    COUNT(*) FILTER (WHERE is_question = true) as questions,
    COUNT(*) FILTER (WHERE is_resolved = true) as resolved_questions,
    COUNT(DISTINCT author_id) as active_users
FROM api_communitypost;
```

### Performance Monitoring (PostgreSQL)

```sql
-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- Check slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Migration Errors

```bash
# Reset migrations (WARNING: This will delete all data)
python manage.py migrate --fake-initial
python manage.py migrate --fake api zero
python manage.py migrate --fake users zero
python manage.py migrate
```

#### 2. Database Connection Issues

```bash
# Test database connection
python manage.py dbshell

# Check Django settings
python manage.py check --database default
```

#### 3. Permission Issues (PostgreSQL)

```sql
-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO django_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO django_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO django_user;
```

#### 4. MySQL Connection Issues

```bash
# Install MySQL client
pip install mysqlclient

# For Windows, you might need:
# pip install mysqlclient-binary
```

### Performance Issues

1. **Slow Queries**: Check if indexes are being used
2. **Large Database**: Consider archiving old data
3. **Memory Issues**: Optimize database configuration
4. **Connection Pool**: Configure connection pooling for production

### Security Considerations

1. **Environment Variables**: Never commit database passwords
2. **Database Permissions**: Use least privilege principle
3. **Backup Encryption**: Encrypt database backups
4. **Connection Security**: Use SSL for database connections in production

## 📚 Additional Resources

- [Django Database Documentation](https://docs.djangoproject.com/en/stable/topics/db/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## 🤝 Support

If you encounter issues with the database setup:

1. Check the troubleshooting section above
2. Review the Django logs: `python manage.py runserver --verbosity=2`
3. Test database connection: `python manage.py dbshell`
4. Verify environment variables in `.env` file

For additional help, please refer to the main project documentation or create an issue in the project repository.
