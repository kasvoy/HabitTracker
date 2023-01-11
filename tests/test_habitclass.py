from src.habitclass import Habit
import src.testdata as testdata
import unittest


class TestHabitClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls): 
        testdata.main()

if __name__ == "__main__":
    unittest.main()