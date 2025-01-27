-- Add moderation_model column to chat_message table if it doesn't exist
PRAGMA foreign_keys=off;
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS chat_message_temp AS SELECT * FROM chat_message;
DROP TABLE chat_message;
CREATE TABLE chat_message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(120) NOT NULL,
    message TEXT NOT NULL,
    is_ai BOOLEAN DEFAULT FALSE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    flagged_conversation BOOLEAN DEFAULT FALSE,
    flag_reason TEXT,
    moderation_model VARCHAR(50)
);
INSERT INTO chat_message (id, user_id, message, is_ai, timestamp, flagged_conversation, flag_reason, moderation_model)
SELECT id, user_id, message, is_ai, timestamp, flagged_conversation, flag_reason, NULL FROM chat_message_temp;
DROP TABLE chat_message_temp;

COMMIT;
PRAGMA foreign_keys=on;