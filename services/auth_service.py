from services.database import db
import hashlib
import re

class AuthService:
    def __init__(self):
        self.conn = db.get_connection()

    def register(self, email: str, username: str, password: str):
        hashed_password = self._hash_password(password)
        try:
            with self.conn:
                cursor = self.conn.execute(
                    'INSERT INTO users (email, username, password) VALUES (?, ?, ?)',
                    (email, username, hashed_password)
                )
                return {'user': {'id': cursor.lastrowid, 'email': email, 'username': username}}
        except sqlite3.IntegrityError:
            raise ValueError("Email already exists")

    def login(self, email: str, password: str):
        hashed_password = self._hash_password(password)
        cursor = self.conn.execute(
            'SELECT id, email, username FROM users WHERE email = ? AND password = ?',
            (email, hashed_password)
        )
        user = cursor.fetchone()
        if user:
            return {'user': {'id': user[0], 'email': user[1], 'username': user[2]}}
        raise ValueError("Invalid credentials")

    def logout(self):
        pass

    def get_current_user(self):
        pass

    @staticmethod
    def _validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def _hash_password(password: str):
        return hashlib.sha256(password.encode()).hexdigest()
