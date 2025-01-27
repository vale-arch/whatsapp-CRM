-- Add role and from_allowed_ending columns to allow_list table
ALTER TABLE allow_list ADD COLUMN role VARCHAR(50) DEFAULT 'Admin';
ALTER TABLE allow_list ADD COLUMN from_allowed_ending BOOLEAN DEFAULT FALSE;