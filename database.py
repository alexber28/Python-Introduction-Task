import psycopg2

class DatabaseManager:
    def __init__(self, db_config):
        self.config = db_config
        self.conn = None

    def connect(self):
        """Creates a connection to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(**self.config)
            print("Connected to the database successfully!")
        except Exception as e:
            print(f"Error connecting to database: {e}")
    
    def select_query(self, query):
        """Executes a query and returns the results (for SELECT statements)."""
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            # This returns the data as a list of tuples
            return cursor.fetchall()

    def execute_query(self, query, params=None):
        """Executes a single query (like CREATE TABLE)."""
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            self.conn.commit()

    def insert_many(self, query, data_list):
        """Inserts a list of tuples into the database in one go."""
        try:
            with self.conn.cursor() as cursor:
                # executemany is much faster for large datasets
                cursor.executemany(query, data_list)
                self.conn.commit()
                print(f"Successfully inserted {len(data_list)} rows.")
        except Exception as e:
            self.conn.rollback() # Undo changes if something goes wrong
            print(f"Error during batch insert: {e}")

    def close(self):
        if self.conn:
            self.conn.close()