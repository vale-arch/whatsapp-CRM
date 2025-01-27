-- Add model_selection column to moderation_settings table
ALTER TABLE moderation_settings ADD COLUMN model_selection VARCHAR(50) DEFAULT 'gpt-4o';

-- Remove unused columns from moderation_settings table
PRAGMA foreign_keys=off;

CREATE TABLE moderation_settings_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    moderation_prompt TEXT DEFAULT '',
    model_selection VARCHAR(50) DEFAULT 'gpt-4o'
);

INSERT INTO moderation_settings_new (id, moderation_prompt, model_selection)
SELECT id, moderation_prompt, model_selection FROM moderation_settings;

DROP TABLE moderation_settings;
ALTER TABLE moderation_settings_new RENAME TO moderation_settings;

PRAGMA foreign_keys=on;