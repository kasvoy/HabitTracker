from habitclass import Habit
from datetime import date


def get_longest_streak(db, habit):

    db.cursor.execute("SELECT current_streak FROM habit_data WHERE habit_name = ?", (habit.name,))
    return max(db.cursor.fetchall())[0]

def print_habit_data(db, habit):

    for entry in get_habit_data(db, habit):
        print(f"Date: {date.fromtimestamp(entry[1])}, streak: {entry[2]}")


#Helper function for get_current_habits. It sets the streaks for the newly created habit objects

def set_streak(db, habit):
    habit_data = get_habit_data(db, habit)

    if len(habit_data) == 0:
        habit.current_streak = 1
    else:
        habit.current_streak = habit_data[-1][2]

def get_current_habits(db):

    db.cursor.execute("SELECT * FROM habit_list")
    tuples_list = db.cursor.fetchall()
    habit_obj_list = []

    #create a list of habit objects from the database representing the currently tracked habits
    for entry in tuples_list:
        habit_obj_list.append(Habit(entry[0], entry[1], entry[2]))

    for habit in habit_obj_list:
        set_streak(db, habit)

    return habit_obj_list

def get_habit_data(db, habit):

    db.cursor.execute("SELECT * FROM habit_data WHERE habit_name = ?", (habit.name,))
    return db.cursor.fetchall()
