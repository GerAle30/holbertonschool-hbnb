-- Sample Data Insertion Script for HBnB Database
-- This script inserts sample data into all tables with proper UUID generation
-- Execute this after creating the tables to populate the database with test data

-- Note: MySQL does not have a built-in UUID() function that generates RFC 4122 compliant UUIDs
-- For production, you should use a proper UUID library or application-level UUID generation

-- =============================================================================
-- INSERT SAMPLE USERS
-- =============================================================================

INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES
('550e8400-e29b-41d4-a716-446655440001', 'John', 'Doe', 'john.doe@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewgLj1vf0H4M4mxy', FALSE),
('550e8400-e29b-41d4-a716-446655440002', 'Jane', 'Smith', 'jane.smith@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewgLj1vf0H4M4mxy', FALSE),
('550e8400-e29b-41d4-a716-446655440003', 'Admin', 'User', 'admin@hbnb.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewgLj1vf0H4M4mxy', TRUE),
('550e8400-e29b-41d4-a716-446655440004', 'Alice', 'Johnson', 'alice.johnson@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewgLj1vf0H4M4mxy', FALSE),
('550e8400-e29b-41d4-a716-446655440005', 'Bob', 'Wilson', 'bob.wilson@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewgLj1vf0H4M4mxy', FALSE);

-- =============================================================================
-- INSERT SAMPLE AMENITIES
-- =============================================================================

INSERT INTO amenities (id, name) VALUES
('660e8400-e29b-41d4-a716-446655440001', 'WiFi'),
('660e8400-e29b-41d4-a716-446655440002', 'Swimming Pool'),
('660e8400-e29b-41d4-a716-446655440003', 'Parking'),
('660e8400-e29b-41d4-a716-446655440004', 'Gym'),
('660e8400-e29b-41d4-a716-446655440005', 'Air Conditioning'),
('660e8400-e29b-41d4-a716-446655440006', 'Kitchen'),
('660e8400-e29b-41d4-a716-446655440007', 'Laundry'),
('660e8400-e29b-41d4-a716-446655440008', 'Pet Friendly'),
('660e8400-e29b-41d4-a716-446655440009', 'Balcony'),
('660e8400-e29b-41d4-a716-446655440010', 'Hot Tub');

-- =============================================================================
-- INSERT SAMPLE PLACES
-- =============================================================================

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
('770e8400-e29b-41d4-a716-446655440001', 
 'Modern Downtown Apartment', 
 'Beautiful modern apartment in the heart of downtown with city views and all amenities.',
 150.00, 
 40.7128, 
 -74.0060, 
 '550e8400-e29b-41d4-a716-446655440001'),

('770e8400-e29b-41d4-a716-446655440002', 
 'Cozy Beach House', 
 'Charming beach house just steps from the ocean. Perfect for a relaxing getaway.',
 250.00, 
 25.7617, 
 -80.1918, 
 '550e8400-e29b-41d4-a716-446655440002'),

('770e8400-e29b-41d4-a716-446655440003', 
 'Mountain Cabin Retreat', 
 'Peaceful cabin in the mountains with stunning views and hiking trails nearby.',
 120.00, 
 39.5501, 
 -105.7821, 
 '550e8400-e29b-41d4-a716-446655440003'),

('770e8400-e29b-41d4-a716-446655440004', 
 'Luxury Penthouse Suite', 
 'High-end penthouse with premium amenities and panoramic city views.',
 400.00, 
 34.0522, 
 -118.2437, 
 '550e8400-e29b-41d4-a716-446655440004'),

('770e8400-e29b-41d4-a716-446655440005', 
 'Historic Brownstone', 
 'Charming historic brownstone in a quiet neighborhood with period features.',
 180.00, 
 42.3601, 
 -71.0589, 
 '550e8400-e29b-41d4-a716-446655440005');

-- =============================================================================
-- INSERT SAMPLE REVIEWS
-- =============================================================================

INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES
('880e8400-e29b-41d4-a716-446655440001', 
 'Amazing place! The location was perfect and the apartment was exactly as described. Would definitely stay again.',
 5, 
 '550e8400-e29b-41d4-a716-446655440002', 
 '770e8400-e29b-41d4-a716-446655440001'),

('880e8400-e29b-41d4-a716-446655440002', 
 'Great beach house with easy access to the water. The host was very responsive and helpful.',
 4, 
 '550e8400-e29b-41d4-a716-446655440001', 
 '770e8400-e29b-41d4-a716-446655440002'),

