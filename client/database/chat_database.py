import sqlite3
import os

class ChatDatabase:
    def __init__(self, user_id):
        os.makedirs("databases", exist_ok=True)
        self.db_path = os.path.join("databases", f"chat_user_{user_id}.db")
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER,
                receiver_id INTEGER,
                content TEXT,
                delivered INTEGER DEFAULT 1
            )
        """)
        self.conn.commit()

    def save_message(self, sender_id, receiver_id, content, delivered = 1):
        self.cursor.execute("""
            INSERT INTO messages (sender_id, receiver_id, content, delivered)
            VALUES (?, ?, ?, ?)
        """, (sender_id, receiver_id, content, delivered))
        self.conn.commit()

    def get_conversation(self, user_a, user_b):
        self.cursor.execute("""
            SELECT sender_id, receiver_id, content, delivered
            FROM messages
            WHERE (sender_id = ? AND receiver_id = ?)
                OR (sender_id = ? AND receiver_id = ?)
            ORDER BY id
        """, (user_a, user_b, user_b, user_a))
        return self.cursor.fetchall()

    def get_pendding_messages(self):
        self.cursor.execute("""
            SELECT id, sender_id, receiver_id, content
            FROM messages WHERE delivered = 0
        """)
        return self.cursor.fetchall()

    def mark_as_delivered(self, msg_id):
        self.cursor.execute("""
            UPDATE messages
            SET delivered = 1
            WHERE id = ?
        """, (msg_id,))
        self.conn.commit()

    def close(self):
            self.conn.close()