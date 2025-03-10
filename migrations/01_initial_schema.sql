-- Initial schema for Kurasi Map

-- Enable PostGIS extension for geospatial data
CREATE EXTENSION IF NOT EXISTS postgis;

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT,
    premium_only BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Locations table
CREATE TABLE IF NOT EXISTS locations (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    category_id TEXT NOT NULL REFERENCES categories(id),
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    geom GEOGRAPHY(POINT) GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography) STORED,
    address TEXT,
    operating_hours JSONB,
    instagram TEXT,
    phone TEXT,
    website TEXT,
    typical_spending TEXT,
    images TEXT[],
    premium_only BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create spatial index on geom column
CREATE INDEX IF NOT EXISTS locations_geom_idx ON locations USING GIST (geom);

-- Subscription plans table
CREATE TABLE IF NOT EXISTS subscription_plans (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    features JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- User subscriptions table
CREATE TABLE IF NOT EXISTS user_subscriptions (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    plan_id TEXT NOT NULL REFERENCES subscription_plans(id),
    start_date TIMESTAMPTZ DEFAULT NOW(),
    end_date TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- User favorites table
CREATE TABLE IF NOT EXISTS user_favorites (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    location_id BIGINT NOT NULL REFERENCES locations(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, location_id)
);

-- User view history table
CREATE TABLE IF NOT EXISTS user_view_history (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    location_id BIGINT NOT NULL REFERENCES locations(id),
    viewed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert default categories
INSERT INTO categories (id, name, description, icon, premium_only)
VALUES
    ('restaurants', 'Restaurants', 'Places to eat', 'utensils', FALSE),
    ('cafes', 'Cafes', 'Coffee shops and cafes', 'coffee', FALSE),
    ('sports', 'Sports Venues', 'Sports and fitness locations', 'volleyball-ball', TRUE),
    ('hospitals', 'Hospitals', 'Medical facilities', 'hospital', TRUE),
    ('shopping', 'Shopping', 'Retail stores and malls', 'shopping-bag', TRUE)
ON CONFLICT (id) DO NOTHING;

-- Insert default subscription plans
INSERT INTO subscription_plans (id, name, description, price, features)
VALUES
    ('free', 'Free Plan', 'Basic access to the map', 0.00, '["Access to basic categories", "Limited location details"]'),
    ('premium', 'Premium Plan', 'Full access to all features', 9.99, '["Access to all categories", "All location details", "No advertisements", "Offline maps"]')
ON CONFLICT (id) DO NOTHING;

-- Create Row Level Security (RLS) policies

-- Enable RLS on tables
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE locations ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscription_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_favorites ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_view_history ENABLE ROW LEVEL SECURITY;

-- Categories policies
CREATE POLICY "Categories are viewable by everyone" 
    ON categories FOR SELECT 
    USING (TRUE);

-- Locations policies
CREATE POLICY "Locations are viewable by everyone" 
    ON locations FOR SELECT 
    USING (TRUE);

-- Subscription plans policies
CREATE POLICY "Subscription plans are viewable by everyone" 
    ON subscription_plans FOR SELECT 
    USING (TRUE);

-- User subscriptions policies
CREATE POLICY "Users can view their own subscriptions" 
    ON user_subscriptions FOR SELECT 
    USING (auth.uid() = user_id);

-- User favorites policies
CREATE POLICY "Users can view their own favorites" 
    ON user_favorites FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own favorites" 
    ON user_favorites FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own favorites" 
    ON user_favorites FOR DELETE 
    USING (auth.uid() = user_id);

-- User view history policies
CREATE POLICY "Users can view their own history" 
    ON user_view_history FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own history" 
    ON user_view_history FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

-- Create functions for nearby locations

-- Function to get nearby locations within a radius
CREATE OR REPLACE FUNCTION get_nearby_locations(
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    radius_meters INTEGER DEFAULT 1000,
    max_results INTEGER DEFAULT 10,
    category_filter TEXT DEFAULT NULL
)
RETURNS SETOF locations
LANGUAGE SQL
STABLE
AS $$
    SELECT *
    FROM locations
    WHERE (
        category_filter IS NULL
        OR category_id = category_filter
    )
    AND ST_DWithin(
        geom,
        ST_SetSRID(ST_MakePoint(lng, lat), 4326)::geography,
        radius_meters
    )
    ORDER BY geom <-> ST_SetSRID(ST_MakePoint(lng, lat), 4326)::geography
    LIMIT max_results;
$$;