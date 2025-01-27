-- Add new fields to moderation_settings table
ALTER TABLE moderation_settings ADD COLUMN content_guidelines TEXT DEFAULT '';
ALTER TABLE moderation_settings ADD COLUMN topic_restrictions TEXT DEFAULT '';

-- Add is_appropriate column to chat_message table
ALTER TABLE chat_message ADD COLUMN is_appropriate BOOLEAN DEFAULT TRUE;