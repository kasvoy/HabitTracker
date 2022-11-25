import sqlite3
import time
from datetime import date



conn = sqlite3.connect("database.db")


cursor = conn.cursor()

#Date entry is stored as the number of seconds since Jan 1 1970 (Unix time)
cursor.execute("""CREATE TABLE IF NOT EXISTS habit_list(
                habit_name TEXT PRIMARY KEY,
                description TEXT  
                )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS habit_data(
                habit_name TEXT,
                date integer,
                current_streak integer,
                FOREIGN KEY(habit_name) REFERENCES habit_list(habit_name)
                )""")
  
  
conn.commit()

def add_habit(name, description):
    cursor.execute("INSERT INTO habit_list VALUES (?, ?)", (name, description))
    conn.commit()

def insert_habit_entry(name, seconds_time = int(time.time())):
     
    cursor.execute("INSERT INTO habit_data VALUES (?, ?, ?)", (name, int(seconds_time), getStreak(name, seconds_time, 1)))
    conn.commit()

def get_all_info():
    
    cursor.execute("SELECT * FROM habit_data")
    return cursor.fetchall()

def get_habit_info(habit_name):
    
    cursor.execute("SELECT * FROM habit_data WHERE habit_name = ?", (habit_name,))
    return cursor.fetchall()

""""
The getStreak function returns the streak of the new entry to the habit_data table.

This function (for now) assumes the new entry has a date that is after in time compared to the previous entry.

It will return 1 if the new entry breaks the streak of [frequency]days or is during the same period.
During thhe same period means on the same day, or within the set number of days.

It will return [streak of previous entry]+1 if the new entry is on the next period determined by the frequency. 
"""
def getStreak(habit_name, habit_date, frequency):
    
    list = get_habit_info(habit_name)
    
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
    

def print_habit_info(habit_name = None):
    
    if not habit_name:
        list = get_all_info()
    
    else:
        list = get_habit_info(habit_name)
    
    for entry in list:
        
        print(f"Name of habit: {entry[0]}")
        print(f"Date of habit: {date.fromtimestamp(entry[1])}, current streak: {entry[2]}")

        
#insert_habit_entry("Exercise")
insert_habit_entry("Exercise", time.mktime(time.strptime("28 Nov 2022 22:15:27", "%d %b %Y %H:%M:%S")))


print_habit_info()


conn.close()