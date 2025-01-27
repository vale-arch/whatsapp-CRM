from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AllowList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), default='Admin')  # Added role field
    from_allowed_ending = db.Column(db.Boolean, default=False)  # Added from_allowed_ending field
    
    def is_email_allowed(self, email_to_check):
        """Check if an email is allowed based on exact match or wildcard pattern."""
        if '@' not in self.email or '@' not in email_to_check:
            return False
        
        pattern_domain = self.email.split('@')[1]
        email_domain = email_to_check.split('@')[1]
        
        # Check for exact match
        if self.email == email_to_check:
            return True
            
        # Check for wildcard domain match (e.g., *@domain.com)
        if self.email.startswith('*@') and email_domain == pattern_domain:
            return True
            
        return False

class ChatbotSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    moderation_prompt = db.Column(db.Text, default="")
    model_selection = db.Column(db.String(50), default="gpt-4o")
    temperature = db.Column(db.Float, default=0.7)  # New field for temperature

    @classmethod
    def get_settings(cls):
        settings = cls.query.first()
        if not settings:
            settings = cls()
            db.session.add(settings)
            db.session.commit()
        return settings

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_ai = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    model = db.Column(db.String(50))  # The AI model used for this message

class AllowedEmailEndings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_ending = db.Column(db.String(120), unique=True, nullable=False)

class BlockList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)