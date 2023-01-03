import time, analysis
import datetime
import copy

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
            previous_entry_date = datetime.date.fromtimestamp(habit_data[-1][1])
            current_entry_date = datetime.date.fromtimestamp(seconds_time)
            previous_streak = habit_data[-1][2]

            if current_entry_date < previous_entry_date:
                dates = []
                for entry in habit_data:
                    dates.append(entry[1])
                    
                for index, date in enumerate(dates):
                    if datetime.date.fromtimestamp(date) == current_entry_date:
                        cutoff_index = index
                        break
                    elif datetime.date.fromtimestamp(date) > current_entry_date:
                        cutoff_index = index - 1
                        break
                
                rearranged = copy.copy(habit_data[cutoff_index+1:])
                
                last_index = len(habit_data) - 1
                num_to_remove = last_index - cutoff_index
                db.delete_lastentry_for_habit(self, num_to_remove)
                
                self.check_off(db, seconds_time)
                                
                for entry in rearranged:
                    self.check_off(db, entry[1])
                
                        
            else:
                time_difference = current_entry_date - previous_entry_date

                if time_difference.days <= self.frequency:
                    self.current_streak = previous_streak + 1

                else:
                    self.current_streak = 1

                db.insert_habit_entry(self, seconds_time)
    
    """    
    Helper function for analysis.get_current_habits.
    It sets the streaks for the newly created habit objects based on the data in the database.
    """      
    def set_streak(self, db):
        habit_data = analysis.get_habit_data(db, self)
        
        #If there are no entries - set streak to zero
        if len(habit_data) == 0:
            self.current_streak = 0
            
        #otherwise set the streak to the streak of the last entry
        else:
            self.current_streak = habit_data[-1][2]
        
    def __str__(self):
        return (f"{self.name}, {self.description}, {self.frequency}, current streak: {self.current_streak}")

