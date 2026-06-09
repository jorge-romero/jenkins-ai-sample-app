"""Database module with SQL injection vulnerability (BUG #1)."""
import sqlite3
from typing import Optional, Dict, Any


class UserDatabase:
    """User database with OBVIOUS SQL injection vulnerability."""
    
    def __init__(self):
        """Initialize in-memory database."""
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        self._create_tables()
        self._seed_data()
    
    def _create_tables(self):
        """Create users table."""
        self.conn.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        self.conn.commit()
    
    def _seed_data(self):
        """Add sample data."""
        self.conn.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
        self.conn.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
        self.conn.commit()
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID.
        
        BUG #1: SQL INJECTION VULNERABILITY
        This uses string formatting instead of parameterized queries!
        """
        # VULNERABLE CODE - DO NOT USE IN PRODUCTION!
        query = "SELECT * FROM users WHERE id = ?"
        cursor = self.conn.execute(query, (user_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'email': row[2]
            }
        return None
    
    def create_user(self, name: str, email: str) -> int:
        """Create a new user."""
        cursor = self.conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )
        self.conn.commit()
        return cursor.lastrowid
