-- =====================================================
-- Agri AI Django Backend - Indexes, Functions & Views
-- =====================================================

-- =====================================================
-- 1. INDEXES FOR PERFORMANCE
-- =====================================================

-- Users Profile Indexes
CREATE INDEX IF NOT EXISTS idx_users_profile_user_id ON users_profile(user_id);
CREATE INDEX IF NOT EXISTS idx_users_profile_role ON users_profile(role);

-- Magic Link Indexes
CREATE INDEX IF NOT EXISTS idx_users_magiclink_token ON users_magiclink(token);
CREATE INDEX IF NOT EXISTS idx_users_magiclink_user_id ON users_magiclink(user_id);
CREATE INDEX IF NOT EXISTS idx_users_magiclink_expires_at ON users_magiclink(expires_at);

-- Request Log Indexes
CREATE INDEX IF NOT EXISTS idx_api_requestlog_endpoint ON api_requestlog(endpoint);
CREATE INDEX IF NOT EXISTS idx_api_requestlog_created_at ON api_requestlog(created_at);

-- Product Indexes
CREATE INDEX IF NOT EXISTS idx_api_product_seller_id ON api_product(seller_id);
CREATE INDEX IF NOT EXISTS idx_api_product_category ON api_product(category);
CREATE INDEX IF NOT EXISTS idx_api_product_is_active ON api_product(is_active);
CREATE INDEX IF NOT EXISTS idx_api_product_created_at ON api_product(created_at);
CREATE INDEX IF NOT EXISTS idx_api_product_location ON api_product(location);
CREATE INDEX IF NOT EXISTS idx_api_product_price_per_unit ON api_product(price_per_unit);

-- Product Image Indexes
CREATE INDEX IF NOT EXISTS idx_api_productimage_product_id ON api_productimage(product_id);

-- Market Price Indexes
CREATE INDEX IF NOT EXISTS idx_api_marketprice_product_category ON api_marketprice(product_category);
CREATE INDEX IF NOT EXISTS idx_api_marketprice_location ON api_marketprice(location);
CREATE INDEX IF NOT EXISTS idx_api_marketprice_recorded_at ON api_marketprice(recorded_at);
CREATE INDEX IF NOT EXISTS idx_api_marketprice_is_active ON api_marketprice(is_active);

-- Weather Data Indexes
CREATE INDEX IF NOT EXISTS idx_api_weatherdata_location ON api_weatherdata(location);
CREATE INDEX IF NOT EXISTS idx_api_weatherdata_forecast_date ON api_weatherdata(forecast_date);
CREATE INDEX IF NOT EXISTS idx_api_weatherdata_is_alert ON api_weatherdata(is_alert);
CREATE INDEX IF NOT EXISTS idx_api_weatherdata_recorded_at ON api_weatherdata(recorded_at);

-- Newsletter Indexes
CREATE INDEX IF NOT EXISTS idx_api_newsletter_category ON api_newsletter(category);
CREATE INDEX IF NOT EXISTS idx_api_newsletter_language ON api_newsletter(language);
CREATE INDEX IF NOT EXISTS idx_api_newsletter_is_published ON api_newsletter(is_published);
CREATE INDEX IF NOT EXISTS idx_api_newsletter_published_at ON api_newsletter(published_at);

-- Community Post Indexes
CREATE INDEX IF NOT EXISTS idx_api_communitypost_author_id ON api_communitypost(author_id);
CREATE INDEX IF NOT EXISTS idx_api_communitypost_category ON api_communitypost(category);
CREATE INDEX IF NOT EXISTS idx_api_communitypost_is_question ON api_communitypost(is_question);
CREATE INDEX IF NOT EXISTS idx_api_communitypost_is_resolved ON api_communitypost(is_resolved);
CREATE INDEX IF NOT EXISTS idx_api_communitypost_created_at ON api_communitypost(created_at);

-- Community Reply Indexes
CREATE INDEX IF NOT EXISTS idx_api_communityreply_post_id ON api_communityreply(post_id);
CREATE INDEX IF NOT EXISTS idx_api_communityreply_author_id ON api_communityreply(author_id);
CREATE INDEX IF NOT EXISTS idx_api_communityreply_is_solution ON api_communityreply(is_solution);
CREATE INDEX IF NOT EXISTS idx_api_communityreply_created_at ON api_communityreply(created_at);

