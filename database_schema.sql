-- =====================================================
-- Agri AI Django Backend - Complete Database Schema
-- =====================================================

-- Set timezone for the session
SET timezone = 'Africa/Blantyre';

-- =====================================================
-- 1. CREATE DATABASE (if not exists)
-- =====================================================

-- For MySQL
-- CREATE DATABASE IF NOT EXISTS agri_ai_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE agri_ai_db;

-- For PostgreSQL
-- CREATE DATABASE agri_ai_db WITH ENCODING 'UTF8' LC_COLLATE='en_US.UTF-8' LC_CTYPE='en_US.UTF-8';

-- For SQLite (default for development)
-- Database file will be created automatically as db.sqlite3

-- =====================================================
-- 2. CUSTOM TABLES CREATION
-- =====================================================

-- Users Profile Table
CREATE TABLE IF NOT EXISTS users_profile (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES auth_user(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL DEFAULT 'FARMER' CHECK (role IN ('ADMIN', 'AGRONOMIST', 'TRADER', 'FARMER')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Magic Link Table for Passwordless Authentication
CREATE TABLE IF NOT EXISTS users_magiclink (
    id BIGSERIAL PRIMARY KEY,
    token UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    used BOOLEAN NOT NULL DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Request Log Table for API Audit
CREATE TABLE IF NOT EXISTS api_requestlog (
    id BIGSERIAL PRIMARY KEY,
    endpoint VARCHAR(100) NOT NULL,
    request_body JSONB,
    response_body JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Products Table
CREATE TABLE IF NOT EXISTS api_product (
    id BIGSERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(20) NOT NULL CHECK (category IN ('GRAINS', 'VEGETABLES', 'FRUITS', 'LIVESTOCK', 'DAIRY', 'OTHER')),
    description TEXT NOT NULL,
    quantity DECIMAL(10,2) NOT NULL CHECK (quantity > 0),
    unit VARCHAR(50) NOT NULL,
    price_per_unit DECIMAL(10,2) NOT NULL CHECK (price_per_unit >= 0),
    harvest_date DATE NOT NULL,
    location VARCHAR(200) NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Product Images Table
CREATE TABLE IF NOT EXISTS api_productimage (
    id BIGSERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES api_product(id) ON DELETE CASCADE,
    image VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Market Prices Table
CREATE TABLE IF NOT EXISTS api_marketprice (
    id BIGSERIAL PRIMARY KEY,
    product_category VARCHAR(50) NOT NULL,
    market_name VARCHAR(100) NOT NULL,
    location VARCHAR(200) NOT NULL,
    price_per_unit DECIMAL(10,2) NOT NULL CHECK (price_per_unit >= 0),
    unit VARCHAR(50) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'MWK',
    is_buying BOOLEAN NOT NULL DEFAULT FALSE,
    source VARCHAR(100) NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Weather Data Table
CREATE TABLE IF NOT EXISTS api_weatherdata (
    id BIGSERIAL PRIMARY KEY,
    location VARCHAR(200) NOT NULL,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    temperature DECIMAL(5,2) NOT NULL,
    humidity INTEGER NOT NULL CHECK (humidity >= 0 AND humidity <= 100),
    precipitation DECIMAL(5,2) NOT NULL DEFAULT 0,
    wind_speed DECIMAL(5,2) NOT NULL DEFAULT 0,
    description VARCHAR(200) NOT NULL,
    forecast_date DATE NOT NULL,
    is_alert BOOLEAN NOT NULL DEFAULT FALSE,
    alert_message TEXT,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Newsletter Table
CREATE TABLE IF NOT EXISTS api_newsletter (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    language VARCHAR(10) NOT NULL CHECK (language IN ('EN', 'CH')),
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Community Posts Table
CREATE TABLE IF NOT EXISTS api_communitypost (
    id BIGSERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    is_question BOOLEAN NOT NULL DEFAULT FALSE,
    is_resolved BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Community Replies Table
CREATE TABLE IF NOT EXISTS api_communityreply (
    id BIGSERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES api_communitypost(id) ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_solution BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Pest Diagnosis Table
CREATE TABLE IF NOT EXISTS api_pestdiagnosis (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    crop_type VARCHAR(100) NOT NULL,
    symptoms TEXT NOT NULL,
    image VARCHAR(255) NOT NULL,
    diagnosis TEXT NOT NULL,
    confidence_score DECIMAL(5,2) NOT NULL CHECK (confidence_score >= 0 AND confidence_score <= 100),
    treatment_advice TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
