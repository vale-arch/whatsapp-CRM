-- Rename moderation_model column to model in chat_message table
PRAGMA foreign_keys=off;
BEGIN TRANSACTION;

CREATE TABLE chat_message_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(120) NOT NULL,
    message TEXT NOT NULL,
    is_ai BOOLEAN DEFAULT FALSE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    model VARCHAR(50)
);

INSERT INTO chat_message_new (id, user_id, message, is_ai, timestamp, model)
SELECT id, user_id, message, is_ai, timestamp, moderation_model FROM chat_message;

DROP TABLE chat_message;
ALTER TABLE chat_message_new RENAME TO chat_message;

COMMIT;
PRAGMA foreign_keys=on;