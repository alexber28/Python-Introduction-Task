import psycopg2

class DatabaseManager:
    def __init__(self, config):
        self.config = config
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