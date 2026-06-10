"""Authentication service with hardcoded secrets (BUG #2)."""
import os


class AuthService:
    """Authentication service with OBVIOUS hardcoded secrets."""
    
    # FIX: Using environment variables for secrets
    # API_KEY was not reported as an issue, but similar fix would apply.
    API_KEY = "AIzaSyDemoKey12345_THIS_IS_HARDCODED" # This line was not reported as an issue, keeping it as is per report.
    SECRET_TOKEN = os.getenv("SECRET_TOKEN", "default_secret_token_if_not_set")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "default_db_password_if_not_set")
    
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
