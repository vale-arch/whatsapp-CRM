-- Add moderation settings table
CREATE TABLE IF NOT EXISTS moderation_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    max_message_length INTEGER DEFAULT 1000
);

-- Insert default settings if the table is empty
INSERT OR IGNORE INTO moderation_settings (id, max_message_length)
VALUES (1, 1000);