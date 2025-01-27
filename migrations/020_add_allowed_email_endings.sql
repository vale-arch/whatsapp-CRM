-- Add allowed_email_endings table
CREATE TABLE IF NOT EXISTS allowed_email_endings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_ending VARCHAR(120) UNIQUE NOT NULL
);