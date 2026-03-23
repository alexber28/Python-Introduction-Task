class QueryRunner:
    def __init__(self, db):
        self.db = db

    def get_all_reports(self):
        return {
            "1_students_per_room": self.db.select_query("""
                SELECT r.name, COUNT(s.id) as count 
                FROM rooms r LEFT JOIN students s ON r.id = s.room 
                GROUP BY r.name"""),
            "2_top_5_youngest": self.db.select_query("""
                SELECT r.name, ROUND(AVG(EXTRACT(YEAR FROM AGE(NOW(), s.birthday))), 2) as avg_age
                FROM rooms r JOIN students s ON r.id = s.room
                GROUP BY r.name ORDER BY avg_age ASC LIMIT 5"""),
            "3_top_5_age_diff": self.db.select_query("""
                SELECT r.name, MAX(s.birthday) - MIN(s.birthday) as diff
                FROM rooms r JOIN students s ON r.id = s.room
                GROUP BY r.name ORDER BY diff DESC LIMIT 5"""),
            "4_mixed_gender": self.db.select_query("""
                SELECT r.name FROM rooms r JOIN students s ON r.id = s.room
                GROUP BY r.name HAVING COUNT(DISTINCT s.sex) > 1""")
        }