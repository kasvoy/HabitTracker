from . import habitclass
from datetime import date, timedelta, datetime

#Helper function for check_off method in Habit class (habitclass.Habit)
def find_block_number(db, habit, entry_date):
    
    block_number = 0
    habit_data = get_habit_data(db, habit)
    
    streaks = []
    for entry in habit_data:
        streaks.append(entry[2])
    
    last_index_streaks = len(streaks) - 1
    
    for streak in reversed(streaks):
        if streak == 1:
            cutoff_index_streaks = last_index_streaks
            break          
        last_index_streaks -= 1 

    latest_date_streak1 = date.fromtimestamp(habit_data[cutoff_index_streaks][1])

    frequency_days = timedelta(days=habit.frequency)

    while(latest_date_streak1 <= entry_date):
        latest_date_streak1 += frequency_days
        block_number += 1
    
    return block_number

def get_longest_streak_habit(db, habit):

    db.cursor.execute("SELECT MAX(current_streak) FROM habit_data WHERE habit_name = ?", (habit.name,))
    return db.cursor.fetchone()[0]

def get_longest_streak_all(db):

    db.cursor.execute("""
                    SELECT habit_name, current_streak 
                    FROM habit_data WHERE current_streak = (SELECT MAX(current_streak) FROM habit_data)
                    """)

    return db.cursor.fetchall()[0]

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
    print(habit.name, delta)
    
    """
    Since the dates in the test database are hardcoded, the results of the tests would change depending
    on when the tests are run.
    Because of this, in test mode we consider "now" to be April 30 2023 - this is the date of the last entry 
    for all predefined habits.
    When app is used in regular mode, "now" is just today's date.
    """
    
    if db.name == "test.db":
        last_date = datetime.fromtimestamp(results[-1][1]) - delta
    else:
        last_date = datetime.now() - delta
    
     
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
    
    no_streaklosses = 0
    
    if dates[cutoff_index] > last_date_seconds:
        pass
    
    entries_in_period = results[cutoff_index:]
    
    for entry in entries_in_period:
        print(entry[0])
        streaks.append(entry[0])
            
    
    
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

def get_current_habits(db):

    db.cursor.execute("SELECT * FROM habit_list")
    tuples_list = db.cursor.fetchall()
    habit_obj_list = []

    #create a list of habit objects from the database representing the currently tracked habits
    for entry in tuples_list:
        habit_obj_list.append(habitclass.Habit(entry[0], entry[1], entry[2]))

    for habit in habit_obj_list:
        habit.set_streak(db)

    return habit_obj_list

def get_habit_data(db,  habit):

    db.cursor.execute("SELECT * FROM habit_data WHERE habit_name = ?", (habit.name,))
    return db.cursor.fetchall()

