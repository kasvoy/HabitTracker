import sys, subprocess, datetime, sqlite3
from . import database, analysis
from . import habitclass

if len(sys.argv) == 2 and sys.argv[1].lower() == 'test':
    db = database.DatabaseConnection("test.db")
else:
    db = database.DatabaseConnection("database.db")

def main_menu():
    clear_screen()
    print("\033[95m\033[1mHABIT PYTRACKER EARLY RELEASE 1.1.\033[0m\n")
    print(" 1. Check off habit. \n 2. Add new habit. \n 3. Track and edit current habits \n 4. Quit program")

    option = get_num_option([1,2,3,4])

    if option == 1:
        check_off_menu()

    elif option == 2:
        add_habit_menu()

    elif option == 3:
        tracking_menu()

    elif option == 4:
        print("Program quit")
        db.conn.close()
        sys.exit()

def check_off_menu():
    clear_screen()
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
        
        date_today_string = datetime.date.today().strftime("%A %d %B %Y")
        clear_screen()
        print(f"Checking off habit \033[1m{tracked_habit.name}\033[0m\n")
        
        
        print(f"\n\033[1m1. Check off habit - NOW ({date_today_string})\033[0m")
        print("\n\n2. Forgot to check off habit before and maybe lost a streak? Check off for date in the past.")
        option = get_num_option([1,2])
        
        if option == 1:                
            tracked_habit.check_off(db)

            print(f"{tracked_habit.name} checked off! Current streak for {tracked_habit.name}: {tracked_habit.current_streak}")
            back_or_quit_or_track()
            
        elif option == 2:
            print(f"What date do you want to insert an entry for {tracked_habit.name}?")
            date_seconds = get_date_frominput()
            
            tracked_habit.check_off(db, date_seconds)
            print(f"{tracked_habit.name} checked off! Current streak for {tracked_habit.name}: {tracked_habit.current_streak}")
            back_or_quit_or_track()

def add_habit_menu():
    clear_screen()
    print("ADD NEW HABIT")

    habit_name = input("Create habit name: ").strip()
    description = input("Set a description for your habit: ")
    frequency = input("Set frequency: ")

    while(not frequency.isdigit() or (frequency.isdigit() and int(frequency) < 1)):
        frequency = input("Frequency must be a positive integer: ")

    habit = habitclass.Habit(habit_name, description, frequency)

    try:
        db.add_habit(habit)
    except sqlite3.IntegrityError:
        clear_screen()
        print("You're trying to add a habit with an exact same name as one of your habits. Add a habit with a different name from the main menu.")
        back_or_quit_or_track()


    clear_screen()
    print("Habit added!")
    print(" 1. Check off habit. \n 2. Main menu")

    option = get_num_option([1,2])

    if option == 1:
        check_off_menu()

    elif option == 2:
        main_menu()


def tracking_menu():

    clear_screen()
    print("\033[1mTRACKING YOUR HABITS\033[0m")

    print(" 1. Show all of my habits. \n 2. Track habit \n")

    option1 = get_num_option([1,2])
    habit_list = analysis.get_current_habits(db)
    
    if option1 == 1:
        if len(habit_list) == 0:
            not_tracking_habits()

        else:
            clear_screen()
            print("\033[1m\u001b[32mYOUR HABITS\u001b[0m")
            for habit in habit_list:
                print('\n\033[1m',habit.name,'\033[0m')
                print(f"Description: {habit.description}")

                if habit.frequency == 1:
                    print("Frequency: Done every day")
                else:
                    print(f"Frequency: Done every {habit.frequency} days")

            print("\n 1. Edit/delete a habit \n 2. Track habit. \n 3. Main menu")
            option2 = get_num_option([1, 2, 3, 4])

            if option2 == 1:

                clear_screen()
                print("Which habit would you like to edit or delete?\n")

                print("0. Go back to main menu")
                for i in range(len(habit_list)):
                    print(f"{i+1}. {habit_list[i].name}")

                del_option = get_num_option(range(len(habit_list) + 1))

                if del_option == 0:
                    main_menu()

                else:
                    clear_screen()
                    chosen_habit = habit_list[del_option - 1]
                    print(f"Do you want to edit or delete \033[1m{chosen_habit.name}\033[0m?")
                    print("\n 1. Edit \n 2. Delete")
                    edit_option = get_num_option([1, 2])

                    if edit_option == 1:
                        editing_menu(chosen_habit)

                    elif edit_option == 2:
                        db.delete_habit(chosen_habit)

                        clear_screen()
                        print(f"\033[1m{chosen_habit.name}\033[0m deleted.")
                        back_or_quit_or_track()

            elif option2 == 2:
                tracking_choice_menu()

            else:
                main_menu()

    elif option1 == 2:
        if len(habit_list) == 0:
            not_tracking_habits()
        else:  
            tracking_choice_menu()


