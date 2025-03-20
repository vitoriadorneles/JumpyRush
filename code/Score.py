import os
import sqlite3


class Score:
    def __init__(self):
        """Initialize the database connection and ensure the scores table exists."""
        self.db_file = os.path.join(os.path.dirname(__file__), 'scores.db')  # Path to SQLite database
        self.create_table()  # Ensure the scores table exists

    def create_table(self):
        """Create the scores table in the database if it does not exist."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score INTEGER NOT NULL,
                game_time REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save_score(self, score: int, game_time: float):
        """Insert a new score into the database."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO scores (score, game_time) VALUES (?, ?)', (score, game_time))
            conn.commit()
            conn.close()
            print(f"[DEBUG] Score saved to database: {score}, time: {game_time:.1f}s")
        except Exception as e:
            print(f"[ERROR] Failed to save score: {e}")

    def load_scores(self, limit: int = 3):
        """Fetch the most recent scores from the database."""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(f'SELECT score, game_time FROM scores ORDER BY id DESC LIMIT {limit}')
            scores = cursor.fetchall()
            conn.close()
            print(f"[DEBUG] Scores fetched from database: {scores}")
            return scores
        except Exception as e:
            print(f"[ERROR] Failed to load scores: {e}")
            return []
