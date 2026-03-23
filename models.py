class Room:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Student:
    def __init__(self, id, name, birthday, sex, room):
        self.id = id
        self.name = name
        self.birthday = birthday
        self.sex = sex
        self.room = room