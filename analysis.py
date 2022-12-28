from habitclass import Habit
from datetime import date, timedelta, datetime



def get_longest_streak_habit(db, habit):

    db.cursor.execute("SELECT current_streak FROM habit_data WHERE habit_name = ?", (habit.name,))
    return max(db.cursor.fetchall())[0]

def get_longest_streak_all(db):

    db.cursor.execute("SELECT current_streak FROM habit_data")
    best_streak = max(db.cursor.fetchall())[0]
    db.cursor.execute("SELECT habit_name FROM habit_data WHERE current_streak = ?", (best_streak,))
    name = db.cursor.fetchone()[0]

    return [name, best_streak]

def print_habit_data(db, habit):

    for entry in get_habit_data(db, habit):
        print(f"Date: {date.fromtimestamp(entry[1])}, streak: {entry[2]}")

def get_frequencies(db):

    db.cursor.execute("SELECT frequency FROM habit_list")
    frequency_list = set()

    for entry in db.cursor.fetchall():
        frequency_list.add(entry[0])

    return frequency_list

def get_habits_with_freq(db, freq):

    db.cursor.execute("SELECT habit_name FROM habit_list WHERE frequency = ?", (freq,))
    names = []

    for entry in db.cursor.fetchall():
        names.append(entry[0])

    return names

def streakloss_in_period(db, habit, period_nodays):
    db.cursor.execute("SELECT current_streak, date FROM habit_data WHERE habit_name = ?", (habit.name,))
    results = db.cursor.fetchall()
    
    if len(results) == 0:
        return "Didn't engage in habit in the set period"

    delta = timedelta(days = period_nodays)
    
    #last_date = datetime.now() - delta
    last_date = datetime.fromtimestamp(results[-1][1]) - delta

    
    #last_date but in a unix timestamp (as stored in the database)
    last_date_seconds = int(last_date.timestamp())

    #create list with just the dates from the entries
    dates = []
    streaks = []
    for entry in results:
        dates.append(entry[1])
    
    for index, date in enumerate(dates):
        if date == last_date_seconds or date > last_date_seconds:
            cutoff_index = index
            break
    
    entries_in_period = results[cutoff_index:]
    
    for entry in entries_in_period:
        streaks.append(entry[0])
            
    no_streaklosses = 0
    
    for i in range(len(streaks) - 1):
        if (streaks[i + 1] - streaks[i]) < 0:
            no_streaklosses += 1

    return no_streaklosses

def find_most_streakloss_in_period(db, period_nodays):

    habit_list = get_current_habits(db)
    habit_streakloss = dict()
        
    for habit in habit_list:
        habit_streakloss.update({habit.name: streakloss_in_period(db, habit, period_nodays)})
    
    return habit_streakloss 

"""    
Helper function for get_current_habits.
It sets the streaks for the newly created habit objects based on the data in the database.
"""

def set_streak(db, habit):
    habit_data = get_habit_data(db, habit)

    if len(habit_data) == 0:
        habit.current_streak = 0
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

