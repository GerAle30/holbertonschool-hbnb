-- Initial Data Insertion Script for HBnB Database
-- This script inserts the required initial data: Administrator user and initial amenities
-- Execute this after creating the database tables

-- Set SQL mode for strict operation
SET SQL_MODE = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO';

-- Disable foreign key checks temporarily (not needed for this script but good practice)
SET FOREIGN_KEY_CHECKS = 0;

-- =============================================================================
-- INSERT ADMINISTRATOR USER
-- =============================================================================

-- Insert the Administrator User with fixed UUID and bcrypt-hashed password
-- Password: admin1234 (hashed using bcrypt with 12 rounds)
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES 
('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$gcgR3rFYqYNWlyG.ntg1W.bV6LG.harP75KvOTIUnOXx8u5zhKZqS', TRUE);

-- =============================================================================
-- INSERT INITIAL AMENITIES
-- =============================================================================

-- Insert the three required initial amenities with randomly generated UUIDs
INSERT INTO amenities (id, name) VALUES
('ccaf6b6c-b86d-4dec-8a87-8a3050d1e463', 'WiFi'),
('075fd2d0-2b15-432a-862d-516366d41465', 'Swimming Pool'),
('6e59f738-be8e-40ce-9e8b-9af7d6b816db', 'Air Conditioning');

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- =============================================================================
-- VERIFY INITIAL DATA INSERTION
-- =============================================================================

-- Verify administrator user was inserted correctly
SELECT 'ADMINISTRATOR USER VERIFICATION' as Info;
SELECT 
    id,
    first_name,
    last_name,
    email,
    is_admin,
    created_at,
    'Password hash starts with: ' || LEFT(password, 10) as password_info
FROM users 
WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- Verify initial amenities were inserted correctly
SELECT 'INITIAL AMENITIES VERIFICATION' as Info;
SELECT 
    id,
    name,
    created_at
FROM amenities 
WHERE id IN (
    'ccaf6b6c-b86d-4dec-8a87-8a3050d1e463',
    '075fd2d0-2b15-432a-862d-516366d41465', 
    '6e59f738-be8e-40ce-9e8b-9af7d6b816db'
)
ORDER BY name;

-- Count total records in each table after insertion
SELECT 'RECORD COUNTS AFTER INITIAL DATA INSERTION' as Info;
SELECT 'users' as table_name, COUNT(*) as record_count FROM users
UNION ALL
SELECT 'amenities' as table_name, COUNT(*) as record_count FROM amenities
UNION ALL
SELECT 'places' as table_name, COUNT(*) as record_count FROM places
UNION ALL
SELECT 'reviews' as table_name, COUNT(*) as record_count FROM reviews
UNION ALL
SELECT 'place_amenities' as table_name, COUNT(*) as record_count FROM place_amenities;

-- Success confirmation
SELECT 'Initial data insertion completed successfully!' as Status,
       NOW() as Timestamp;
