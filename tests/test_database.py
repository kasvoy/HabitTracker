from src import database, habitclass, analysis
import unittest, os


class TestDatabaseClass(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        if os.path.exists('database_test.db'):
            os.remove("database_test.db")
    
    
    #initialize an empty database
    def setUp(self):
        self.test_db = database.DatabaseConnection("database_test.db")
    def tearDown(self):
        self.test_db.conn.close()
    def test_add_habit(self):
        self.example_habit = habitclass.Habit("ExampleName", "ExampleDesc", 2)
        self.test_db.add_habit(self.example_habit)
        self.test_db.cursor.execute("SELECT * FROM habit_list")

        
        

    
        
    
                
if __name__ == "__main__":
    unittest.main()