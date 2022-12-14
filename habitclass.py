import time, analysis
from datetime import date
from database import DatabaseConnection

#db = DatabaseConnection("database.db")

class Habit:

    def __init__(self, name, description, frequency):
        self.name = name
        self.description = description
        self.frequency = frequency

    """"
    The check_off method assigns a new streak to the habit object as well as inserts an entry into the database.

    This method assumes the new entry has a date that is after in time compared to the previous entry.

    It will return 1 if the new entry breaks the streak of [frequency]days or is during the same period.
    During the same period means on the same day, or within the set number of days.

    It will return [streak of previous entry]+1 if the new entry is on the next period determined by the frequency.
    """

    def check_off(self, db, seconds_time = int(time.time())):

        habit_data = analysis.get_habit_data(db, self)

        if len(habit_data) == 0:
            self.current_streak = 1
            db.insert_habit_entry(self, seconds_time)

        else:
            previous_entry_date = date.fromtimestamp(habit_data[-1][1])
            current_entry_date = date.fromtimestamp(seconds_time)
            previous_streak = habit_data[-1][2]

            if current_entry_date < previous_entry_date:
                raise ValueError("Can't put in date from the past")

            time_difference = current_entry_date - previous_entry_date

            if time_difference.days == self.frequency:
                self.current_streak = previous_streak + 1

            elif time_difference.days < self.frequency:
                self.current_streak = previous_streak

            else:
                self.current_streak = 1

            db.insert_habit_entry(self, seconds_time)

    def __str__(self):
        return (f"{self.name}, {self.description}, {self.frequency}, current streak: {self.current_streak}")

