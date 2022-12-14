import sqlite3


class DatabaseConnection:
    
    def __init__(self, name):
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()

        #Date entry is stored as the number of seconds since Jan 1 1970 (Unix time)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS habit_list(
                habit_name TEXT PRIMARY KEY,
                description TEXT,
                frequency integer
                )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS habit_data(
                habit_name TEXT,
                date integer,
                current_streak integer,
                FOREIGN KEY(habit_name) REFERENCES habit_list(habit_name)
                )""")

        self.conn.commit()


    def add_habit(self, habit):
        self.cursor.execute("INSERT INTO habit_list VALUES (?, ?, ?)", (habit.name, habit.description, habit.frequency))
        self.conn.commit()

    def insert_habit_entry(self, habit, seconds_time):

        self.cursor.execute("INSERT INTO habit_data VALUES (?, ?, ?)", (habit.name, int(seconds_time), habit.current_streak))
        self.conn.commit()

    def delete_last_no_entries_for_habit(self, habit, num_to_remove):
        self.cursor.execute("DELETE FROM habit_data WHERE habit_name = ? ORDER BY date DESC LIMIT ?", (habit.name, num_to_remove))
        self.conn.commit()

    def delete_habit(self, habit):
    
        self.cursor.execute("DELETE FROM habit_data WHERE habit_name = ?", (habit.name,))
        self.cursor.execute("DELETE FROM habit_list WHERE habit_name = ?", (habit.name,))
    
        self.conn.commit()
    
    def edit_habit(self, habit, new_values):
        
        new_name = new_values[0]
        new_description = new_values[1]
        new_frequency = new_values[2]
        
        
        self.cursor.execute("""UPDATE habit_list 
                            SET habit_name = :new_name,
                                description = :new_description,
                                frequency = :new_frequency
                            WHERE habit_name = :current_name
                            """, {'new_name': new_name, 'new_description': new_description, 'new_frequency': new_frequency,
                                  'current_name': habit.name})
        
        self.cursor.execute("""UPDATE habit_data 
                            SET habit_name = :new_name
                            WHERE habit_name = :current_name
                            """, {'new_name': new_name, 'current_name': habit.name})
        
        
        self.conn.commit()