from database import DatabaseManager
from loaders import JSONLoader

def main():
    # 1. Database Configuration (Update with your actual password!)
    db_config = {
        "host": "localhost",
        "database": "university_db", 
        "user": "postgres",
        "password": "Sashastar28"
    }

    db = DatabaseManager(db_config)
    db.connect()

    loader = JSONLoader()

    # 2. Load and Insert Rooms
    rooms_raw = loader.load("data/rooms.json")
    # Convert list of dicts to list of tuples: (id, name)
    rooms_to_insert = [(r['id'], r['name']) for r in rooms_raw]
    
    room_query = "INSERT INTO rooms (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING"
    # db.insert_many(room_query, rooms_to_insert) - inserting into DB

    # 3. Load and Insert Students
    students_raw = loader.load("data/students.json")
    # Convert to tuples: (id, name, birthday, sex, room_id) git config --global user.email "you@example.com"
    # Note: we map 'room' from JSON to 'room_id' for SQL
    students_to_insert = [
        (s['id'], s['name'], s['birthday'], s['sex'], s['room']) 
        for s in students_raw
    ]

    student_query = """
        INSERT INTO students (id, name, birthday, sex, room) 
        VALUES (%s, %s, %s, %s, %s) 
        ON CONFLICT (id) DO NOTHING
    """
    # db.insert_many(student_query, students_to_insert)

    db.close()

if __name__ == "__main__":
    main()