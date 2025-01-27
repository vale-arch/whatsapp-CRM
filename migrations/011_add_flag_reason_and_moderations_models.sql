-- Add flag_reason and moderation_model columns to chat_message table if they don't exist
PRAGMA foreign_keys=off;
BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS chat_message_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(120) NOT NULL,
    message TEXT NOT NULL,
    is_ai BOOLEAN DEFAULT FALSE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    flagged_conversation BOOLEAN DEFAULT FALSE,
    flag_reason TEXT,
    moderation_model VARCHAR(50)
);

INSERT INTO chat_message_new (id, user_id, message, is_ai, timestamp, flagged_conversation)
SELECT id, user_id, message, is_ai, timestamp, flagged_conversation FROM chat_message;

DROP TABLE chat_message;
ALTER TABLE chat_message_new RENAME TO chat_message;

COMMIT;
PRAGMA foreign_keys=on;