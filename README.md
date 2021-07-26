# McGill-Parser

# Intro

I built this parser to extract all courses and programs from McGill's eCalendar website into an excel spreadsheet. This might be useful for you if you have an idea for a project that requires this info. Unfortunately McGill doesn't provide this data already...

If you have any suggestions please let me know or make a PR.

## Suggested Set Up

1. Clone the repo
2. cd into the repo
3. `pip install virtualenv`
4. `python3 -m venv env`
5. `source env/bin/activate`
6. `pip install pandas`
7. Run the main.py file to extract all course and program data into a spreadsheet

# What the parser will do for you

After running `main.py` you will have an excel spreadsheet generated in the same directory as the project. This spreadsheet contains 2 sheets:

## Courses

| Index |                         Name                          |      Faculty       |    Department    |     Level     | Credits |
| :---: | :---------------------------------------------------: | :----------------: | :--------------: | :-----------: | :-----: |
|   0   | COMP 250 Introduction to Computer Science (3 credits) | Faculty of Science | Computer Science | Undergraduate |    3    |
|  ...  |                          ...                          |        ...         |       ...        |      ...      |   ...   |

## Programs

| Index |                                  Name                                   |        Faculty         |       Department       |     Level     | Credits |
| :---: | :---------------------------------------------------------------------: | :--------------------: | :--------------------: | :-----------: | :-----: |
|   0   | Bachelor of Engineering (B.Eng.) - Mechanical Engineering (142 credits) | Faculty of Engineering | Mechanical Engineering | Undergraduate |   142   |
|  ...  |                                   ...                                   |          ...           |          ...           |      ...      |   ...   |