-- Pest Diagnosis Indexes
CREATE INDEX IF NOT EXISTS idx_api_pestdiagnosis_user_id ON api_pestdiagnosis(user_id);
CREATE INDEX IF NOT EXISTS idx_api_pestdiagnosis_crop_type ON api_pestdiagnosis(crop_type);
CREATE INDEX IF NOT EXISTS idx_api_pestdiagnosis_created_at ON api_pestdiagnosis(created_at);

-- =====================================================
-- 2. TRIGGERS FOR UPDATED_AT TIMESTAMPS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at columns
CREATE TRIGGER update_users_profile_updated_at 
    BEFORE UPDATE ON users_profile 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_api_product_updated_at 
    BEFORE UPDATE ON api_product 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_api_newsletter_updated_at 
    BEFORE UPDATE ON api_newsletter 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_api_communitypost_updated_at 
    BEFORE UPDATE ON api_communitypost 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_api_communityreply_updated_at 
    BEFORE UPDATE ON api_communityreply 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 3. USEFUL FUNCTIONS AND STORED PROCEDURES
-- =====================================================

-- Function to get product statistics
CREATE OR REPLACE FUNCTION get_product_statistics()
RETURNS TABLE (
    total_products BIGINT,
    active_products BIGINT,
    total_sellers BIGINT,
    avg_price DECIMAL(10,2),
    most_common_category VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::BIGINT as total_products,
        COUNT(*) FILTER (WHERE is_active = true)::BIGINT as active_products,
        COUNT(DISTINCT seller_id)::BIGINT as total_sellers,
        AVG(price_per_unit) as avg_price,
        (SELECT category FROM api_product GROUP BY category ORDER BY COUNT(*) DESC LIMIT 1) as most_common_category
    FROM api_product;
END;
$$ LANGUAGE plpgsql;

-- Function to get market price trends
CREATE OR REPLACE FUNCTION get_market_price_trends(
    p_category VARCHAR(50),
    p_days INTEGER DEFAULT 30
)
RETURNS TABLE (
    date DATE,
    avg_price DECIMAL(10,2),
    min_price DECIMAL(10,2),
    max_price DECIMAL(10,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        DATE(recorded_at) as date,
        AVG(price_per_unit) as avg_price,
        MIN(price_per_unit) as min_price,
        MAX(price_per_unit) as max_price
    FROM api_marketprice
    WHERE product_category = p_category
    AND recorded_at >= CURRENT_DATE - INTERVAL '1 day' * p_days
    AND is_active = true
    GROUP BY DATE(recorded_at)
    ORDER BY date;
END;
$$ LANGUAGE plpgsql;

-- Function to get weather alerts
CREATE OR REPLACE FUNCTION get_weather_alerts(
    p_location VARCHAR(200) DEFAULT NULL
)
RETURNS TABLE (
    id INTEGER,
    location VARCHAR(200),
    description VARCHAR(200),
    alert_message TEXT,
    forecast_date DATE,
    recorded_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        w.id,
        w.location,
        w.description,
        w.alert_message,
        w.forecast_date,
        w.recorded_at
    FROM api_weatherdata w
    WHERE w.is_alert = true
    AND (p_location IS NULL OR w.location = p_location)
    AND w.forecast_date >= CURRENT_DATE
    ORDER BY w.forecast_date, w.recorded_at DESC;
END;
$$ LANGUAGE plpgsql;

-- Function to get community statistics
CREATE OR REPLACE FUNCTION get_community_statistics()
RETURNS TABLE (
    total_posts BIGINT,
    total_replies BIGINT,
    questions_count BIGINT,
    resolved_questions BIGINT,
    active_users BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(p.*)::BIGINT as total_posts,
        COUNT(r.*)::BIGINT as total_replies,
        COUNT(*) FILTER (WHERE p.is_question = true)::BIGINT as questions_count,
        COUNT(*) FILTER (WHERE p.is_question = true AND p.is_resolved = true)::BIGINT as resolved_questions,
        COUNT(DISTINCT p.author_id)::BIGINT as active_users
    FROM api_communitypost p
    LEFT JOIN api_communityreply r ON p.id = r.post_id;
END;
$$ LANGUAGE plpgsql;

-- Function to search products
CREATE OR REPLACE FUNCTION search_products(
    p_search_term TEXT,
    p_category VARCHAR(20) DEFAULT NULL,
    p_location VARCHAR(200) DEFAULT NULL,
    p_min_price DECIMAL(10,2) DEFAULT NULL,
    p_max_price DECIMAL(10,2) DEFAULT NULL
)
RETURNS TABLE (
    id INTEGER,
    name VARCHAR(200),
    category VARCHAR(20),
    description TEXT,
    price_per_unit DECIMAL(10,2),
    location VARCHAR(200),
    seller_username VARCHAR(150),
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        p.name,
        p.category,
        p.description,
        p.price_per_unit,
        p.location,
        u.username as seller_username,
        p.created_at
    FROM api_product p
    JOIN auth_user u ON p.seller_id = u.id
    WHERE p.is_active = true
    AND (
        p.name ILIKE '%' || p_search_term || '%'
        OR p.description ILIKE '%' || p_search_term || '%'
    )
    AND (p_category IS NULL OR p.category = p_category)
    AND (p_location IS NULL OR p.location ILIKE '%' || p_location || '%')
    AND (p_min_price IS NULL OR p.price_per_unit >= p_min_price)
    AND (p_max_price IS NULL OR p.price_per_unit <= p_max_price)
    ORDER BY p.created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 4. VIEWS FOR COMMON QUERIES
-- =====================================================

-- View for active products with seller info
CREATE OR REPLACE VIEW active_products_view AS
SELECT 
    p.id,
    p.name,
    p.category,
    p.description,
    p.quantity,
    p.unit,
    p.price_per_unit,
    p.harvest_date,
    p.location,
    p.contact_phone,
    p.created_at,
    u.username as seller_username,
    u.email as seller_email,
    up.role as seller_role
FROM api_product p
JOIN auth_user u ON p.seller_id = u.id
LEFT JOIN users_profile up ON u.id = up.user_id
WHERE p.is_active = true;

-- View for market price summary
CREATE OR REPLACE VIEW market_price_summary_view AS
SELECT 
    product_category,
    location,
    AVG(price_per_unit) as avg_price,
    MIN(price_per_unit) as min_price,
    MAX(price_per_unit) as max_price,
    COUNT(*) as price_count,
    MAX(recorded_at) as last_updated
FROM api_marketprice
WHERE is_active = true
GROUP BY product_category, location;

-- View for community posts with reply counts
CREATE OR REPLACE VIEW community_posts_summary_view AS
SELECT 
    p.id,
    p.title,
    p.content,
    p.category,
    p.is_question,
    p.is_resolved,
    p.created_at,
    p.updated_at,
    u.username as author_username,
    COUNT(r.id) as reply_count,
    COUNT(r.id) FILTER (WHERE r.is_solution = true) as solution_count
FROM api_communitypost p
JOIN auth_user u ON p.author_id = u.id
LEFT JOIN api_communityreply r ON p.id = r.post_id
GROUP BY p.id, u.username;

-- View for user activity summary
CREATE OR REPLACE VIEW user_activity_summary_view AS
SELECT 
    u.id,
    u.username,
    u.email,
    u.date_joined,
    u.last_login,
    up.role,
    COUNT(DISTINCT p.id) as products_count,
    COUNT(DISTINCT cp.id) as posts_count,
    COUNT(DISTINCT cr.id) as replies_count,
    COUNT(DISTINCT pd.id) as diagnoses_count
FROM auth_user u
LEFT JOIN users_profile up ON u.id = up.user_id
LEFT JOIN api_product p ON u.id = p.seller_id
LEFT JOIN api_communitypost cp ON u.id = cp.author_id
LEFT JOIN api_communityreply cr ON u.id = cr.author_id
LEFT JOIN api_pestdiagnosis pd ON u.id = pd.user_id
GROUP BY u.id, up.role;
