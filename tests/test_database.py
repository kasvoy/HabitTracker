from src import database, habitclass, analysis
import unittest


class TestDatabaseClass(unittest.TestCase):
    
    def setUp(self):
        self.test_db = database.DatabaseConnection("test.db")
    def tearDown(self):
        self.test_db.conn.close()
    def test_add_habit(self):
        habit = habitclass.Habit("ExampleName", "ExampleDesc", 2)
        self.test_db.add_habit(habit)
        
    
        
    
                
if __name__ == "__main__":
    unittest.main()