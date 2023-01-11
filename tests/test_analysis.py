import unittest, src
from src import analysis, testdata, habitclass, database



class TestAnalysisModule(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls): 
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
        self.assertEqual(self.habit_list[2].description, "Meditate daily")
        self.assertEqual(self.habit_list[3].description, "Water plants every 5 days")
        self.assertEqual(self.habit_list[4].description, "Summarize expenses monthly")

        self.assertEqual(self.habit_list[0].frequency, 2)
        self.assertEqual(self.habit_list[1].frequency, 7)
        self.assertEqual(self.habit_list[2].frequency, 1)
        self.assertEqual(self.habit_list[3].frequency, 5)
        self.assertEqual(self.habit_list[4].frequency, 30)
    
    def test_get_habit_data(self):
        for habit in self.habit_list:
            self.assertTrue(len(analysis.get_habit_data(self.test_db, habit)) > 0)

   
if __name__ == "__main__":
    unittest.main()

