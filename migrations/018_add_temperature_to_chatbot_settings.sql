-- Add temperature column to chatbot_settings table
ALTER TABLE chatbot_settings ADD COLUMN temperature FLOAT DEFAULT 0.7;