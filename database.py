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

    def delete_lastentry(self):
    
        self.cursor.execute("DELETE FROM habit_data WHERE rowid = (SELECT MAX(rowid) FROM habit_data)")
        self.conn.commit()

    def delete_habit(self, habit):
    
        self.cursor.execute("DELETE FROM habit_data WHERE habit_name = ?", (habit.name,))
        self.cursor.execute("DELETE FROM habit_list WHERE habit_name = ?", (habit.name,))
    
        self.conn.commit()


if __name__ == "__main__":
    main()

    """
    with database as db:
        #db.add_habit("Litter", "Litterbox clean", 7)
        print(db.get_current_habits())
        #db.insert_habit_entry("Litter")
        db.print_habit_info()
        #db.insert_habit_entry("Litter", time.mktime(time.strptime("06 Dec 2022 15:15:27", "%d %b %Y %H:%M:%S")))
        print(db.get_longest_streak("Litter"))
    """




