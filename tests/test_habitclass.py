from src.habitclass import Habit
from src import testdata, database, analysis
import unittest, os
from datetime import datetime, timedelta


class TestHabitClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls): 
        #Reset the test database - see src.testdata for how it's done.
        testdata.main()
        if os.path.exists('empty.db'):
            os.remove("empty.db")

    @classmethod
    def tearDownClass(cls):
        if os.path.exists('empty.db'):
            os.remove("empty.db")

    def setUp(self):
        self.testdata_db = database.DatabaseConnection("test.db")
        self.empty_db = database.DatabaseConnection("empty.db")
        self.habit_list = analysis.get_current_habits(self.testdata_db)    

    def tearDown(self):
        self.testdata_db.conn.close()
        self.empty_db.conn.close()
    
    def test_check_off_on_empty_db(self):

        today = datetime.now()

        #Test habit done daily
        
        test_habit_daily = Habit("DailyHabit", "Daily test Description", 1)
        test_habit_weekly = Habit("WeeklyHabit", "Weekly test Description", 7)
        
        self.assertEqual(test_habit_daily.current_streak, None)
        self.assertEqual(test_habit_weekly.current_streak, None)

        self.empty_db.add_habit(test_habit_daily)
        self.empty_db.add_habit(test_habit_weekly)

        #First check off - today (whatever the date is at the time of running the test).
        test_habit_daily.check_off(self.empty_db)
        test_habit_weekly.check_off(self.empty_db)

        self.assertEqual(test_habit_daily.current_streak, 1)
        self.assertEqual(test_habit_weekly.current_streak, 1)

        #Second check off - day after for daily, week after for weekly to check streak increase.

        test_habit_daily.check_off(self.empty_db, (today + timedelta(days=1)).timestamp())
        test_habit_weekly.check_off(self.empty_db, (today + timedelta(days=7)).timestamp())

        self.assertEqual(test_habit_daily.current_streak, 2)
        self.assertEqual(test_habit_weekly.current_streak, 2)

        #Third check off - streak broken (reset to 1).

        test_habit_daily.check_off(self.empty_db, (today + timedelta(days=1) + timedelta(days=2)).timestamp())
        test_habit_weekly.check_off(self.empty_db, (today + timedelta(days=7) + timedelta(days=9)).timestamp())

        self.assertEqual(test_habit_daily.current_streak, 1)
        self.assertEqual(test_habit_weekly.current_streak, 1)
    

    def test_check_off_exercise(self):
        """
        Habit exercise from the test data - done every 2 days.
        In the test data database, the last exercise entry is logged on Apr 30 2023. The streak then is 2.
        """
        
        exercise = self.habit_list[0]
        self.assertEqual(exercise.name, "Exercise")
        self.assertEqual(exercise.frequency, 2)

        #Streak on Apr 30 2023.
        self.assertEqual(exercise.current_streak, 2)

        #Check off exercise 2 days after (on May 2) - streak increment
        exercise.check_off(self.testdata_db, datetime(2023, 5, 2).timestamp())
        self.assertEqual(exercise.current_streak, 3)

        #Check off exercise 1 day after previous check off (May 3) - streak kept but no increase
        exercise.check_off(self.testdata_db, datetime(2023, 5, 3).timestamp())
        self.assertEqual(exercise.current_streak, 3)

        #Check off exercise 1 day after previous (May 4) - streak increase because 2 days passed since May 2

        exercise.check_off(self.testdata_db, datetime(2023, 5, 4).timestamp())
        self.assertEqual(exercise.current_streak, 4)

        #Check off 3 days after previous (May 7) - streak broken (reset back to 1)

        exercise.check_off(self.testdata_db, datetime(2023, 5, 7).timestamp())
        self.assertEqual(exercise.current_streak, 1)
    

    def test_check_off_clean(self):
        """
        Habit clean room from the test data - done weekly (every 7 days).
        In the test data database, the last clean room entry is logged on Apr 30 2023. The streak then is 1.
        """
        clean = self.habit_list[1]
        self.assertEqual(clean.name, "Clean room")
        self.assertEqual(clean.frequency, 7)

        #Streak on Apr 30 2023.
        self.assertEqual(clean.current_streak, 1)

        #Check off clean 7 days after (on May 7) - streak increment
        clean.check_off(self.testdata_db, datetime(2023, 5, 7).timestamp())
        self.assertEqual(clean.current_streak, 2)

        #Check off clean 4 days after previous check off (May 11) - streak kept but no increase
        clean.check_off(self.testdata_db, datetime(2023, 5, 11).timestamp())
        self.assertEqual(clean.current_streak, 2)

        #Check off clean 1 day after previous (May 14) - streak increase because 7 days passed since May 7

        clean.check_off(self.testdata_db, datetime(2023, 5, 14).timestamp())
        self.assertEqual(clean.current_streak, 3)

        #Check off 9 days after previous (May 23) - streak broken (reset back to 1)

        clean.check_off(self.testdata_db, datetime(2023, 5, 23).timestamp())
        self.assertEqual(clean.current_streak, 1)


    def test_backlogging(self):
        """
        Testing backlogging - a situation where the user inputs a date that is previous to the last entry date.
        They might have forgotten to check off a habit which led to them losing their streak.
        In this test, an example habit done every 3 days (frequency = 3) is added to the empty testing database.
        We then check it off today (datetime.now()) and then at the dates according to increasing the streak to 4
        and then breaking it by checking it off to late. 
        """
        today = datetime.now()

        example_habit = Habit("Example", "Example descriptbion", 3)
        self.assertEqual(example_habit.current_streak, None)

        self.empty_db.add_habit(example_habit)

        example_habit.check_off(self.empty_db, today.timestamp())
        self.assertEqual(example_habit.current_streak, 1)

        #checking off the habit at the next 3 periods so the streak is increased to 4, so 3, 6 and 9 days after
        example_habit.check_off(self.empty_db, (today + timedelta(days=3)).timestamp())
        example_habit.check_off(self.empty_db, (today + timedelta(days=6)).timestamp())
        example_habit.check_off(self.empty_db, (today + timedelta(days=9)).timestamp())

        self.assertEqual(example_habit.current_streak, 4)

        #checking off the habit 5 days later - too late - streak broken (reset to 1)
        example_habit.check_off(self.empty_db, (today + timedelta(days=14)).timestamp())
        self.assertEqual(example_habit.current_streak, 1)

        #Backlogging - checking off the habit at date (today + 12 days). This increases the streak to 5.
        #That streak is then kept in the check off at date (today + 14 days). It's kept, but not increased,
        #as that entry is only 2 days after the date (today + 12 days).
        example_habit.check_off(self.empty_db, (today + timedelta(days = 12)).timestamp())
        
        #This is the streak at (today + 14 days) after checking off at the past (today + 12 days) date.
        self.assertEqual(example_habit.current_streak, 5)



if __name__ == "__main__":
    unittest.main()