-- Add indexes to improve chat history search performance
CREATE INDEX IF NOT EXISTS idx_chat_message_user_id ON chat_message(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_message_timestamp ON chat_message(timestamp);
CREATE INDEX IF NOT EXISTS idx_chat_message_model ON chat_message(model);