def tracking_choice_menu():
    clear_screen()
    print("Which of your habits would you like to track?")

    habit_list = analysis.get_current_habits(db)
    length = len(habit_list)

    for i in range(len(habit_list)):
        print(f"{i+1}. {habit_list[i].name}")

    print("\nOR GLOBAL STATS:\n ")
    print(f"{length+1}. Show longest streak of all your habits.")
    print(f"{length+2}. Show habits with the same frequency.")
    print(f"{length+3}. With which habits did you struggle most so far?")

    option = get_num_option(range(1, length + 4))
    if option < length + 1:
        habit = habit_list[option-1]
        indiv_habit_tracking_menu(habit)
    
    elif option == length + 1:
        
        name_streak = analysis.get_longest_streak_all(db)
        
        name = name_streak[0]
        best_streak = name_streak[1]
        
        print(f"Your longest streak of all habits is {best_streak} for habit {name}.")
        back_or_quit_or_track()

    elif option == length + 2:
        clear_screen()
        sorted_freq_set = sorted(analysis.get_frequencies(db))

        for i in range(len(sorted_freq_set)):
            print(f"{i+1}. Habits done every {sorted_freq_set[i]} days.")

        freq_option = get_num_option(range(0, len(sorted_freq_set) + 1))
        chosen_freq = sorted_freq_set[freq_option - 1]
        habits_with_chosen_freq = analysis.get_habits_with_freq(db, chosen_freq)

        print(f"Habits done every {chosen_freq} days are:")

        for i in range(len(habits_with_chosen_freq)):
            print(f"{i+1}. {habits_with_chosen_freq[i]}")

        back_or_quit_or_track()
        
    elif option == length + 3:
        clear_screen()
        print("What habits did you struggle most with?")
        print("\nThis is determined by how many streak losses you had in your chosen period.")
        print("\nFor example, if you want to know which habits you struggled the most with last month, put '30' in the next prompt.")
        period_no_days = input("\nPut the number of days from today you want to know how many streak losses you had: ")
        
        while(not period_no_days.isdigit() or (period_no_days.isdigit() and int(period_no_days) < 1)):
            period_no_days = input("Not a valid period. Pick a whole positive number of days: ")
        
        clear_screen()

        habit_streakloss = analysis.find_most_streakloss_in_period(db, int(period_no_days))
        
        if not habit_streakloss:
            print(f"No streak losses in the last {period_no_days} days! Keep up the good work!")
        else:
            print(f"The habit(s) that you struggled with the most in the last {period_no_days} days is/are: ")
            for habit_name, streakloss in habit_streakloss.items():
                print(f"\n\033[1m{habit_name}\033[0m with \033[1m{streakloss}\033[0m streak losses.")

        back_or_quit_or_track()

"""
Functionalities related to tracking individual habits (streak info etc).
"""

def indiv_habit_tracking_menu(habit):
    clear_screen()
    print(f"Habit: {habit.name}. Current streak: {habit.current_streak}\n")

    print(f" 1. Show all entries for {habit.name}. \n 2. What was my longest streak for {habit.name}")

    option = get_num_option([1, 2])

    if option == 1:
        print_habit_data(db, habit)

    if option == 2:
        print(f"Your best streak for {habit.name} is {analysis.get_longest_streak_habit(db, habit)}")

    back_or_quit_or_track()


