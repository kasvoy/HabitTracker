# A CLI Habit Tracker in Python

## To install
Requirements: Newest version of the Python 3 interpreter installed for your platform: https://www.python.org/downloads/

Download the code from this repository, either downloading it as zip using the green code button
or type in terminal: 
```
git clone https://github.com/kasvoy/HabitTracker
```

In all the code snippets below the python interpeter is invoked to run the code. The format `python3 [filename] [options]` is used in this readme,
as it would be on the by default on Unix operating systems but keep in mind on different platforms it can be invoked differently such as 
`python [filename] [options]` on Windows. So if you type "python3" and it doesn't work, try "python" instead. See the python documentation for details: https://docs.python.org/3/tutorial/interpreter.html#invoking-the-interpreter 


## To run the app
Navigate to the directory ../HabitTracker (if cloned using git) or  ../HabitTracker-main (from unzipped code file)

Run from terminal:
```
python3 habit.py
```

## To run tests
From the directory ../HabitTracker

Run from terminal: 
```
python3 -m unittest
```
to run all of the unit tests from the tests folder.

In the tests directory you can see there are 3 tests related to different parts of the program. If you wish to run tests individually run:
```
python3 -m unittest tests.test_analysis
```
to test the analysis module, or
```
python3 -m unittest tests.test_database
```
to test the database class, or
```
python3 -m unittest tests.test_habitclass
```
to test the habit class and functionality related to checking off the habits.


# How to use the Habit Tracker
Define and check off your habits, build your streak and see your stats!

This program allows you to define habits - tasks you would like to accomplish periodically - and then check them off and track your progress.
This could be anything like exercising, meditation, tracking your spending - you name it!
The app allows you to set the *frequency* of a habit - this is per how many days you want to engage in the habit.

For example:
You want to meditate daily - you would set the frequency to 1.
You want to clean your room weekly - you would set the frequency to 7.
You want to exercise every two days - you would set the frequency to 2.

To navigate the app, when you're prompted to "Choose option: " in any menu, put in one of the numbers representing the available options followed by Enter.
When you open the app, you are presented with the main menu - to define a habit put "2" and press Enter when prompted.
This brings you to the menu where you can define your habit. Just follow the prompts on screen:)

### Checking off habits
The app allows you to check off your habits - log them into the program's database so you can build your streak and track your progress.
From the main menu, type "1" and hit Enter - the option corresponding to checking off habits. From there you can pick the habit you want to check off.
After choosing your habit, pick option "1" to check off habit - this will log a habit entry into the database for today.
In case you engaged in one of your habits, but forgot to check it off, the app allows you to "backlog", meaning put a log for a date in the past.
This will update your streak accordingly.

The habit data is stored in the "database.db" file. **Make sure you do not delete it!**

### Tracking your habits
From the main menu, you can go to the tracking menu by putting in option "3" followed by Enter. You can also type "t" right after checking off a habit when prompted.
From there, option "1" will lead you to seeing all of your defined habits - from there you can inspect them, edit them or delete them. You can also track an individual habit, which is equivalent to putting in option "2" in the first place like mentioned below.

Option "2", on the other hand, will allow you to inspect your statistics regarding the streaks of your habits. You can put in the option corresponding
to the habit you want to inspect follow by Enter, or check out any of the "global" stats - ones that are related to all of your habits, such as what's your best streaks out of all your habits, etc.

### Tests and test data
As mentioned above from the main directory you can run `python3 -m unittest` to run all the unit tests.
These tests use test data related to 5 predefined habits. If you wish to inspect these predefined habits and their tracking data and play around 
with the habit tracker with them you can run:
`python3 habit.py test`. This will use the "test.db" database file that is included in the folder, but also gets regenerated every time you run the tests.
The script responsible for generating the test data is "testdata.py" in the src folder which you can run by typing `python3 -m src.testdata` from the project directory.
The check off dates of the test data are hardcoded and for all predefined habits start on Feb 20 2023 and end on Apr 30 2023. Because of this if you wish to check off the predefined test habits you can manipulate the date of check off with option "2" in the check off menu - this might be needed depending what you want to check out because checking off for "now" depends what date you use this application in test mode. Keep in mind, any time you run the tests, the test data will be regenerated.
