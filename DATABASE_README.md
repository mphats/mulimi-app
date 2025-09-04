# Database Schema & Setup Guide

## Quick Setup

```bash
# Run automated setup
python setup_database.py

# Or manual setup
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Database Files

- `database_schema.sql` - Main tables and structure
- `database_indexes_and_functions.sql` - Indexes, functions, views
- `sample_data_and_maintenance.sql` - Sample data and maintenance
- `setup_database.py` - Automated setup script

## Database Schema

### Core Tables

1. **User Management**
   - `users_profile` - Extended user profiles with roles
   - `users_magiclink` - Passwordless authentication

2. **Product Marketplace**
   - `api_product` - Agricultural products
   - `api_productimage` - Product images

3. **Market Data**
   - `api_marketprice` - Real-time market prices

4. **Weather Information**
   - `api_weatherdata` - Weather forecasts and alerts

5. **Community Forum**
   - `api_communitypost` - Community posts
   - `api_communityreply` - Post replies

6. **AI Services**
   - `api_pestdiagnosis` - Pest diagnosis results

7. **Content Management**
   - `api_newsletter` - Multilingual newsletters
   - `api_requestlog` - API audit logs

## Sample Data

Default users:
- admin / Admin123! (Superuser)
- farmer1 / Password123! (Farmer)
- trader1 / Password123! (Trader)
- agronomist1 / Password123! (Agronomist)

## Database Support

- **SQLite** (Default - Development)
- **PostgreSQL** (Production Recommended)
- **MySQL** (Production)

## Maintenance

```sql
-- Clean expired magic links
DELETE FROM users_magiclink WHERE expires_at < CURRENT_TIMESTAMP;

-- Clean old request logs
DELETE FROM api_requestlog WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '30 days';
```

## Backup

```bash
# SQLite
cp db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3

# PostgreSQL
pg_dump -h localhost -U django_user -d agri_ai_db > backup.sql

# MySQL
mysqldump -h localhost -u root -p agri_ai_db > backup.sql
```
