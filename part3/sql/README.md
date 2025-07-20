# HBnB Database SQL Scripts

This directory contains SQL scripts for creating and managing the HBnB (Airbnb clone) database schema.

## Files Overview

### Table Creation Scripts

1. **`00_create_all_tables.sql`** - Master script that creates all tables in the correct order
2. **`01_create_user_table.sql`** - Creates the users table with authentication fields
3. **`02_create_place_table.sql`** - Creates the places table with location and pricing data
4. **`03_create_amenity_table.sql`** - Creates the amenities table for place features
5. **`04_create_review_table.sql`** - Creates the reviews table with rating system
6. **`05_create_place_amenity_table.sql`** - Creates the junction table for place-amenity relationships

### Data Scripts

7. **`06_insert_sample_data.sql`** - Inserts sample data for testing and development

## Database Schema

### Tables and Relationships

```
users (1) -----> (*) places
  ^                   |
  |                   v
  |                (*) reviews
  |                   ^
  |                   |
  +-------------------+

places (*) -----> (*) amenities
           (via place_amenities)
```

### Table Specifications

#### Users Table
- **Purpose**: User accounts and authentication
- **Primary Key**: `id` (CHAR(36) - UUID)
- **Unique Fields**: `email`
- **Key Fields**: `first_name`, `last_name`, `email`, `password`, `is_admin`

#### Places Table  
- **Purpose**: Rental property listings
- **Primary Key**: `id` (CHAR(36) - UUID)
- **Foreign Keys**: `owner_id` → `users.id`
- **Key Fields**: `title`, `description`, `price`, `latitude`, `longitude`
- **Constraints**: Price must be positive, lat/lng within valid ranges

#### Reviews Table
- **Purpose**: User reviews and ratings
- **Primary Key**: `id` (CHAR(36) - UUID)
- **Foreign Keys**: `user_id` → `users.id`, `place_id` → `places.id`
- **Unique Constraint**: `(user_id, place_id)` - One review per user per place
- **Key Fields**: `text`, `rating` (1-5)

#### Amenities Table
- **Purpose**: Available amenities catalog
- **Primary Key**: `id` (CHAR(36) - UUID)
- **Unique Fields**: `name`
- **Key Fields**: `name`

#### Place_Amenities Table
- **Purpose**: Many-to-many relationship between places and amenities
- **Composite Primary Key**: `(place_id, amenity_id)`
- **Foreign Keys**: `place_id` → `places.id`, `amenity_id` → `amenities.id`

## Usage Instructions

### 1. Create Database Schema

**Option A: Use Master Script**
```sql
-- Execute the master script (recommended)
SOURCE /path/to/sql/00_create_all_tables.sql;
```

**Option B: Execute Individual Scripts**
```sql
-- Execute in this specific order:
SOURCE /path/to/sql/01_create_user_table.sql;
SOURCE /path/to/sql/03_create_amenity_table.sql;
SOURCE /path/to/sql/02_create_place_table.sql;
SOURCE /path/to/sql/04_create_review_table.sql;
SOURCE /path/to/sql/05_create_place_amenity_table.sql;
```

### 2. Insert Sample Data

```sql
-- Load sample data for testing
SOURCE /path/to/sql/06_insert_sample_data.sql;
```

### 3. Verify Installation

```sql
-- Check all tables were created
SHOW TABLES;

-- Verify foreign key relationships
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE REFERENCED_TABLE_NAME IS NOT NULL
    AND TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME;
```

## Key Features

### UUID Primary Keys
- All tables use CHAR(36) for UUID primary keys
- Provides globally unique identifiers
- Better for distributed systems and security

### Foreign Key Constraints
- Full referential integrity enforced
- CASCADE DELETE/UPDATE for data consistency
- Proper relationship maintenance

### Data Validation
- CHECK constraints for data ranges and formats
- UNIQUE constraints where appropriate
- NOT NULL constraints for required fields

### Performance Optimization
- Indexes on frequently queried columns
- Composite indexes for relationship lookups
- Foreign key columns automatically indexed

### Timestamps
- `created_at` and `updated_at` fields on all tables
- Automatic timestamp updates using triggers
- Audit trail for data changes

## Sample Data

The sample data includes:
- **5 Users**: Mix of regular users and 1 admin
- **5 Places**: Various property types and locations
- **6 Reviews**: Different ratings and review text
- **10 Amenities**: Common property amenities
- **25+ Place-Amenity associations**: Realistic amenity assignments

### Sample Queries

```sql
-- Find all places with WiFi
SELECT p.title, p.price 
FROM places p
JOIN place_amenities pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
WHERE a.name = 'WiFi';

-- Get average rating for each place
SELECT 
    p.title,
    AVG(r.rating) as avg_rating,
    COUNT(r.id) as review_count
FROM places p
LEFT JOIN reviews r ON p.id = r.place_id
GROUP BY p.id, p.title;

-- Find users who haven't written reviews
SELECT u.first_name, u.last_name, u.email
FROM users u
LEFT JOIN reviews r ON u.id = r.user_id
WHERE r.id IS NULL;
```

## Notes

### UUID Generation
- UUIDs in sample data are manually generated for consistency
- In production, use proper UUID libraries (Python `uuid`, Java `UUID.randomUUID()`, etc.)
- MySQL 8.0+ has `UUID()` function but it's not RFC 4122 compliant

### Password Storage
- Sample passwords are bcrypt hashed
- All sample accounts use password: `password123`
- Never store plain text passwords in production

### Decimal Precision
- Prices use DECIMAL(10,2) for exact monetary calculations
- Avoids floating point precision issues
- Maximum price: 99,999,999.99

### Geographic Coordinates
- Latitude range: -90 to +90 degrees
- Longitude range: -180 to +180 degrees
- Sample data uses real city coordinates

## Compatibility

- **MySQL 5.7+** (recommended)
- **MySQL 8.0+** (full compatibility)
- **MariaDB 10.2+** (compatible with minor syntax adjustments)

## Security Considerations

- Use parameterized queries in applications
- Implement proper authentication and authorization
- Hash passwords using strong algorithms (bcrypt, Argon2)
- Validate input data before database insertion
- Use database user accounts with minimal required privileges

## Maintenance

### Regular Tasks
- Monitor table sizes and performance
- Update statistics for query optimization  
- Review and update indexes as needed
- Backup data regularly

### Schema Updates
- Always backup before schema changes
- Test changes on development environment first
- Consider migration scripts for production updates
- Document all schema modifications
