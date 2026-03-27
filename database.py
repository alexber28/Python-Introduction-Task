import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

class DatabaseManager:
    def __init__(self):
        # Use os.getenv to grab the values safely
        self.config = {
            "host": os.getenv("DB_HOST"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD")
        }
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(**self.config)
        self.conn.autocommit = True

    def select_query(self, sql):
        with self.conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()

    def insert_query(self, sql, data):
        with self.conn.cursor() as cur:
            cur.executemany(sql, data)

    def close(self):
        if self.conn:
            self.conn.close()