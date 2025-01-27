-- Add moderation_model column to chat_message table
ALTER TABLE chat_message ADD COLUMN moderation_model VARCHAR(50);