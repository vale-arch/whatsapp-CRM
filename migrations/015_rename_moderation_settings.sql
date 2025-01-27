-- Rename moderation_settings table to chatbot_settings and remove infractions_until_ban column
PRAGMA foreign_keys=off;
BEGIN TRANSACTION;

CREATE TABLE chatbot_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    moderation_prompt TEXT DEFAULT '',
    model_selection VARCHAR(50) DEFAULT 'gpt-4o'
);

INSERT INTO chatbot_settings (id, moderation_prompt, model_selection)
SELECT id, moderation_prompt, model_selection FROM moderation_settings;

DROP TABLE moderation_settings;

COMMIT;
PRAGMA foreign_keys=on;