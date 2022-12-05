import sys, subprocess
import time
import analysis
from database import DatabaseConnection



class Habit:

    def __init__(self, name, description, frequency):
        self.name = name
        self.description = description
        self.frequency = frequency

database = DatabaseConnection("database.db")


def main_menu():
    subprocess.run("clear", shell = True)
    print("Hello and welcome to my habit tracker, take your pick.")
    print(" 1. Check off habit. \n 2. Add new habit. \n 3. Track and edit current habits \n 4. Quit program")


    option = get_num_option([1,2,3,4])

    if option == 1:
        pass

    elif option == 2:
        add_habit_menu()

    elif option == 3:
        tracking_menu()

    if option == 4:
        print("Program quit")
        database.conn.close()
        sys.exit()


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
        db.add_habit(habit.name, habit.description, habit.frequency)

    print("Habit added!")
    print(" 1. Check off habit. \n 2. Main menu")

    option = get_num_option([1,2])

    if option == 1:
        check_off_menu()

    elif option == 2:
        main_menu()


def indiv_habit_menu(habit_name):
    print(f"Habit: {habit_name}")
    pass

def check_off_menu():
    pass

def tracking_menu():

    subprocess.run("clear", shell = True)
    print("TRACKING YOUR HABITS")

    print(" 1. Show all of my habits. \n 2. Track habit")

    option = get_num_option([1,2])

    if option == 1:
        with database as db:
            habit_list = analysis.get_current_habits(db)

        if len(habit_list) == 0:
            print("You are not currently tracking any habits. ")
            print(" 1. Add habit. \n 2. Main menu")
            option = get_num_option([1,2])

            if option == 1:
                add_habit_menu()
            elif option == 2:
                main_menu()

        for habit in habit_list:
            print('\033[1m',habit[0].upper(),'\033[0m')
            print(f"Description: {habit[1]}")

            if habit[2] == 1:
                print("Frequency: Done every day")
            else:
                print(f"Frequency: Done every {habit[2]} days")

        print(" 1. Track habit. \n 2. Main menu")
        option = get_num_option([1,2])

        if option == 1:
            pass

        elif option == 2:
            main_menu()

    elif option == 2:
        pass


def get_num_option(option_list):

    user_choice = input("Choose option: ")

    while(not user_choice.isdigit() or (user_choice.isdigit() and (int(user_choice) not in option_list))):
        user_choice = input("Not a valid option. Choose again: ")

    return int(user_choice)


def main():
    main_menu()



if __name__ == "__main__":
    main()





"""
with db:
    #db.add_habit("Exercise", "I want to exercise every day", 1)
    print(db.get_current_habits())
    db.insert_habit_entry("Exercise")
    #db.insert_habit_entry("Exercise", time.mktime(time.strptime("30 Nov 2022 15:15:27", "%d %b %Y %H:%M:%S")))
    db.print_habit_info()
"""
