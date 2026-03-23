import json
from models import Room, Student

class JSONLoader:
    def load_rooms(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
            return [Room(r['id'], r['name']) for r in data]

    def load_students(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
            return [Student(s['id'], s['name'], s['birthday'], s['sex'], s['room']) for s in data]