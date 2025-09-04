-- =====================================================
-- Agri AI Django Backend - Sample Data & Maintenance
-- =====================================================

-- =====================================================
-- 1. SAMPLE DATA INSERTION
-- =====================================================

-- Insert sample users (passwords should be hashed in production)
-- Note: In Django, use User.objects.create_user() instead
INSERT INTO auth_user (username, email, password, is_staff, is_superuser, is_active, date_joined, last_login) VALUES
('admin', 'admin@mlimiapp.com', 'pbkdf2_sha256$600000$...', true, true, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('farmer1', 'farmer1@example.com', 'pbkdf2_sha256$600000$...', false, false, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('trader1', 'trader1@example.com', 'pbkdf2_sha256$600000$...', false, false, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('agronomist1', 'agronomist1@example.com', 'pbkdf2_sha256$600000$...', false, false, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (username) DO NOTHING;

-- Insert user profiles
INSERT INTO users_profile (user_id, role) VALUES
((SELECT id FROM auth_user WHERE username = 'admin'), 'ADMIN'),
((SELECT id FROM auth_user WHERE username = 'farmer1'), 'FARMER'),
((SELECT id FROM auth_user WHERE username = 'trader1'), 'TRADER'),
((SELECT id FROM auth_user WHERE username = 'agronomist1'), 'AGRONOMIST')
ON CONFLICT (user_id) DO NOTHING;

-- Insert sample products
INSERT INTO api_product (seller_id, name, category, description, quantity, unit, price_per_unit, harvest_date, location, contact_phone) VALUES
((SELECT id FROM auth_user WHERE username = 'farmer1'), 'Fresh Maize', 'GRAINS', 'High-quality maize harvested last week', 100.00, 'kg', 500.00, CURRENT_DATE - INTERVAL '7 days', 'Lilongwe', '+265123456789'),
((SELECT id FROM auth_user WHERE username = 'farmer1'), 'Tomatoes', 'VEGETABLES', 'Organic tomatoes from my garden', 50.00, 'kg', 800.00, CURRENT_DATE - INTERVAL '3 days', 'Blantyre', '+265123456789'),
((SELECT id FROM auth_user WHERE username = 'trader1'), 'Beans', 'GRAINS', 'Red beans available in bulk', 200.00, 'kg', 1200.00, CURRENT_DATE - INTERVAL '5 days', 'Mzuzu', '+265987654321')
ON CONFLICT DO NOTHING;

-- Insert sample market prices
INSERT INTO api_marketprice (product_category, market_name, location, price_per_unit, unit, currency, is_buying, source) VALUES
('GRAINS', 'Lilongwe Market', 'Lilongwe', 550.00, 'kg', 'MWK', false, 'Market Survey'),
('VEGETABLES', 'Blantyre Market', 'Blantyre', 750.00, 'kg', 'MWK', false, 'Market Survey'),
('FRUITS', 'Mzuzu Market', 'Mzuzu', 1200.00, 'kg', 'MWK', false, 'Market Survey'),
('GRAINS', 'Lilongwe Market', 'Lilongwe', 480.00, 'kg', 'MWK', true, 'Market Survey')
ON CONFLICT DO NOTHING;

-- Insert sample weather data
INSERT INTO api_weatherdata (location, temperature, humidity, precipitation, wind_speed, description, forecast_date, is_alert) VALUES
('Lilongwe', 25.5, 65, 0.0, 5.2, 'Partly cloudy', CURRENT_DATE, false),
('Blantyre', 28.0, 70, 2.5, 8.1, 'Light rain', CURRENT_DATE, true),
('Mzuzu', 22.0, 60, 0.0, 3.5, 'Sunny', CURRENT_DATE, false)
ON CONFLICT DO NOTHING;

-- Insert sample newsletters
INSERT INTO api_newsletter (title, content, category, language, is_published, published_at) VALUES
('Farming Tips for Rainy Season', 'During the rainy season, ensure proper drainage...', 'Tips', 'EN', true, CURRENT_TIMESTAMP),
('Market Trends This Week', 'Prices for maize have increased by 10%...', 'Market Trends', 'EN', true, CURRENT_TIMESTAMP),
('Ukulima Mwatsopano', 'M''mvula, onetsetsani kuti malo anu ali ndi drainage...', 'Tips', 'CH', true, CURRENT_TIMESTAMP)
ON CONFLICT DO NOTHING;

-- Insert sample community posts
INSERT INTO api_communitypost (author_id, title, content, category, is_question) VALUES
((SELECT id FROM auth_user WHERE username = 'farmer1'), 'Help with maize disease', 'My maize has yellow leaves, what should I do?', 'Question', true),
((SELECT id FROM auth_user WHERE username = 'agronomist1'), 'Best practices for tomato farming', 'Here are some tips for successful tomato farming...', 'Advice', false)
ON CONFLICT DO NOTHING;

-- Insert sample community replies
INSERT INTO api_communityreply (post_id, author_id, content, is_solution) VALUES
((SELECT id FROM api_communitypost WHERE title = 'Help with maize disease'), (SELECT id FROM auth_user WHERE username = 'agronomist1'), 'This looks like nitrogen deficiency. Apply fertilizer...', true),
((SELECT id FROM api_communitypost WHERE title = 'Best practices for tomato farming'), (SELECT id FROM auth_user WHERE username = 'farmer1'), 'Thank you for the advice!', false)
ON CONFLICT DO NOTHING;

-- =====================================================
-- 2. MAINTENANCE QUERIES
-- =====================================================

-- Clean up expired magic links
DELETE FROM users_magiclink WHERE expires_at < CURRENT_TIMESTAMP;

-- Clean up old request logs (older than 30 days)
DELETE FROM api_requestlog WHERE created_at < CURRENT_TIMESTAMP - INTERVAL '30 days';

-- Archive old market prices (older than 1 year)
-- CREATE TABLE IF NOT EXISTS api_marketprice_archive AS 
-- SELECT * FROM api_marketprice WHERE recorded_at < CURRENT_TIMESTAMP - INTERVAL '1 year';
-- DELETE FROM api_marketprice WHERE recorded_at < CURRENT_TIMESTAMP - INTERVAL '1 year';

-- =====================================================
-- 3. USEFUL QUERIES FOR ADMINISTRATION
-- =====================================================

-- Get user statistics
SELECT 
    COUNT(*) as total_users,
    COUNT(*) FILTER (WHERE is_active = true) as active_users,
    COUNT(*) FILTER (WHERE date_joined >= CURRENT_DATE - INTERVAL '30 days') as new_users_30_days
FROM auth_user;

-- Get product statistics
SELECT 
    COUNT(*) as total_products,
    COUNT(*) FILTER (WHERE is_active = true) as active_products,
    COUNT(DISTINCT seller_id) as unique_sellers,
    AVG(price_per_unit) as average_price
FROM api_product;

-- Get market price statistics
SELECT 
    product_category,
    COUNT(*) as price_records,
    AVG(price_per_unit) as avg_price,
    MIN(price_per_unit) as min_price,
    MAX(price_per_unit) as max_price
FROM api_marketprice
WHERE is_active = true
GROUP BY product_category
ORDER BY avg_price DESC;

-- Get community activity
SELECT 
    COUNT(*) as total_posts,
    COUNT(*) FILTER (WHERE is_question = true) as questions,
    COUNT(*) FILTER (WHERE is_resolved = true) as resolved_questions,
    COUNT(DISTINCT author_id) as active_users
FROM api_communitypost;

-- Get weather alerts
SELECT 
    location,
    description,
    alert_message,
    forecast_date
FROM api_weatherdata
WHERE is_alert = true
AND forecast_date >= CURRENT_DATE
ORDER BY forecast_date;

-- =====================================================
-- 4. BACKUP AND RESTORE COMMANDS
-- =====================================================

-- PostgreSQL Backup
-- pg_dump -h localhost -U django_user -d agri_ai_db > backup_$(date +%Y%m%d_%H%M%S).sql

-- PostgreSQL Restore
-- psql -h localhost -U django_user -d agri_ai_db < backup_file.sql

-- MySQL Backup
-- mysqldump -h localhost -u root -p agri_ai_db > backup_$(date +%Y%m%d_%H%M%S).sql

-- MySQL Restore
-- mysql -h localhost -u root -p agri_ai_db < backup_file.sql

-- SQLite Backup
-- cp db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3

-- =====================================================
-- 5. DJANGO MIGRATION COMMANDS
-- =====================================================

-- After creating the schema, run these Django commands:
-- python manage.py makemigrations
-- python manage.py migrate
-- python manage.py createsuperuser
-- python manage.py collectstatic

-- =====================================================
-- 6. GRANTS AND PERMISSIONS (PostgreSQL)
-- =====================================================

-- Grant permissions to Django database user
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO django_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO django_user;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO django_user;

-- =====================================================
-- 7. DATABASE OPTIMIZATION QUERIES
-- =====================================================

-- Analyze tables for better query planning (PostgreSQL)
-- ANALYZE users_profile;
-- ANALYZE api_product;
-- ANALYZE api_marketprice;
-- ANALYZE api_weatherdata;
-- ANALYZE api_communitypost;
-- ANALYZE api_communityreply;
-- ANALYZE api_pestdiagnosis;

-- Vacuum tables to reclaim storage (PostgreSQL)
-- VACUUM ANALYZE users_profile;
-- VACUUM ANALYZE api_product;
-- VACUUM ANALYZE api_marketprice;
-- VACUUM ANALYZE api_weatherdata;
-- VACUUM ANALYZE api_communitypost;
-- VACUUM ANALYZE api_communityreply;
-- VACUUM ANALYZE api_pestdiagnosis;

-- =====================================================
-- 8. MONITORING QUERIES
-- =====================================================

-- Check table sizes (PostgreSQL)
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats
WHERE tablename IN ('users_profile', 'api_product', 'api_marketprice', 'api_weatherdata', 'api_communitypost', 'api_communityreply', 'api_pestdiagnosis')
ORDER BY tablename, attname;

-- Check index usage (PostgreSQL)
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

-- Check slow queries (PostgreSQL)
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
