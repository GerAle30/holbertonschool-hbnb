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

-- Create indexes for performance optimization
CREATE INDEX idx_amenities_name ON amenities(name);

-- Add comments for documentation
ALTER TABLE amenities COMMENT = 'Available amenities that can be associated with rental places';
ALTER TABLE amenities MODIFY COLUMN id CHAR(36) COMMENT 'UUID primary key for amenity identification';
ALTER TABLE amenities MODIFY COLUMN name VARCHAR(255) COMMENT 'Unique name of the amenity (e.g., WiFi, Pool, Parking)';
ALTER TABLE amenities MODIFY COLUMN created_at TIMESTAMP COMMENT 'Timestamp when amenity was created';
ALTER TABLE amenities MODIFY COLUMN updated_at TIMESTAMP COMMENT 'Timestamp when amenity was last updated';
