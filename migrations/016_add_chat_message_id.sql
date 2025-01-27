-- Add id column as primary key to chat_message table
PRAGMA foreign_keys=off;
BEGIN TRANSACTION;

CREATE TABLE chat_message_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(120) NOT NULL,
    message TEXT NOT NULL,
    is_ai BOOLEAN DEFAULT FALSE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    flagged_conversation BOOLEAN DEFAULT FALSE,
    flag_reason TEXT,
    moderation_model VARCHAR(50),
    category VARCHAR(50)
);

INSERT INTO chat_message_new (user_id, message, is_ai, timestamp, flagged_conversation, flag_reason, moderation_model, category)
SELECT user_id, message, is_ai, timestamp, flagged_conversation, flag_reason, moderation_model, category FROM chat_message;

DROP TABLE chat_message;
ALTER TABLE chat_message_new RENAME TO chat_message;

COMMIT;
PRAGMA foreign_keys=on;