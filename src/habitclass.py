from src import analysis
import time, datetime, copy

class Habit:

    def __init__(self, name, description, frequency):
        self.name = name
        self.description = description
        self.frequency = frequency

    """
    The check_off method calculates the streak of a new habit entry and adds the entry to the database.
    
    For the purpose of this method, the start date of the habit is the latest date when the streak was set to 1
    (it was either started for the first time or had been broken).
    
    We can imagine blocks of {self.frequency} number of days drawn from the start date.
    
    FOR EXAMPLE:    habit has self.frequency = 7 (habit done weekly)
                    habit start date is 1 Jan
                    
                    block number 1 is the 7 days from Jan 1 to Jan 7
                    block number 2 is the 7 days from Jan 8 to Jan 14 
                    
                    Following this:
                    The date Jan 3 is in block number 1
                    The date Jan 14 is in block number 2
                    The date Jan 30 is in block number 5
    
    Keeping that in mind ,the streak is calculated as follows:
    
    - If the elapsed time in days between the current date (the date for which we are checking off the habit)
    and the previous entry date is more than the frequency, the streak is broken and set to 1.
    
    - Otherwise, if the elapsed time in days between the current and previous date is less or equal to the frequency:
        If the current entry date is in the same block as the previous entry date:
            set the streak for the same one as the previous entry (neither breaking or increasing streak)
        Else - the current entry date is on the next block from the previous entry date:
            increase the streak (set it to [previous_streak + 1])     
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
            
            """
            BACKLOGGING:
            The next if statement is the situation in which the user logs an entry from the past
            (meaning, on the date before the latest habit entry)
            
            In that situation - we 1. find the closest date before the desired date for backlogging.
            2. Copy and remove all entries after that closest date from the database.
            3. Insert the new entry (self.check_off(backlogged_date_in_seconds))
            4. Reinsert all the entries that were removed before
            """
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
                db.delete_last_no_entries_for_habit(self, num_to_remove)
                
                self.check_off(db, seconds_time)
                                
                for entry in rearranged:
                    self.check_off(db, entry[1])
               
            #Setting the actual streak    
            #See analysis.find_block_number for block number calculation for a date    
            else:
                
                elapsed_delta = current_entry_date - previous_entry_date
                                
                block_number_current = analysis.find_block_number(db, self, current_entry_date)
                block_number_previous = analysis.find_block_number(db, self, previous_entry_date)

                if (elapsed_delta.days <= self.frequency):
                    if(block_number_current == block_number_previous):
                        self.current_streak = previous_streak
                    else:
                        self.current_streak = previous_streak + 1
                else:
                    self.current_streak = 1
                                
                db.insert_habit_entry(self, seconds_time)
                
    """    
    Helper method for analysis.get_current_habits.
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

