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

-- Create indexes for performance optimization
CREATE INDEX idx_places_owner_id ON places(owner_id);
CREATE INDEX idx_places_price ON places(price);
CREATE INDEX idx_places_location ON places(latitude, longitude);
CREATE INDEX idx_places_title ON places(title);

-- Add comments for documentation
ALTER TABLE places COMMENT = 'Rental place listings with location and pricing details';
ALTER TABLE places MODIFY COLUMN id CHAR(36) COMMENT 'UUID primary key for place identification';
ALTER TABLE places MODIFY COLUMN title VARCHAR(255) COMMENT 'Title/name of the rental place';
ALTER TABLE places MODIFY COLUMN description TEXT COMMENT 'Detailed description of the rental place';
ALTER TABLE places MODIFY COLUMN price DECIMAL(10, 2) COMMENT 'Price per night in decimal format (max 99999999.99)';
ALTER TABLE places MODIFY COLUMN latitude FLOAT COMMENT 'Latitude coordinate (-90 to 90)';
ALTER TABLE places MODIFY COLUMN longitude FLOAT COMMENT 'Longitude coordinate (-180 to 180)';
ALTER TABLE places MODIFY COLUMN owner_id CHAR(36) COMMENT 'UUID of the user who owns this place';
ALTER TABLE places MODIFY COLUMN created_at TIMESTAMP COMMENT 'Timestamp when place was created';
ALTER TABLE places MODIFY COLUMN updated_at TIMESTAMP COMMENT 'Timestamp when place was last updated';
