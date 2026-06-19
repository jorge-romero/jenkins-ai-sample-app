"""Authentication service with hardcoded secrets (BUG #2)."""
import os


class AuthService:
    """Authentication service with OBVIOUS hardcoded secrets."""
    
    # FIX #2: Replaced hardcoded secrets with environment variables.
    # API_KEY is still hardcoded as it was not explicitly reported by line number in the issues.
    API_KEY = "AIzaSyDemoKey12345_THIS_IS_HARDCODED"
    SECRET_TOKEN = os.getenv('APP_SECRET_TOKEN', 'default-secret-token-for-dev')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'default-db-password-for-dev')
    
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
