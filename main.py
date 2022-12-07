import sys, subprocess
import time
import analysis
from datetime import date
from database import DatabaseConnection

database = DatabaseConnection("database.db")

class Habit:

    def __init__(self, name, description, frequency):
        self.name = name
        self.description = description
        self.frequency = frequency

        with database as db:
            entry_list = analysis.get_habit_data(db, self)

        self.current_streak = entry_list[-1][2]


    """"
    The check_off method assigns a new streak to the habit object as well as inserts an entry into the database.

    This method assumes the new entry has a date that is after in time compared to the previous entry.

    It will return 1 if the new entry breaks the streak of [frequency]days or is during the same period.
    During the same period means on the same day, or within the set number of days.

    It will return [streak of previous entry]+1 if the new entry is on the next period determined by the frequency.
    """

    def check_off(self, seconds_time = int(time.time())):

        with database as db:
            list1 = analysis.get_habit_data(db, self)

        if len(list1) == 0:
            self.current_streak = 1

        else:
            previous_entry_date = date.fromtimestamp(list1[-1][1])
            current_entry_date = date.fromtimestamp(seconds_time)
            previous_streak = list1[-1][2]

            if current_entry_date < previous_entry_date:
                raise ValueError("Can't put in date from the past")

            time_difference = current_entry_date - previous_entry_date

            if time_difference.days == self.frequency:
                self.current_streak = previous_streak + 1

            elif time_difference.days < self.frequency:
                self.current_streak = previous_streak

            else:
                self.current_streak = 1

        with database as db:
            db.insert_habit_entry(self, seconds_time)


def main_menu():
    subprocess.run("clear", shell = True)
    print("\033[95m🐍HABIT PYTRACKER V.ALPHA 1.2.🐍\033[0m")
    print(" 1. Check off habit. \n 2. Add new habit. \n 3. Track and edit current habits \n 4. Quit program")


    option = get_num_option([1,2,3,4])

    if option == 1:
        check_off_menu()

    elif option == 2:
        add_habit_menu()

    elif option == 3:
        tracking_menu()

    if option == 4:
        print("Program quit")
        database.conn.close()
        sys.exit()


def check_off_menu():
    subprocess.run("clear", shell = True)
    print("\033[1mCHECK OFF HABIT - NEW HABIT ENTRY\033[0m")
    print("\nWhich habit do you want to check off?")

    with database as db:
        habit_list = analysis.get_current_habits(db)

    if len(habit_list) == 0:
        subprocess.run("clear", shell = True)
        print("You are not currently tracking any habits. ")
        print(" 1. Add habit. \n 2. Main menu")
        option = get_num_option([1,2])

        if option == 1:
            add_habit_menu()
        elif option == 2:
            main_menu()

    for i in range(len(habit_list)):
        print(f"{i+1}. {habit_list[i].name}")

    option = get_num_option([1, len(habit_list)])
    tracked_habit = habit_list[option - 1]


    tracked_habit.check_off()

    print(f"Habit checked off! Current streak for {tracked_habit.name}: {tracked_habit.current_streak}")


def add_habit_menu():
    subprocess.run("clear", shell = True)
    print("ADD NEW HABIT")

    habit_name = input("Create habit name: ")
    description = input("Set a description for your habit: ")
    frequency = input("Set frequency (in number of days): ")

    habit = Habit(habit_name, description, frequency)

    while(not frequency.isdigit() or (frequency.isdigit() and int(frequency) < 1)):
        frequency = input("Frequency must be a positive integer: ")

    with database as db:
        db.add_habit(habit)

    subprocess.run("clear", shell = True)
    print("Habit added!")
    print(" 1. Check off habit. \n 2. Main menu")

    option = get_num_option([1,2])

    if option == 1:
        check_off_menu()

    elif option == 2:
        main_menu()


def tracking_menu():

    subprocess.run("clear", shell = True)
    print("TRACKING YOUR HABITS")

    print(" 1. Show all of my habits. \n 2. Track habit")

    option = get_num_option([1,2])

    if option == 1:
        with database as db:
            habit_list = analysis.get_current_habits(db)

        if len(habit_list) == 0:
            subprocess.run("clear", shell = True)
            print("You are not currently tracking any habits. ")
            print(" 1. Add habit. \n 2. Main menu")
            option = get_num_option([1,2])

            if option == 1:
                add_habit_menu()
            elif option == 2:
                main_menu()

        for habit in habit_list:
            print('\033[1m',habit.name.upper(),'\033[0m')
            print(f"Description: {habit.description}")

            if habit.frequency == 1:
                print("Frequency: Done every day")
            else:
                print(f"Frequency: Done every {habit.frequency} days")

        print("\n 1. Track habit. \n 2. Main menu")
        option = get_num_option([1,2])

        if option == 1:
            tracking_choice_menu()

        elif option == 2:
            main_menu()

    elif option == 2:
        tracking_choice_menu()


def tracking_choice_menu():
    subprocess.run("clear", shell = True)
    print("Which of your habits would you like to track?")
    with database as db:
        habit_list = analysis.get_current_habits(db)

    for i in range(len(habit_list)):
        print(f"{i+1}. {habit_list[i].name}")

    option = get_num_option([1, len(habit_list)])
    habit = habit_list[option-1]

    indiv_habit_tracking_menu(habit)

"""
Functionalities related to tracking individual habits (streak info etc).
"""

def indiv_habit_tracking_menu(habit):
    subprocess.run("clear", shell = True)
    print(f"Habit: {habit.name}. Current streak: {habit.current_streak}\n")

    print(f" 1. Show all entries for {habit.name}. \n 2. What was my longest streak for {habit.name}")

    option = get_num_option([1, 2])

    if option == 1:
        with database as db:
            analysis.print_habit_data(db, habit)

    if option == 2:
        with database as db:
            print(f"Your best streak for {habit.name} is {analysis.get_longest_streak(db, habit)}")


def get_num_option(option_list):

    user_choice = input("Choose option: ")

    while(not user_choice.isdigit() or (user_choice.isdigit() and (int(user_choice) not in option_list))):
        user_choice = input("Not a valid option. Choose again: ")

    return int(user_choice)


def main():
    main_menu()


if __name__ == "__main__":
    main()
