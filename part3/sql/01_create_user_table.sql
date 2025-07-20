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

-- Create index on email for faster lookups
CREATE INDEX idx_users_email ON users(email);

-- Create index on is_admin for admin queries
CREATE INDEX idx_users_is_admin ON users(is_admin);

-- Add comments for documentation
ALTER TABLE users COMMENT = 'User accounts table storing authentication and profile information';
ALTER TABLE users MODIFY COLUMN id CHAR(36) COMMENT 'UUID primary key for user identification';
ALTER TABLE users MODIFY COLUMN first_name VARCHAR(255) COMMENT 'User first name';
ALTER TABLE users MODIFY COLUMN last_name VARCHAR(255) COMMENT 'User last name';
ALTER TABLE users MODIFY COLUMN email VARCHAR(255) COMMENT 'Unique email address for user authentication';
ALTER TABLE users MODIFY COLUMN password VARCHAR(255) COMMENT 'Hashed password for user authentication';
ALTER TABLE users MODIFY COLUMN is_admin BOOLEAN COMMENT 'Flag indicating if user has administrative privileges';
ALTER TABLE users MODIFY COLUMN created_at TIMESTAMP COMMENT 'Timestamp when user account was created';
ALTER TABLE users MODIFY COLUMN updated_at TIMESTAMP COMMENT 'Timestamp when user account was last updated';
