-- Add AI response fields to chat_message table
ALTER TABLE chat_message ADD COLUMN profanity_detected BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_message ADD COLUMN sensitive_topics_detected BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_message ADD COLUMN custom_banned_words_detected BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_message ADD COLUMN violence_detected BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_message ADD COLUMN adult_content_detected BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_message ADD COLUMN hate_speech_detected BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_message ADD COLUMN discrimination_detected BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_message ADD COLUMN spam_detected BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_message ADD COLUMN harassment_detected BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_message ADD COLUMN inappropriate_links_detected BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_message ADD COLUMN risk_score INTEGER DEFAULT 0;
ALTER TABLE chat_message ADD COLUMN manual_review_flag BOOLEAN DEFAULT FALSE;