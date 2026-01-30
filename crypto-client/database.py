"""
Database models and utilities for user authentication
"""
import sqlite3
import os
from datetime import datetime
from passlib.context import CryptContext
from typing import Optional, Dict
import secrets

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Database:
    """SQLite database manager for user authentication"""
    
    def __init__(self, db_path: str = None):
        """Initialize database connection"""
        if db_path is None:
            # Use /app/data in Docker, current directory otherwise
            data_dir = "/app/data" if os.path.exists("/app/data") else "."
            db_path = os.path.join(data_dir, "crypto_client_users.db")
        
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def init_db(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                is_active BOOLEAN DEFAULT 1,
                is_admin BOOLEAN DEFAULT 0,
                client_id TEXT,
                client_secret TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """)
        
        # Create sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
    
    def create_user(self, username: str, password: str, email: Optional[str] = None,
                   client_id: Optional[str] = None, client_secret: Optional[str] = None,
                   is_admin: bool = False) -> Dict:
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Truncate password to 72 bytes (bcrypt limitation)
            # This ensures compatibility with bcrypt's maximum input length
            password_bytes = password.encode('utf-8')[:72]
            password_truncated = password_bytes.decode('utf-8', errors='ignore')
            
            # Hash password
            password_hash = pwd_context.hash(password_truncated)
            
            cursor.execute("""
                INSERT INTO users (username, password_hash, email, client_id, client_secret, is_admin)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, password_hash, email, client_id, client_secret, is_admin))
            
            conn.commit()
            user_id = cursor.lastrowid
            
            print(f"✅ User created: {username} (ID: {user_id})")
            
            return {
                "id": user_id,
                "username": username,
                "email": email,
                "is_admin": is_admin
            }
        except sqlite3.IntegrityError:
            raise ValueError(f"User '{username}' already exists")
        finally:
            conn.close()
    
    def verify_user(self, username: str, password: str) -> Optional[Dict]:
        """Verify user credentials and return user data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, password_hash, email, is_active, is_admin, 
                   client_id, client_secret
            FROM users
            WHERE username = ?
        """, (username,))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return None
        
        # Truncate password to 72 bytes (bcrypt limitation)
        password_bytes = password.encode('utf-8')[:72]
        password_truncated = password_bytes.decode('utf-8', errors='ignore')
        
        # Verify password
        if not pwd_context.verify(password_truncated, user["password_hash"]):
            return None
        
        # Check if active
        if not user["is_active"]:
            return None
        
        # Update last login
        self.update_last_login(user["id"])
        
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "is_admin": bool(user["is_admin"]),
            "client_id": user["client_id"],
            "client_secret": user["client_secret"]
        }
    
    def update_last_login(self, user_id: int):
        """Update user's last login timestamp"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users
            SET last_login = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (user_id,))
        
        conn.commit()
        conn.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, is_active, is_admin, client_id, client_secret
            FROM users
            WHERE id = ?
        """, (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return None
        
        return dict(user)
    
    def create_session(self, user_id: int, expires_in_hours: int = 24) -> str:
        """Create a new session token for user"""
        from datetime import timedelta
        
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=expires_in_hours)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO sessions (user_id, session_token, expires_at)
            VALUES (?, ?, ?)
        """, (user_id, session_token, expires_at))
        
        conn.commit()
        conn.close()
        
        return session_token
    
    def verify_session(self, session_token: str) -> Optional[Dict]:
        """Verify session token and return user data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.user_id, s.expires_at, u.username, u.email, u.is_admin,
                   u.client_id, u.client_secret
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.session_token = ? AND u.is_active = 1
        """, (session_token,))
        
        session = cursor.fetchone()
        conn.close()
        
        if not session:
            return None
        
        # Check if expired
        expires_at = datetime.fromisoformat(session["expires_at"])
        if datetime.now() > expires_at:
            self.delete_session(session_token)
            return None
        
        return {
            "user_id": session["user_id"],
            "username": session["username"],
            "email": session["email"],
            "is_admin": bool(session["is_admin"]),
            "client_id": session["client_id"],
            "client_secret": session["client_secret"]
        }
    
    def delete_session(self, session_token: str):
        """Delete a session (logout)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sessions WHERE session_token = ?", (session_token,))
        
        conn.commit()
        conn.close()
    
    def cleanup_expired_sessions(self):
        """Remove all expired sessions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sessions WHERE expires_at < CURRENT_TIMESTAMP")
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        if deleted > 0:
            print(f"🧹 Cleaned up {deleted} expired sessions")


# Global database instance
db = Database()
