-- Master SQL Script for HBnB Database Creation
-- This script creates all tables in the correct order respecting foreign key dependencies
-- Execute this script to set up the complete database schema

-- Set SQL mode and character set
SET SQL_MODE = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO';
SET NAMES utf8mb4;
SET COLLATION_CONNECTION = utf8mb4_unicode_ci;

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

-- Create User Table
-- This table stores user account information including authentication details

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

-- Create indexes for users table
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_admin ON users(is_admin);

-- =============================================================================
-- 2. CREATE AMENITY TABLE
-- =============================================================================

-- Create Amenity Table
-- This table stores available amenities that can be associated with places

CREATE TABLE amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Constraints for data validation
    CONSTRAINT chk_amenities_name_not_empty 
        CHECK (TRIM(name) != '')
);

-- Create indexes for amenities table
CREATE INDEX idx_amenities_name ON amenities(name);

-- =============================================================================
-- 3. CREATE PLACE TABLE
-- =============================================================================

-- Create Place Table
-- This table stores rental place listings with location and pricing information

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
    
    -- Foreign key constraint to users table
    CONSTRAINT fk_places_owner_id 
        FOREIGN KEY (owner_id) 
        REFERENCES users(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    -- Constraints for data validation
    CONSTRAINT chk_places_price_positive 
        CHECK (price > 0),
    CONSTRAINT chk_places_latitude_range 
        CHECK (latitude >= -90 AND latitude <= 90),
    CONSTRAINT chk_places_longitude_range 
        CHECK (longitude >= -180 AND longitude <= 180)
);

-- Create indexes for places table
CREATE INDEX idx_places_owner_id ON places(owner_id);
CREATE INDEX idx_places_price ON places(price);
CREATE INDEX idx_places_location ON places(latitude, longitude);
CREATE INDEX idx_places_title ON places(title);

-- =============================================================================
-- 4. CREATE REVIEW TABLE
-- =============================================================================

-- Create Review Table
-- This table stores user reviews for places with rating system

CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL,
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
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
    
    -- Unique constraint: one review per user per place
    CONSTRAINT uq_reviews_user_place 
        UNIQUE (user_id, place_id),
    
    -- Data validation constraints
    CONSTRAINT chk_reviews_rating_range 
        CHECK (rating >= 1 AND rating <= 5),
    CONSTRAINT chk_reviews_text_not_empty 
        CHECK (TRIM(text) != '')
);

-- Create indexes for reviews table
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_place_id ON reviews(place_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
CREATE INDEX idx_reviews_created_at ON reviews(created_at);

-- =============================================================================
-- 5. CREATE PLACE_AMENITY TABLE
-- =============================================================================

-- Create Place_Amenity Table (Junction Table)
-- This table manages the many-to-many relationship between places and amenities

CREATE TABLE place_amenities (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Composite primary key
    PRIMARY KEY (place_id, amenity_id),
    
    -- Foreign key constraints
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

-- Create indexes for place_amenities table
CREATE INDEX idx_place_amenities_place_id ON place_amenities(place_id);
CREATE INDEX idx_place_amenities_amenity_id ON place_amenities(amenity_id);

-- =============================================================================
-- VERIFY TABLE CREATION
-- =============================================================================

-- Show all created tables
SHOW TABLES;

-- Display table structures for verification
DESCRIBE users;
DESCRIBE places;
DESCRIBE reviews;
DESCRIBE amenities;
DESCRIBE place_amenities;

-- Display foreign key relationships
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM 
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE 
    REFERENCED_TABLE_NAME IS NOT NULL
    AND TABLE_SCHEMA = DATABASE()
ORDER BY 
    TABLE_NAME, COLUMN_NAME;

-- Success message
SELECT 'HBnB Database Schema Created Successfully!' as Status;
