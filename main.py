import sys
import time
from database import DatabaseConnection


class Habit:

    def __init__(self, name, description, frequency):
        
        self.name = name
        self.description = description
        self.frequency = frequency



db = DatabaseConnection("database.db")

with db:
    #db.add_habit("Exercise", "I want to exercise every day", 1)
    print(db.get_current_habits())
    db.insert_habit_entry("Exercise")
    #db.insert_habit_entry("Exercise", time.mktime(time.strptime("30 Nov 2022 15:15:27", "%d %b %Y %H:%M:%S")))
    db.print_habit_info()

    
