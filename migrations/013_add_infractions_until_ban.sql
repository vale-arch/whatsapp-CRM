-- Add infractions_until_ban column to moderation_settings table
ALTER TABLE moderation_settings ADD COLUMN infractions_until_ban INTEGER DEFAULT 3;