from src import database, habitclass, analysis
import unittest, os, datetime


class TestDatabaseClass(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        if os.path.exists('database_test.db'):
            os.remove("database_test.db")

    @classmethod
    def tearDownClass(cls):
        if os.path.exists('database_test.db'):
            os.remove("database_test.db")

    #initialize an empty database
    def setUp(self):
        self.test_db = database.DatabaseConnection("database_test.db")
        self.example_habit = habitclass.Habit("ExampleName", "ExampleDesc", 2)
        
    def tearDown(self):
        self.test_db.conn.close()

    def test_add_habit(self):
        
        self.test_db.add_habit(self.example_habit)
        self.habit_list = analysis.get_current_habits(self.test_db)

        self.assertTrue(len(self.habit_list) == 1)
    
        self.assertEqual(self.habit_list[0].name, "ExampleName")
        self.assertEqual(self.habit_list[0].description, "ExampleDesc")
        self.assertEqual(self.habit_list[0].frequency, 2)
    
    def test_insert_habit_entry(self):

        today = datetime.datetime.now()
        self.test_db.insert_habit_entry(self.example_habit, today.timestamp())

        habit_data = analysis.get_habit_data(self.test_db, self.example_habit)
        
        self.assertEqual(habit_data[0][0], "ExampleName")
        self.assertEqual(habit_data[0][1], int(today.timestamp()))
        self.assertEqual(habit_data[0][2], None)

    def test_edit_habit(self):
        
        to_be_edited = habitclass.Habit("This will be edited", "Oh no please don't edit me", 7)

        self.test_db.add_habit(to_be_edited)
        self.habit_list = analysis.get_current_habits(self.test_db)
        self.assertTrue(len(self.habit_list) == 2)
            
        self.assertEqual(self.habit_list[1].name, "This will be edited")
        self.assertEqual(self.habit_list[1].description, "Oh no please don't edit me")
        self.assertEqual(self.habit_list[1].frequency, 7)

        new_values_for_habit = ["Edited", "I guess I'm daily now :(", 1]

        self.test_db.edit_habit(to_be_edited, new_values_for_habit)

        #Have to call this function every time, as it needs to update the habit list
        self.habit_list = analysis.get_current_habits(self.test_db)
        self.assertTrue(len(self.habit_list) == 2)

        self.assertEqual(self.habit_list[1].name, "Edited")
        self.assertEqual(self.habit_list[1].description, "I guess I'm daily now :(")
        self.assertEqual(self.habit_list[1].frequency, 1)
    




if __name__ == "__main__":
    unittest.main()