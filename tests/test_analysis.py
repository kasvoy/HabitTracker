import unittest
from src import analysis, testdata, habitclass, database

class TestAnalysisModule(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls): 
        """Regenerate the test data before start of testing. This is what causes the tests to run slow."""
        testdata.main()
    
    def setUp(self):
        self.test_db = database.DatabaseConnection("test.db")
        self.habit_list = analysis.get_current_habits(self.test_db)    

    def tearDown(self):
        self.test_db.conn.close()
         
    def test_get_current_habits(self):  
     
        self.assertTrue(len(self.habit_list) == 5)
        
        for habit in self.habit_list:
            self.assertTrue(isinstance(habit, habitclass.Habit))
        
        self.assertEqual(self.habit_list[0].name, "Exercise")
        self.assertEqual(self.habit_list[1].name, "Clean room")
        self.assertEqual(self.habit_list[2].name, "Meditation")
        self.assertEqual(self.habit_list[3].name, "Water plants")
        self.assertEqual(self.habit_list[4].name, "Budget")
        
        self.assertEqual(self.habit_list[0].description, "Go to the gym every 2 days")
        self.assertEqual(self.habit_list[1].description, "Clean your room once a week")
        self.assertEqual(self.habit_list[2].description, "Meditate daily using Headspace")
        self.assertEqual(self.habit_list[3].description, "Water plants every week")
        self.assertEqual(self.habit_list[4].description, "Summarize expenses monthly")

        self.assertEqual(self.habit_list[0].frequency, 2)
        self.assertEqual(self.habit_list[1].frequency, 7)
        self.assertEqual(self.habit_list[2].frequency, 1)
        self.assertEqual(self.habit_list[3].frequency, 7)
        self.assertEqual(self.habit_list[4].frequency, 30)
    
    def test_get_habit_data(self):
        for habit in self.habit_list:
            self.assertTrue(len(analysis.get_habit_data(self.test_db, habit)) > 0)
    
    def test_get_habits_with_freq(self):
        habits_daily_names = ["Meditation"]
        habits_weekly_names = ["Clean room", "Water plants"]
        habits_monthly_names = ["Budget"]
        habits_every_two_names = ["Exercise"]
        
        self.assertEqual(analysis.get_habits_with_freq(self.test_db, 1), habits_daily_names)
        self.assertEqual(analysis.get_habits_with_freq(self.test_db, 7), habits_weekly_names)
        self.assertEqual(analysis.get_habits_with_freq(self.test_db, 30), habits_monthly_names)
        self.assertEqual(analysis.get_habits_with_freq(self.test_db, 2), habits_every_two_names)
    
    def test_get_longest_streak_all(self):
        self.assertEqual(analysis.get_longest_streak_all(self.test_db), ("Meditation", 17))
    
    def test_get_longest_streak_habit(self):
        self.assertEqual(analysis.get_longest_streak_habit(self.test_db, self.habit_list[0]), 9)
        self.assertEqual(analysis.get_longest_streak_habit(self.test_db, self.habit_list[1]), 7)
        self.assertEqual(analysis.get_longest_streak_habit(self.test_db, self.habit_list[2]), 17)
        self.assertEqual(analysis.get_longest_streak_habit(self.test_db, self.habit_list[3]), 8)
        self.assertEqual(analysis.get_longest_streak_habit(self.test_db, self.habit_list[4]), 3)

    #see analysis.streakloss_in_period for clarification on how this is counted in test mode.
    def test_find_most_streakloss_in_period(self):
        most_last_week = {"Exercise": 1, "Clean room": 1}
        most_last_two_weeks = {"Exercise": 2}
        most_last_month = {"Exercise": 3}
        most_last_three_months = {"Exercise": 6}

        self.assertEqual(analysis.find_most_streakloss_in_period(self.test_db, 7), most_last_week)
        self.assertEqual(analysis.find_most_streakloss_in_period(self.test_db, 14), most_last_two_weeks)
        self.assertEqual(analysis.find_most_streakloss_in_period(self.test_db, 30), most_last_month)
        self.assertEqual(analysis.find_most_streakloss_in_period(self.test_db, 90), most_last_three_months)
        
if __name__ == "__main__":
    unittest.main()

