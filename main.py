import argparse
from database import DatabaseManager
from loaders import JSONLoader
from queries import QueryRunner
from exporters import ExportFactory

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("students", help="Path to students.json")
    parser.add_argument("rooms", help="Path to rooms.json")
    parser.add_argument("format", choices=["json", "xml"], help="Output format")
    args = parser.parse_args()

    db = DatabaseManager({"host": "localhost", "database": "university_db", "user": "postgres", "password": "Sashastar28"})
    db.connect()

    # Smart Check: Only load if database is empty
    if db.select_query("SELECT COUNT(*) FROM students")[0][0] == 0:
        loader = JSONLoader()
        rooms = loader.load_rooms(args.rooms)
        #if db.select_query("SELECT COUNT(*) FROM students")[0][0] == 0:
        print("Database is empty. Starting ingestion...")
        loader = JSONLoader()
        
        # Load objects from JSON
        rooms = loader.load_rooms(args.rooms)
        students = loader.load_students(args.students)

        # Prepare data for SQL (converting objects to tuples)
        room_data = [(r.id, r.name) for r in rooms]
        student_data = [(s.id, s.name, s.birthday, s.sex, s.room_id) for s in students]

        # Raw SQL Batch Inserts
        db.insert_query("INSERT INTO rooms (id, name) VALUES (%s, %s)", room_data)
        db.insert_query(
            "INSERT INTO students (id, name, birthday, sex, room) VALUES (%s, %s, %s, %s, %s)", 
            student_data
        )
        print(f"Successfully inserted {len(room_data)} rooms and {len(student_data)} students.")
    else:
        print("Data already exists. Skipping ingestion phase.")
    
    # Run reports and export
    runner = QueryRunner(db)
    reports = runner.get_all_reports()
    ExportFactory.export(reports, args.format)

    db.close()

if __name__ == "__main__":
    main()