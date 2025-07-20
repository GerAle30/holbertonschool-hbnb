-- Comprehensive SQL Test Script for HBnB Database
-- This script tests table creation, constraints, relationships, and CRUD operations

-- Set SQL mode for strict operation
SET SQL_MODE = 'STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO';
SET FOREIGN_KEY_CHECKS = 1;

SELECT 'HBnB Database Comprehensive Test Suite' as Test_Suite,
       'Starting table creation and CRUD operation tests' as Description,
       NOW() as Start_Time;

-- =============================================================================
-- TEST 1: TABLE CREATION AND STRUCTURE VERIFICATION
-- =============================================================================

SELECT 'TEST 1: TABLE CREATION VERIFICATION' as Test_Phase;

-- Check if all required tables exist
SELECT 'Checking table existence...' as Status;
SELECT 
    TABLE_NAME as Table_Name,
    ENGINE as Storage_Engine,
    TABLE_COLLATION as Collation
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME;

-- Verify table structures
SELECT 'Verifying table structures...' as Status;

-- Users table structure
SELECT 'USERS TABLE STRUCTURE:' as Info;
DESCRIBE users;

-- Places table structure  
SELECT 'PLACES TABLE STRUCTURE:' as Info;
DESCRIBE places;

-- Reviews table structure
SELECT 'REVIEWS TABLE STRUCTURE:' as Info;
DESCRIBE reviews;

-- Amenities table structure
SELECT 'AMENITIES TABLE STRUCTURE:' as Info;
DESCRIBE amenities;

-- Place_amenities table structure
SELECT 'PLACE_AMENITIES TABLE STRUCTURE:' as Info;
DESCRIBE place_amenities;

-- =============================================================================
-- TEST 2: CONSTRAINTS AND RELATIONSHIPS VERIFICATION
-- =============================================================================

SELECT 'TEST 2: CONSTRAINTS AND RELATIONSHIPS VERIFICATION' as Test_Phase;

-- Check foreign key constraints
SELECT 'Foreign Key Constraints:' as Info;
SELECT 
    CONSTRAINT_NAME,
    TABLE_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME,
    DELETE_RULE,
    UPDATE_RULE
FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc
JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu 
    ON rc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
WHERE rc.CONSTRAINT_SCHEMA = DATABASE()
ORDER BY TABLE_NAME, COLUMN_NAME;

-- Check unique constraints
SELECT 'Unique Constraints:' as Info;
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE CONSTRAINT_SCHEMA = DATABASE()
    AND CONSTRAINT_NAME != 'PRIMARY'
ORDER BY TABLE_NAME, COLUMN_NAME;

-- Check indexes
SELECT 'Table Indexes:' as Info;
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    COLUMN_NAME,
    NON_UNIQUE
FROM INFORMATION_SCHEMA.STATISTICS
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;

-- =============================================================================
-- TEST 3: INITIAL DATA INSERTION AND VERIFICATION
-- =============================================================================

SELECT 'TEST 3: INITIAL DATA INSERTION AND VERIFICATION' as Test_Phase;

-- Insert initial data (if not already present)
SELECT 'Inserting initial data...' as Status;