('880e8400-e29b-41d4-a716-446655440003', 
 'Beautiful mountain views and very peaceful. Perfect for a weekend getaway. Highly recommend!',
 5, 
 '550e8400-e29b-41d4-a716-446655440004', 
 '770e8400-e29b-41d4-a716-446655440003'),

('880e8400-e29b-41d4-a716-446655440004', 
 'Luxury at its finest. Every detail was perfect. Worth every penny for a special occasion.',
 5, 
 '550e8400-e29b-41d4-a716-446655440005', 
 '770e8400-e29b-41d4-a716-446655440004'),

('880e8400-e29b-41d4-a716-446655440005', 
 'Good location but the place could use some updates. Overall decent stay.',
 3, 
 '550e8400-e29b-41d4-a716-446655440003', 
 '770e8400-e29b-41d4-a716-446655440005'),

('880e8400-e29b-41d4-a716-446655440006', 
 'Clean and comfortable. Great for business travel. Would book again.',
 4, 
 '550e8400-e29b-41d4-a716-446655440002', 
 '770e8400-e29b-41d4-a716-446655440005');

-- =============================================================================
-- INSERT SAMPLE PLACE-AMENITY RELATIONSHIPS
-- =============================================================================

-- Modern Downtown Apartment amenities
INSERT INTO place_amenities (place_id, amenity_id) VALUES
('770e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440001'), -- WiFi
('770e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440003'), -- Parking
('770e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440005'), -- Air Conditioning
('770e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440006'), -- Kitchen
('770e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440009'); -- Balcony

-- Cozy Beach House amenities
INSERT INTO place_amenities (place_id, amenity_id) VALUES
('770e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440001'), -- WiFi
('770e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440002'), -- Swimming Pool
('770e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440006'), -- Kitchen
('770e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440007'), -- Laundry
('770e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440008'); -- Pet Friendly

-- Mountain Cabin Retreat amenities
INSERT INTO place_amenities (place_id, amenity_id) VALUES
('770e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440001'), -- WiFi
('770e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440006'), -- Kitchen
('770e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440010'); -- Hot Tub

-- Luxury Penthouse Suite amenities (all amenities)
INSERT INTO place_amenities (place_id, amenity_id) VALUES
('770e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440001'), -- WiFi
('770e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440002'), -- Swimming Pool
('770e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440003'), -- Parking
('770e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440004'), -- Gym
('770e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440005'), -- Air Conditioning
('770e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440006'), -- Kitchen
('770e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440007'), -- Laundry
('770e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440009'), -- Balcony
('770e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440010'); -- Hot Tub

-- Historic Brownstone amenities
INSERT INTO place_amenities (place_id, amenity_id) VALUES
('770e8400-e29b-41d4-a716-446655440005', '660e8400-e29b-41d4-a716-446655440001'), -- WiFi
('770e8400-e29b-41d4-a716-446655440005', '660e8400-e29b-41d4-a716-446655440003'), -- Parking
('770e8400-e29b-41d4-a716-446655440005', '660e8400-e29b-41d4-a716-446655440006'), -- Kitchen
('770e8400-e29b-41d4-a716-446655440005', '660e8400-e29b-41d4-a716-446655440007'); -- Laundry

-- =============================================================================
-- VERIFY SAMPLE DATA
-- =============================================================================

-- Count records in each table
SELECT 'Users' as Table_Name, COUNT(*) as Record_Count FROM users
UNION ALL
SELECT 'Places' as Table_Name, COUNT(*) as Record_Count FROM places
UNION ALL
SELECT 'Reviews' as Table_Name, COUNT(*) as Record_Count FROM reviews
UNION ALL
SELECT 'Amenities' as Table_Name, COUNT(*) as Record_Count FROM amenities
UNION ALL
SELECT 'Place_Amenities' as Table_Name, COUNT(*) as Record_Count FROM place_amenities;

-- Show sample data from each table
SELECT 'USERS TABLE' as Info;
SELECT id, first_name, last_name, email, is_admin FROM users LIMIT 3;

SELECT 'PLACES TABLE' as Info;
SELECT id, title, price, owner_id FROM places LIMIT 3;

SELECT 'REVIEWS TABLE' as Info;
SELECT id, LEFT(text, 50) as text_preview, rating, user_id, place_id FROM reviews LIMIT 3;

SELECT 'AMENITIES TABLE' as Info;
SELECT id, name FROM amenities LIMIT 5;

SELECT 'PLACE_AMENITIES RELATIONSHIPS' as Info;
SELECT 
    p.title as place_title,
    a.name as amenity_name
FROM place_amenities pa
JOIN places p ON pa.place_id = p.id
JOIN amenities a ON pa.amenity_id = a.id
LIMIT 10;

-- Success message
SELECT 'Sample data inserted successfully!' as Status;
