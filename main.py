import sys, subprocess, time, analysis
from datetime import date
from database import DatabaseConnection
from habitclass import Habit

db = DatabaseConnection("database.db")

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

    habit_list = analysis.get_current_habits(db)

    if len(habit_list) == 0:
        not_tracking_habits()

    else:
        for i in range(len(habit_list)):
            print(f"{i+1}. {habit_list[i].name}")

        option = get_num_option(range(1, len(habit_list) + 1))
        tracked_habit = habit_list[option - 1]

        tracked_habit.check_off(db)

        print(f"{tracked_habit.name} checked off! Current streak for {tracked_habit.name}: {tracked_habit.current_streak}")

def add_habit_menu():
    subprocess.run("clear", shell = True)
    print("ADD NEW HABIT")

    habit_name = input("Create habit name: ").strip()
    description = input("Set a description for your habit: ")
    frequency = input("Set frequency (in number of days): ")

    while(not frequency.isdigit() or (frequency.isdigit() and int(frequency) < 1)):
        frequency = input("Frequency must be a positive integer: ")

    habit = Habit(habit_name, description, frequency)

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

    option1 = get_num_option([1,2])

    if option1 == 1:
        habit_list = analysis.get_current_habits(db)

        if len(habit_list) == 0:
            not_tracking_habits()

        else:
            subprocess.run("clear", shell = True)
            print("YOUR HABITS")
            for habit in habit_list:
                print('\n\033[1m',habit.name.upper(),'\033[0m')
                print(f"Description: {habit.description}")

                if habit.frequency == 1:
                    print("Frequency: Done every day")
                else:
                    print(f"Frequency: Done every {habit.frequency} days")

            print("\n 1. Edit/delete a habit \n 2. Track habit. \n 3. Main menu")
            option2 = get_num_option([1,2,3])

            if option2 == 1:

                subprocess.run("clear", shell = True)
                print("Which habit would you like to edit or delete?\n")

                print("0. Go back to main menu")
                for i in range(len(habit_list)):
                    print(f"{i+1}. {habit_list[i].name}")

                del_option = get_num_option([0, len(habit_list)])

                if del_option == 0:
                    main_menu()

                else:
                    subprocess.run("clear", shell = True)
                    chosen_habit = habit_list[del_option - 1]
                    print("Do you want to edit or delete this habit?")
                    print("\n 1. Edit \n 2. Delete")
                    edit_option = get_num_option([1, 2])

                    if edit_option == 1:
                        editing_menu()

                    elif edit_option == 2:
                        db.delete_habit(chosen_habit)

                        subprocess.run("clear", shell = True)
                        print(f"{chosen_habit.name} deleted.")
                        print("0. Go back to main menu")
                        menu_nooption = get_num_option([0])
                        main_menu()

            elif option2 == 2:
                tracking_choice_menu()

            else:
                main_menu()

    elif option1 == 2:
        tracking_choice_menu()


def tracking_choice_menu():
    subprocess.run("clear", shell = True)
    print("Which of your habits would you like to track?")

    habit_list = analysis.get_current_habits(db)

    for i in range(len(habit_list)):
        print(f"{i+1}. {habit_list[i].name}")

    option = get_num_option(range(1, len(habit_list) + 1))
    habit = habit_list[option-1]
    print("in tracking choice menu", habit)

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
        analysis.print_habit_data(db, habit)

    if option == 2:
        print(f"Your best streak for {habit.name} is {analysis.get_longest_streak(db, habit)}")


def get_num_option(option_list):

    user_choice = input("\nChoose option: ").strip()

    while(not user_choice.isdigit() or (user_choice.isdigit() and (int(user_choice) not in option_list))):
        user_choice = input("Not a valid option. Choose again: ")

    return int(user_choice)

def editing_menu():
    print("Not implemented yet")
    pass

def not_tracking_habits():

    subprocess.run("clear", shell = True)
    print("You are not currently tracking any habits. ")
    print(" 1. Add habit. \n 2. Main menu")
    option = get_num_option([1,2])

    if option == 1:
        add_habit_menu()
    elif option == 2:
        main_menu()

def main():
    main_menu()


if __name__ == "__main__":
    main()
