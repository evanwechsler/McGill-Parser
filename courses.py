from helper import get_data, validate_info, get_credits
from bs4 import PageElement

URL = "https://www.mcgill.ca/study/courses/search"

def get_course_info(course: PageElement) -> tuple:
    """Extracts course information from row

    Args:
        course (PageElement): Row in body of page containing course info

    Returns:
        tuple: (data, error) Data is a dictionary containing course info and error is a string with a possible issue
    """
    name = course.find("div", class_="views-field-field-course-title-long").a.string
    faculty = course.find("span", class_="views-field-field-faculty-code").span.string
    department = course.find("span", class_="views-field-field-dept-code").span.string
    level = course.find("span", class_="views-field-level").span.string
    num_credits = get_credits(name)
    data = {
        "Name": name,
        "Faculty": faculty,
        "Department": department,
        "Level": level,
        "Credits": num_credits
    }

    error = ""
    try:
        validate_info(data)
    except ValueError as err:
        error = str(err)

    return (data, error)

def get_all_courses() -> tuple:
    """Gets data for all courses

    Returns:
        tuple: (data, errors) data is a dictionary containing info for all courses and errors is a list of string of possible issues
    """
    print("Getting courses...")
    data, errors = get_data(URL, get_course_info)
    print(f"{len(data.index)} courses found")
    print("--------------------------------")
    return (data, errors)