def get_num_option(option_list):

    user_choice = input("\nChoose option: ").strip()

    while(not user_choice.isdigit() or (user_choice.isdigit() and (int(user_choice) not in option_list))):
        user_choice = input("Not a valid option. Choose again: ")

    return int(user_choice)

def get_date_frominput():
    year = input("Enter year (type 'm' if you didn't intend this): ")

    #giving the user the option to back out in case of missclick
    while((not year.isdigit() and year.lower() != 'm') or (year.isdigit() and int(year) < 1970)):
        year = input("Enter a valid year (Gregorian calendar, before 1970): ")
    
    if year.lower() == 'm':
        main_menu()

    else:
        month = input("Enter month (1-12): ")
        while(not month.isdigit() or (month.isdigit() and int(month) not in list(range(1, 13)))):
            month = input("Enter a valid month (1-12): ")
                
        day = input("Enter day: ")
        while(not month.isdigit() or (month.isdigit() and int(month) not in list(range(1, 31)))):
            month = input("Enter a valid day - depends on month!): ")
        
            
        #The 15:30:00 time is completely arbitrary, as the main functionalities of the program are related
        #to just the dates. The time is set arbitrarly as the datetime.date objects do not have a timestamp() method 
        date = datetime.datetime(int(year), int(month), int(day), 15, 30, 0)
        return int(date.timestamp())

def editing_menu(habit):
    clear_screen()
    print(f"\033[1mEDITING HABIT - {habit.name}\033[0m\n")
    
    new_name = input((f"Current habit name: \033[1m{habit.name}\033[0m. Type new name: ")).strip()
    while (not new_name or new_name.isspace()):
        new_name = input(f"Provide a new name (can't be just spaces); if you changed your mind, just put in the same name: ")
    
    new_description = input((f"Current habit description: \033[1m{habit.description}\033[0m. Type new description: ")).strip()
    while (not new_description or new_description.isspace()):
        new_description = input(f"Provide a new description (if you changed your mind, just put in the same one: ")
    
    print("\n\033[1mKEEP IN MIND\033[0m: Changing the frequency changes when you get a streak increase.")

    new_frequency = input(f"\nCurrent frequency: \033[1m{habit.frequency}\033[0m; Provide new frequency (if you changed your mind just put in the same one as before): ")
    while (not new_frequency.isdigit() or (new_frequency.isdigit() and int(new_frequency) < 1)):
        new_frequency = input("Provide a valid frequency - a positive whole number of days: ") 
    
    new_values = [new_name, new_description, int(new_frequency)]
    db.edit_habit(habit, new_values)
    
    print("Habit edited!")
    
    back_or_quit_or_track()

def not_tracking_habits():

    clear_screen()
    print("You are not currently tracking any habits. ")
    print(" 1. Add habit. \n 2. Main menu")
    option = get_num_option([1,2])

    if option == 1:
        add_habit_menu()
    elif option == 2:
        main_menu()

def back_or_quit_or_track():

    user_choice = input("\nType 'm/M' for main menu or 't/T' for tracking menu or q/Q to quit program: ").lower()

    while(user_choice != 'q' and user_choice != 'm' and user_choice != 't'):
        user_choice = input("Not a valid option. Type 'm/M' for main menu or 't/T' for tracking menu or q/Q to quit program: ").lower()

    if user_choice == 'q':
        print("Program quit.")
        sys.exit()
    elif user_choice == 'm':
        main_menu()
    else:
        tracking_choice_menu()

def print_habit_data(db, habit):

    """
    A function that prints all the habit logs in the habit_data table

    Parameters:
                db: a database.DatabaseConnection object
                habit: a habitclass.Habit object
    """

    if len(analysis.get_habit_data(db, habit)) == 0:
        print(f"No entries for {habit.name} yet! You can check off the habit from the main menu")

    for entry in analysis.get_habit_data(db, habit):
        print(f"Date: {datetime.date.fromtimestamp(entry[1])}, streak: {entry[2]}")

def clear_screen():
    os = sys.platform
    
    if os == 'win32':
        subprocess.run("cls", shell = True)
    elif os == 'linux' or os == 'darwin':
        subprocess.run("clear", shell = True)    
    
def main():
    main_menu()

if __name__ == "__main__":
    main()
    
