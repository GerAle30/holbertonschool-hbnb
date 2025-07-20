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

-- Create indexes for performance optimization
CREATE INDEX idx_place_amenities_place_id ON place_amenities(place_id);
CREATE INDEX idx_place_amenities_amenity_id ON place_amenities(amenity_id);

-- Add comments for documentation
ALTER TABLE place_amenities COMMENT = 'Junction table managing many-to-many relationship between places and amenities';
ALTER TABLE place_amenities MODIFY COLUMN place_id CHAR(36) COMMENT 'UUID of the place';
ALTER TABLE place_amenities MODIFY COLUMN amenity_id CHAR(36) COMMENT 'UUID of the amenity';
ALTER TABLE place_amenities MODIFY COLUMN created_at TIMESTAMP COMMENT 'Timestamp when association was created';
