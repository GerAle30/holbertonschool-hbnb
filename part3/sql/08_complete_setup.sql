-- Complete Database Setup Script for HBnB
-- This script creates all tables and inserts the required initial data
-- Execute this script to set up the complete database with initial data

-- Set SQL mode and character set for consistent operation
SET SQL_MODE = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO';
SET NAMES utf8mb4;
SET COLLATION_CONNECTION = utf8mb4_unicode_ci;

-- Display setup information
SELECT 'HBnB Database Complete Setup' as Info,
       'Creating tables and inserting initial data' as Description,
       NOW() as Start_Time;

-- Disable foreign key checks temporarily to avoid dependency issues during creation
SET FOREIGN_KEY_CHECKS = 0;

-- Drop tables if they exist (in reverse order of creation)
DROP TABLE IF EXISTS place_amenities;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- =============================================================================
-- 1. CREATE USER TABLE
-- =============================================================================

CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_admin ON users(is_admin);

-- =============================================================================
-- 2. CREATE AMENITY TABLE
-- =============================================================================

CREATE TABLE amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_amenities_name_not_empty CHECK (TRIM(name) != '')
);

CREATE INDEX idx_amenities_name ON amenities(name);

-- =============================================================================
-- 3. CREATE PLACE TABLE
-- =============================================================================

CREATE TABLE places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_places_owner_id 
        FOREIGN KEY (owner_id) 
        REFERENCES users(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    CONSTRAINT chk_places_price_positive CHECK (price > 0),
    CONSTRAINT chk_places_latitude_range CHECK (latitude >= -90 AND latitude <= 90),
    CONSTRAINT chk_places_longitude_range CHECK (longitude >= -180 AND longitude <= 180)
);

CREATE INDEX idx_places_owner_id ON places(owner_id);
CREATE INDEX idx_places_price ON places(price);
CREATE INDEX idx_places_location ON places(latitude, longitude);
CREATE INDEX idx_places_title ON places(title);

-- =============================================================================
-- 4. CREATE REVIEW TABLE
-- =============================================================================

CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL,
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_reviews_user_id 
        FOREIGN KEY (user_id) 
        REFERENCES users(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_reviews_place_id 
        FOREIGN KEY (place_id) 
        REFERENCES places(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    CONSTRAINT uq_reviews_user_place UNIQUE (user_id, place_id),
    CONSTRAINT chk_reviews_rating_range CHECK (rating >= 1 AND rating <= 5),
    CONSTRAINT chk_reviews_text_not_empty CHECK (TRIM(text) != '')
);

CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_place_id ON reviews(place_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
CREATE INDEX idx_reviews_created_at ON reviews(created_at);

-- =============================================================================
-- 5. CREATE PLACE_AMENITY TABLE
-- =============================================================================

CREATE TABLE place_amenities (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (place_id, amenity_id),
    
    CONSTRAINT fk_place_amenities_place_id 
        FOREIGN KEY (place_id) 
        REFERENCES places(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    CONSTRAINT fk_place_amenities_amenity_id 
        FOREIGN KEY (amenity_id) 
        REFERENCES amenities(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

CREATE INDEX idx_place_amenities_place_id ON place_amenities(place_id);
CREATE INDEX idx_place_amenities_amenity_id ON place_amenities(amenity_id);

-- Display table creation completion
SELECT 'Database tables created successfully' as Status,
       'Proceeding to insert initial data' as Next_Step;

-- =============================================================================
-- 6. INSERT INITIAL DATA
-- =============================================================================

-- Insert Administrator User (Fixed UUID as specified)
-- Password: admin1234 (bcrypt hashed with 12 rounds)
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES 
('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$gcgR3rFYqYNWlyG.ntg1W.bV6LG.harP75KvOTIUnOXx8u5zhKZqS', TRUE);

-- Insert Initial Amenities (Generated UUIDs)
INSERT INTO amenities (id, name) VALUES
('ccaf6b6c-b86d-4dec-8a87-8a3050d1e463', 'WiFi'),
('075fd2d0-2b15-432a-862d-516366d41465', 'Swimming Pool'),
('6e59f738-be8e-40ce-9e8b-9af7d6b816db', 'Air Conditioning');

-- =============================================================================
-- 7. VERIFICATION AND SUMMARY
-- =============================================================================

-- Show all created tables
SELECT 'CREATED TABLES' as Info;
SHOW TABLES;

-- Verify initial data insertion
SELECT 'INITIAL DATA VERIFICATION' as Info;

-- Check administrator user
SELECT 'Administrator User:' as Type,
       id, first_name, last_name, email, is_admin, created_at
FROM users 
WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- Check initial amenities
SELECT 'Initial Amenities:' as Type,
       id, name, created_at
FROM amenities 
WHERE id IN (
    'ccaf6b6c-b86d-4dec-8a87-8a3050d1e463',
    '075fd2d0-2b15-432a-862d-516366d41465',
    '6e59f738-be8e-40ce-9e8b-9af7d6b816db'
)
ORDER BY name;

-- Display record counts
SELECT 'RECORD COUNTS' as Info;
SELECT 'users' as table_name, COUNT(*) as record_count FROM users
UNION ALL
SELECT 'amenities' as table_name, COUNT(*) as record_count FROM amenities
UNION ALL
SELECT 'places' as table_name, COUNT(*) as record_count FROM places
UNION ALL
SELECT 'reviews' as table_name, COUNT(*) as record_count FROM reviews
UNION ALL
SELECT 'place_amenities' as table_name, COUNT(*) as record_count FROM place_amenities
ORDER BY table_name;

-- Display foreign key relationships
SELECT 'FOREIGN KEY RELATIONSHIPS' as Info;
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE REFERENCED_TABLE_NAME IS NOT NULL
    AND TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME, COLUMN_NAME;

-- Final success message
SELECT 'HBnB Database Setup Completed Successfully!' as Status,
       'Admin credentials: admin@hbnb.io / admin1234' as Login_Info,
       '3 initial amenities created' as Amenities_Info,
       NOW() as Completion_Time;
