import sqlite3
import time
from datetime import date

class DatabaseConnection:
    
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()

        #Date entry is stored as the number of seconds since Jan 1 1970 (Unix time)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS habit_list(
                habit_name TEXT PRIMARY KEY,
                description TEXT,
                frequency integer
                )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS habit_data(
                habit_name TEXT,
                date integer,
                current_streak integer,
                FOREIGN KEY(habit_name) REFERENCES habit_list(habit_name)
                )""")
  
  
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def add_habit(self, name, description, frequency):
        self.cursor.execute("INSERT INTO habit_list VALUES (?, ?, ?)", (name, description, frequency))
        self.conn.commit()

    def insert_habit_entry(self, name, seconds_time = int(time.time())):
    
        self.cursor.execute("SELECT frequency FROM habit_list WHERE habit_name = ?", (name,))
    
        frequency = self.cursor.fetchall()
        if len(frequency) == 0:
            print("Habit not added. Add habit first.")
            return 0

        self.cursor.execute("INSERT INTO habit_data VALUES (?, ?, ?)", (name, int(seconds_time), self.getStreak(name, seconds_time, frequency[0][0])))
        self.conn.commit()

    def delete_lastentry(self):
    
        self.cursor.execute("DELETE FROM habit_data WHERE rowid = (SELECT MAX(rowid) FROM habit_data)")
        self.conn.commit()

    def delete_habit(self, name):
    
        self.cursor.execute("DELETE FROM habit_data WHERE habit_name = ?", (name,))
        self.cursor.execute("DELETE FROM habit_list WHERE habit_name = ?", (name,))
    
        self.conn.commit()

    def get_habit_info(self, habit_name = None):
    
        if not habit_name:
            self.cursor.execute("SELECT * FROM habit_data")
        else:
            self.cursor.execute("SELECT * FROM habit_data WHERE habit_name = ?", (habit_name,))
        
        return self.cursor.fetchall()

    def get_current_habits(self):
    
        self.cursor.execute("SELECT * FROM habit_list")
        return self.cursor.fetchall()

    """"
    The getStreak function returns the streak of the new entry to the habit_data table.

    This function (for now) assumes the new entry has a date that is after in time compared to the previous entry.

    It will return 1 if the new entry breaks the streak of [frequency]days or is during the same period.
    During thhe same period means on the same day, or within the set number of days.

    It will return [streak of previous entry]+1 if the new entry is on the next period determined by the frequency. 
    """
    def getStreak(self, habit_name, habit_date, frequency):
    
        list = self.get_habit_info(habit_name)
    
        if len(list) == 0:
            return 1
    
        previous_date = date.fromtimestamp(list[-1][1])
        current_date = date.fromtimestamp(habit_date)
        current_streak = list[-1][2]
        time_difference = current_date - previous_date
    
        if time_difference.days == frequency:
            return current_streak + 1
    
        elif time_difference.days < frequency:
            return current_streak
    
        else:
            return 1
    
    def get_longest_streak(self, habit_name):
    
        self.cursor.execute("SELECT current_streak FROM habit_data WHERE habit_name = ?", (habit_name,))
        return max(self.cursor.fetchall())[0]    

    def print_habit_info(self, habit_name = None):
    
        for entry in self.get_habit_info(habit_name):
        
            print(f"Name of habit: {entry[0]}")
            print(f"Date of habit: {date.fromtimestamp(entry[1])}, current streak: {entry[2]}")


database = DatabaseConnection()

with database as db:
    #db.add_habit("Litter", "Litterbox clean", 7)
    #print(db.get_current_habits())
    db.insert_habit_entry("Exercise")
    db.print_habit_info()

database.insert_habit_entry("Exercise")
#print(database.get_current_habits())




#database.print_habit_info()    


#insert_habit_entry("Exercise", time.mktime(time.strptime("29 Nov 2022 15:15:27", "%d %b %Y %H:%M:%S")))

