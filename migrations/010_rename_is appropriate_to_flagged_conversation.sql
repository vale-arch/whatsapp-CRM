-- Rename is_appropriate column to flagged_conversation in chat_message table
ALTER TABLE chat_message RENAME COLUMN is_appropriate TO flagged_conversation;

-- Update the existing data
UPDATE chat_message SET flagged_conversation = NOT flagged_conversation;

-- Add flag_reason column if it doesn't exist
PRAGMA foreign_keys=off;
BEGIN TRANSACTION;

ALTER TABLE chat_message ADD COLUMN flag_reason TEXT;

COMMIT;
PRAGMA foreign_keys=on;