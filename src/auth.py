"""Authentication service with hardcoded secrets (BUG #2)."""


import os

class AuthService:
    """Authentication service with OBVIOUS hardcoded secrets."""
    
    # FIX: Hardcoded secrets replaced with environment variables.
    # It's crucial to set these environment variables securely in production.
    API_KEY = os.getenv("API_KEY", "default_api_key_for_dev")
    SECRET_TOKEN = os.getenv("SECRET_TOKEN", "default_secret_token_for_dev")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "default_db_password_for_dev")
    
    def authenticate(self, token: str) -> bool:
        """Authenticate a user token.
        
        BUG #2: Uses hardcoded secret for comparison!
        """
        return token == self.SECRET_TOKEN
    
    def get_api_key(self) -> str:
        """Get API key.
        
        BUG #2: Returns hardcoded API key!
        """
        return self.API_KEY
    
    def connect_to_database(self) -> str:
        """Get database connection string.
        
        BUG #2: Uses hardcoded password!
        """
        return f"postgresql://admin:{self.DATABASE_PASSWORD}@localhost/mydb"
