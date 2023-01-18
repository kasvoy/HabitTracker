from src.habitclass import Habit
from src import testdata, database, analysis
import unittest


class TestHabitClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls): 
        testdata.main()

    def setUp(self):
        self.test_db = database.DatabaseConnection("test.db")
        self.habit_list = analysis.get_current_habits(self.test_db)    

    def tearDown(self):
        self.test_db.conn.close()
    
    def test_check_off(self):

        #Test habit done daily
        self.test_habit = Habit("TestName", "Test Description", 1)
        self.assertEqual(self.test_habit.current_streak, None)
        

         

if __name__ == "__main__":
    unittest.main()