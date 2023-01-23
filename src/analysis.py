from . import habitclass
from datetime import date, timedelta, datetime

def find_block_number(db, habit, entry_date):
    """
    Helper function for check_off method in Habit class (habitclass.Habit). It finds on which "block" of [habit.frequency] 
    days a particular date falls on.
    Check habitclass.Habit.check_off() for more details.

    Parameters:
                db: a database.DatabaseConnection object
                habit: a habitclass.Habit object
                entry_date: a datetime.date object

    Returns:
                block_number: an integer signyfing the block number.

    """

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

    """
    A function that returns the longest run streak for a given habit.

    Parameters:
                db: a database.DatabaseConnection object
                habit: a habitclass.Habit object
    Returns:
                The longest run streak for a given habit: Integer. Returned as the first entry in a db.cursor.fetchone tuple.

    """

    db.cursor.execute("SELECT MAX(current_streak) FROM habit_data WHERE habit_name = ?", (habit.name,))
    return db.cursor.fetchone()[0]


def get_longest_streak_all(db):

    """
    A function that returns the longest run streak for all habits in the database.

    Parameters:
                db: a database.DatabaseConnection object
                habit: a habitclass.Habit object
    Returns:
                The longest run streak for all habits in the database: Integer. Returned as the first entry in a db.cursor.fetchall tuple.

    """

    db.cursor.execute("""
                    SELECT habit_name, current_streak 
                    FROM habit_data WHERE current_streak = (SELECT MAX(current_streak) FROM habit_data)
                    """)

    return db.cursor.fetchall()[0]


def get_frequencies(db):

    """
    A helper function for the below get_habits_with_freq function. It returns a list of all the different frequencies of the habits in the 
    database.

    Parameters:
                db: a database.DatabaseConnection object

    Returns:
                frequency_list: a list of integers with the frequencies of all the habits in the database.
    """

    db.cursor.execute("SELECT frequency FROM habit_list")
    frequency_list = set()

    for entry in db.cursor.fetchall():
        frequency_list.add(entry[0])

    return frequency_list

def get_habits_with_freq(db, freq):
    """
    A function that returns the names of the habits that have a frequency of the parameter [freq] (habit.frequency = freq)

    Parameters:
                db: a database.DatabaseConnection object.
                freq: Integer. Represents the frequency of a habit.

    Returns:
                names: a list of strings representing the names of the habits with the desired frequency.
    
    """

    db.cursor.execute("SELECT habit_name FROM habit_list WHERE frequency = ?", (freq,))
    names = []

    for entry in db.cursor.fetchall():
        names.append(entry[0])

    return names

def streakloss_in_period(db, habit, period_no_days):
    """
    A function that returns the number of streak losses of a particular habit in a given period.

    Parameters:
                db: a database.DatabaseConnection object.
                habit: a habitclass.Habit object.
                period_no_days: integer. The number of days from today to the past that represents the period. Example: period_no_days = 30 -> last 30 days.

    Returns:
                no_streaklosses: int. number of streak losses of a particular habit in a given period.
    """

    db.cursor.execute("SELECT current_streak, date FROM habit_data WHERE habit_name = ?", (habit.name,))
    results = db.cursor.fetchall()
    
    if len(results) == 0:
        return "Didn't engage in habit in the set period"

    delta = timedelta(days = period_no_days)

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
    for entry in results:
        streaks.append(entry[0])
    
    for index, date in enumerate(dates):
        if date == last_date_seconds or date > last_date_seconds:
            cutoff_index = index
            break
 
    no_streaklosses = 0

    if dates[cutoff_index] > last_date_seconds and streaks[cutoff_index] == 1:
        if streaks[cutoff_index - 1] > 1:
            if (datetime.fromtimestamp(dates[cutoff_index - 1]) + timedelta(days=habit.frequency)) >= last_date:
                no_streaklosses += 1
    
    entries_in_period = results[cutoff_index:]

    for i in range(len(entries_in_period) - 1):
        if (entries_in_period[i + 1][0] - entries_in_period[i][0]) < 0:
            no_streaklosses += 1

    return no_streaklosses

def find_most_streakloss_in_period(db, period_no_days):
    """
    A function that returns the habits with the most streak losses in a given period with the number of these streak losses
    thanks to the above streakloss_in_period function.

    Parameters:
                db: a database.DatabaseConnection object.
                period_no_days: int. The number of days from today to the past that represents the period. Example: period_no_days = 30 -> last 30 days.
                
    Returns:
                most_habit_streakloss: dictionary. Keys - names of habits with the most streak losses (str). Values - the streak losses (int)
    
    """
    habit_list = get_current_habits(db)
    habit_streakloss = dict()
    most_habit_streakloss = dict()
        
    for habit in habit_list:
        if streakloss_in_period(db, habit, period_no_days) != 0:
           habit_streakloss.update({habit.name: streakloss_in_period(db, habit, period_no_days)})
    
    most_streakloss_habit_names = [
    habit_names for habit_names, values in habit_streakloss.items() if values == max(habit_streakloss.values())
        ]
    
    for habit_name in most_streakloss_habit_names:
        most_habit_streakloss.update({habit_name: habit_streakloss[habit_name]})
    
    if len(most_habit_streakloss) == 0:
        return None
    
    
    return most_habit_streakloss 

def get_current_habits(db):

    """
    A function that gets all the habits currently tracked from the habit_list table of the database and packages them into habitclass.Habit objects
    for use in all other parts of the program.

    Parameters:
                db: a database.DatabaseConnection object.
            
    Returns:
                habit_obj_list: a list of habitclass.Habit objects representing all the habits in the habit_list table of the database.
    
    """
    db.cursor.execute("SELECT * FROM habit_list")
    tuples_list = db.cursor.fetchall()
    habit_obj_list = []

    #create a list of habit objects from the database representing the currently tracked habits
    for entry in tuples_list:
        habit_obj_list.append(habitclass.Habit(entry[0], entry[1], entry[2]))

    for habit in habit_obj_list:
        habit.set_streak(db)

    return habit_obj_list

def get_habit_data(db, habit):

    """
    A function that gets all the habit logs for a given habit: the habit_data table values for that habit.
    Parameters:
                db: a database.DatabaseConnection object.
                habit: a habitclass.Habit object.
            
    Returns:
                a tuple of all the habit logs for a given habit. Contains the habit name, date of check off, streak at that date.
    
    """

    db.cursor.execute("SELECT * FROM habit_data WHERE habit_name = ?", (habit.name,))
    return db.cursor.fetchall()

