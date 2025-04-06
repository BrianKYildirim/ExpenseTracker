# models/user.py
import sqlite3
import bcrypt
import re


class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def valid_password(password):
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    @staticmethod
    def create_user(db_file, username, email, password):
        if not User.valid_password(password):
            return False
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, hashed))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def get_user_by_identifier(db_file, identifier):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, password FROM users WHERE username = ? OR email = ?",
                       (identifier, identifier))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(*row)
        return None

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)