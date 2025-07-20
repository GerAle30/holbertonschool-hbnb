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

-- Create indexes for performance optimization
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_place_id ON reviews(place_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
CREATE INDEX idx_reviews_created_at ON reviews(created_at);

-- Add comments for documentation
ALTER TABLE reviews COMMENT = 'User reviews for rental places with ratings';
ALTER TABLE reviews MODIFY COLUMN id CHAR(36) COMMENT 'UUID primary key for review identification';
ALTER TABLE reviews MODIFY COLUMN text TEXT COMMENT 'Review text content written by the user';
ALTER TABLE reviews MODIFY COLUMN rating INT COMMENT 'Rating score from 1 to 5 stars';
ALTER TABLE reviews MODIFY COLUMN user_id CHAR(36) COMMENT 'UUID of the user who wrote this review';
ALTER TABLE reviews MODIFY COLUMN place_id CHAR(36) COMMENT 'UUID of the place being reviewed';
ALTER TABLE reviews MODIFY COLUMN created_at TIMESTAMP COMMENT 'Timestamp when review was created';
ALTER TABLE reviews MODIFY COLUMN updated_at TIMESTAMP COMMENT 'Timestamp when review was last updated';
