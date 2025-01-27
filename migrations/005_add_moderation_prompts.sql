-- Add moderation_prompt column to moderation_settings table
ALTER TABLE moderation_settings ADD COLUMN moderation_prompt TEXT DEFAULT '';