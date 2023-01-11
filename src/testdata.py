import time, sqlite3
from src.habitclass import Habit
from src.database import DatabaseConnection

def main():
    
    test_db = DatabaseConnection("test.db")
    
    exercise = Habit("Exercise", "Go to the gym every 2 days", 2)
    clean = Habit("Clean room", "Clean your room once a week", 7)
    meditation = Habit("Meditation", "Meditate daily", 1)
    water_plants = Habit("Water plants", "Water plants every 5 days", 5)
    budget = Habit("Budget", "Summarize expenses monthly", 30)
    

    habit_list = [exercise, clean, meditation, water_plants, budget]


    #streak losses - 3
    exercise_testdates = [

    time.mktime(time.strptime("20 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("22 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("24 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("26 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("28 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("03 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("05 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("07 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("08 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("10 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("12 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("14 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("16 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("18 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("20 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("23 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("25 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("27 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("29 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("03 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("05 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("07 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("09 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("11 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("13 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("14 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("17 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("19 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("21 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("23 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("25 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("27 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    
    ]

    #streak losses -1 
    clean_room_testdates = [

    time.mktime(time.strptime("20 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("27 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("10 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("17 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("24 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("31 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("07 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("14 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("21 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("30 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),

    ]
    #streak losses - 3
    meditation_testdates = [

    time.mktime(time.strptime("20 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("21 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("22 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("23 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("24 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("25 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("26 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("27 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("28 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("01 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("02 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("03 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("04 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("06 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("07 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("08 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("09 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("10 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("11 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("12 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("13 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("14 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("15 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("16 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("18 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("19 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("20 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("21 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("22 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("23 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("24 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("25 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("26 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("27 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("27 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("28 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("30 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("31 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("01 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("02 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("03 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("04 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("04 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("05 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("06 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),


    ]

    budget_testdates = [
        
    time.mktime(time.strptime("20 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("22 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("21 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
        
    ]
    
    water_plants_testdates = [
        
    time.mktime(time.strptime("20 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("25 Feb 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("02 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("07 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("12 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("17 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("22 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("27 Mar 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("05 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("10 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("15 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("20 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("25 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    time.mktime(time.strptime("30 Apr 2023 20:15:27", "%d %b %Y %H:%M:%S")),
    
    ]
    
    try:
        for habit in habit_list:
            test_db.add_habit(habit)
            
    except sqlite3.IntegrityError:
        test_db.cursor.execute("DELETE FROM habit_list")
        test_db.cursor.execute("DELETE FROM habit_data")
        for habit in habit_list:
            test_db.add_habit(habit)


    for date in exercise_testdates:
        exercise.check_off(test_db, date)

    for date in clean_room_testdates:
        clean.check_off(test_db, date)

    for date in meditation_testdates:
        meditation.check_off(test_db, date)
        
    for date in budget_testdates:
        budget.check_off(test_db, date)
        
    for date in water_plants_testdates:
        water_plants.check_off(test_db, date)
  
if __name__ == "__main__":
    main()