-- Check if admin user already exists
SET @admin_exists = (SELECT COUNT(*) FROM users WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1');

-- Insert admin user if not exists
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
SELECT '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', 
       '$2b$12$gcgR3rFYqYNWlyG.ntg1W.bV6LG.harP75KvOTIUnOXx8u5zhKZqS', TRUE
WHERE @admin_exists = 0;

-- Check if amenities already exist and insert if not
INSERT INTO amenities (id, name)
SELECT * FROM (
    SELECT 'ccaf6b6c-b86d-4dec-8a87-8a3050d1e463' as id, 'WiFi' as name
    UNION ALL
    SELECT '075fd2d0-2b15-432a-862d-516366d41465', 'Swimming Pool'
    UNION ALL  
    SELECT '6e59f738-be8e-40ce-9e8b-9af7d6b816db', 'Air Conditioning'
) AS new_amenities
WHERE NOT EXISTS (
    SELECT 1 FROM amenities WHERE name = new_amenities.name
);

-- Verify initial data insertion
SELECT 'Initial Data Verification:' as Status;

-- Check admin user
SELECT 'Admin User Details:' as Info;
SELECT 
    id,
    first_name,
    last_name,
    email,
    is_admin,
    LEFT(password, 10) as password_hash_start,
    created_at
FROM users 
WHERE email = 'admin@hbnb.io';

-- Verify admin user properties
SELECT 
    CASE 
        WHEN is_admin = TRUE THEN 'PASS' 
        ELSE 'FAIL' 
    END as Admin_Status_Check,
    CASE 
        WHEN password LIKE '$2b$%' THEN 'PASS' 
        ELSE 'FAIL' 
    END as Password_Hash_Check,
    CASE 
        WHEN id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1' THEN 'PASS' 
        ELSE 'FAIL' 
    END as UUID_Check
FROM users 
WHERE email = 'admin@hbnb.io';

-- Check initial amenities
SELECT 'Initial Amenities:' as Info;
SELECT id, name, created_at 
FROM amenities 
WHERE name IN ('WiFi', 'Swimming Pool', 'Air Conditioning')
ORDER BY name;

-- =============================================================================
-- TEST 4: CRUD OPERATIONS TESTING
-- =============================================================================

SELECT 'TEST 4: CRUD OPERATIONS TESTING' as Test_Phase;

-- Test INSERT operations
SELECT 'Testing INSERT operations...' as Status;

-- Insert test user
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES
('test-user-001', 'Test', 'User', 'test@example.com', 'hashed_password', FALSE);

-- Insert test amenity
INSERT INTO amenities (id, name) VALUES
('test-amenity-001', 'Test Amenity');

-- Insert test place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
('test-place-001', 'Test Place', 'A place for testing', 100.50, 40.7128, -74.0060, 'test-user-001');

-- Insert test review
INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES
('test-review-001', 'Great test place!', 5, 'test-user-001', 'test-place-001');

-- Insert place-amenity relationship
INSERT INTO place_amenities (place_id, amenity_id) VALUES
('test-place-001', 'test-amenity-001');

SELECT 'Test data inserted successfully' as Insert_Status;

-- Test SELECT operations
SELECT 'Testing SELECT operations...' as Status;

-- Count records in each table
SELECT 'Record counts after test inserts:' as Info;
SELECT 'users' as table_name, COUNT(*) as record_count FROM users
UNION ALL
SELECT 'places', COUNT(*) FROM places
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'amenities', COUNT(*) FROM amenities
UNION ALL
SELECT 'place_amenities', COUNT(*) FROM place_amenities;

-- Test relationship queries
SELECT 'Testing relationship queries...' as Status;

-- User with their places
SELECT 'User-Place relationship test:' as Info;
SELECT 
    u.email,
    u.first_name,
    u.last_name,
    p.title as place_title,
    p.price
FROM users u
JOIN places p ON u.id = p.owner_id
WHERE u.email = 'test@example.com';

-- Place with reviews
SELECT 'Place-Review relationship test:' as Info;
SELECT 
    p.title,
    r.text as review_text,
    r.rating,
    u.email as reviewer
FROM places p
JOIN reviews r ON p.id = r.place_id
JOIN users u ON r.user_id = u.id
WHERE p.id = 'test-place-001';

-- Place with amenities
SELECT 'Place-Amenity relationship test:' as Info;
SELECT 
    p.title,
    a.name as amenity_name
FROM places p
JOIN place_amenities pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
WHERE p.id = 'test-place-001';

-- Test UPDATE operations
SELECT 'Testing UPDATE operations...' as Status;

-- Update test user
UPDATE users 
SET last_name = 'UpdatedUser' 
WHERE email = 'test@example.com';

-- Update test place
UPDATE places 
SET price = 150.75, description = 'Updated test place description' 
WHERE id = 'test-place-001';

-- Update test review
UPDATE reviews 
SET rating = 4, text = 'Updated review text - still good!' 
WHERE id = 'test-review-001';

-- Update test amenity
UPDATE amenities 
SET name = 'Updated Test Amenity' 
WHERE id = 'test-amenity-001';

-- Verify updates
SELECT 'Verifying UPDATE operations:' as Status;

SELECT 'Updated user:' as Info;
SELECT first_name, last_name, email FROM users WHERE email = 'test@example.com';

SELECT 'Updated place:' as Info;
SELECT title, price, description FROM places WHERE id = 'test-place-001';

SELECT 'Updated review:' as Info;
SELECT text, rating FROM reviews WHERE id = 'test-review-001';

SELECT 'Updated amenity:' as Info;
SELECT name FROM amenities WHERE id = 'test-amenity-001';

-- =============================================================================
-- TEST 5: CONSTRAINT TESTING
-- =============================================================================

SELECT 'TEST 5: CONSTRAINT TESTING' as Test_Phase;

-- Test constraint violations (these should fail)
SELECT 'Testing constraint violations...' as Status;

-- Test unique constraint violation (should fail)
SELECT 'Testing unique email constraint...' as Test_Info;
-- This will show an error message but won't stop execution due to our error handling
INSERT IGNORE INTO users (id, first_name, last_name, email, password, is_admin) VALUES
('test-user-002', 'Another', 'User', 'test@example.com', 'password', FALSE);

-- Check if duplicate was prevented
SELECT 
    COUNT(*) as duplicate_count,
    CASE 
        WHEN COUNT(*) = 1 THEN 'PASS - Unique constraint working' 
        ELSE 'FAIL - Duplicate email allowed' 
    END as unique_constraint_test
FROM users 
WHERE email = 'test@example.com';

-- Test check constraints
SELECT 'Testing CHECK constraints...' as Test_Info;

-- Try to insert invalid price (should fail)
INSERT IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
('invalid-place', 'Invalid Place', 'Negative price test', -50.00, 40.0, -74.0, 'test-user-001');

-- Try to insert invalid rating (should fail)
INSERT IGNORE INTO reviews (id, text, rating, user_id, place_id) VALUES
('invalid-review', 'Invalid rating test', 6, 'test-user-001', 'test-place-001');

-- Try to insert invalid coordinates (should fail)
INSERT IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
('invalid-coords', 'Invalid Coordinates', 'Invalid lat/lng test', 100.00, 95.0, 200.0, 'test-user-001');

-- Verify constraints prevented invalid data
SELECT 'Constraint test results:' as Info;
SELECT 
    (SELECT COUNT(*) FROM places WHERE price <= 0) as negative_price_count,
    (SELECT COUNT(*) FROM reviews WHERE rating > 5 OR rating < 1) as invalid_rating_count,
    (SELECT COUNT(*) FROM places WHERE latitude > 90 OR latitude < -90 OR longitude > 180 OR longitude < -180) as invalid_coords_count;

-- =============================================================================
-- TEST 6: FOREIGN KEY CONSTRAINT TESTING
-- =============================================================================

SELECT 'TEST 6: FOREIGN KEY CONSTRAINT TESTING' as Test_Phase;

-- Try to insert place with non-existent owner (should fail)
INSERT IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
('orphan-place', 'Orphan Place', 'No owner test', 100.00, 40.0, -74.0, 'non-existent-user');

-- Try to insert review with non-existent user (should fail)
INSERT IGNORE INTO reviews (id, text, rating, user_id, place_id) VALUES
('orphan-review-user', 'Orphan review', 4, 'non-existent-user', 'test-place-001');

-- Try to insert review with non-existent place (should fail)
INSERT IGNORE INTO reviews (id, text, rating, user_id, place_id) VALUES
('orphan-review-place', 'Orphan review', 4, 'test-user-001', 'non-existent-place');

-- Verify foreign key constraints prevented invalid references
SELECT 'Foreign key constraint test results:' as Info;
SELECT 
    (SELECT COUNT(*) FROM places WHERE owner_id = 'non-existent-user') as orphan_places,
    (SELECT COUNT(*) FROM reviews WHERE user_id = 'non-existent-user') as orphan_reviews_user,
    (SELECT COUNT(*) FROM reviews WHERE place_id = 'non-existent-place') as orphan_reviews_place;

-- =============================================================================
-- TEST 7: CASCADE DELETE TESTING
-- =============================================================================

SELECT 'TEST 7: CASCADE DELETE TESTING' as Test_Phase;

-- Record counts before deletion
SELECT 'Counts before cascade delete test:' as Info;
SELECT 'places' as table_name, COUNT(*) as count FROM places WHERE owner_id = 'test-user-001'
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews WHERE user_id = 'test-user-001'
UNION ALL  
SELECT 'place_amenities', COUNT(*) FROM place_amenities WHERE place_id = 'test-place-001';

-- Delete test user (should cascade to places, reviews, and place_amenities)
DELETE FROM users WHERE id = 'test-user-001';

-- Verify cascade deletions
SELECT 'Counts after cascade delete test:' as Info;
SELECT 'places' as table_name, COUNT(*) as count FROM places WHERE owner_id = 'test-user-001'
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews WHERE user_id = 'test-user-001'
UNION ALL
SELECT 'place_amenities', COUNT(*) FROM place_amenities WHERE place_id = 'test-place-001';

-- Clean up remaining test data
DELETE FROM amenities WHERE id = 'test-amenity-001';

-- =============================================================================
-- TEST 8: PERFORMANCE AND INDEXING TEST
-- =============================================================================

SELECT 'TEST 8: PERFORMANCE AND INDEXING TEST' as Test_Phase;

-- Show execution plans for common queries
SELECT 'Testing query performance with indexes...' as Status;

-- Test email lookup (should use index)
EXPLAIN SELECT * FROM users WHERE email = 'admin@hbnb.io';

-- Test place owner lookup (should use foreign key index)
EXPLAIN SELECT * FROM places WHERE owner_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';

-- Test amenity name lookup (should use unique index)
EXPLAIN SELECT * FROM amenities WHERE name = 'WiFi';

-- =============================================================================
-- TEST SUMMARY AND RESULTS
-- =============================================================================

SELECT 'TEST SUMMARY AND RESULTS' as Final_Phase;

-- Final record counts
SELECT 'Final record counts:' as Summary;
SELECT 'users' as table_name, COUNT(*) as record_count FROM users
UNION ALL
SELECT 'places', COUNT(*) FROM places
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews  
UNION ALL
SELECT 'amenities', COUNT(*) FROM amenities
UNION ALL
SELECT 'place_amenities', COUNT(*) FROM place_amenities;

-- Verify admin user still exists and is correct
SELECT 'Admin user final verification:' as Summary;
SELECT 
    id,
    CONCAT(first_name, ' ', last_name) as full_name,
    email,
    is_admin,
    created_at
FROM users 
WHERE email = 'admin@hbnb.io';

-- Verify initial amenities still exist
SELECT 'Initial amenities final verification:' as Summary;
SELECT id, name, created_at 
FROM amenities 
WHERE name IN ('WiFi', 'Swimming Pool', 'Air Conditioning')
ORDER BY name;

-- Test completion message
SELECT 'HBnB Database Test Suite Completed Successfully!' as Status,
       'All tables, constraints, relationships, and CRUD operations tested' as Result,
       NOW() as Completion_Time;
