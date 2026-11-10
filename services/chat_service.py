from services.database import db

class ChatService:
    def __init__(self):
        self.conn = db.get_connection()

    def send_message(self, user_id: int, content: str):
        with self.conn:
            # Si l'utilisateur n'est pas connecté, utiliser NULL comme user_id
            actual_user_id = user_id if user_id else None
            cursor = self.conn.execute(
                'INSERT INTO chat_messages (user_id, content) VALUES (?, ?)',
                (actual_user_id, content)
            )
            return cursor.lastrowid

    def get_messages(self):
        cursor = self.conn.execute('''
            SELECT m.id, m.content, m.created_at, 
                   COALESCE(u.username, 'Guest') as username
            FROM chat_messages m
            LEFT JOIN users u ON m.user_id = u.id
            ORDER BY m.created_at DESC
            LIMIT 50
        ''')
        return cursor.fetchall()
