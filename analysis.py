def getStreak(db, habit_name, habit_date, frequency):

    list1 = db.get_habit_info(habit_name)

    if len(list1) == 0:
        return 1

    previous_date = date.fromtimestamp(list1[-1][1])
    current_date = date.fromtimestamp(habit_date)
    current_streak = list1[-1][2]
    time_difference = current_date - previous_date

    if time_difference.days == frequency:
        return current_streak + 1

    elif time_difference.days < frequency:
        return current_streak

    else:
        return 1

def get_longest_streak(db, habit_name):

    db.cursor.execute("SELECT current_streak FROM habit_data WHERE habit_name = ?", (habit_name,))
    return max(db.cursor.fetchall())[0]

def print_habit_info(db, habit_name = None):

    for entry in db.get_habit_info(habit_name):
        print(f"Name of habit: {entry[0]}")
        print(f"Date of habit: {date.fromtimestamp(entry[1])}, current streak: {entry[2]}")
        
def get_current_habits(db):

    db.cursor.execute("SELECT * FROM habit_list")
    return db.cursor.fetchall()
