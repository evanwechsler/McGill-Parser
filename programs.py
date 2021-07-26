from helper import get_data, validate_info, get_credits
from bs4 import PageElement

URL = "https://www.mcgill.ca/study/programs/search"

def get_program_info(program: PageElement) -> tuple:
    """Extracts program information from row

    Args:
        program (PageElement): Row in body of page containing program info

    Returns:
        tuple: (data, error) Data is a dictionary containing program info and error is a string containing any issues
    """
    name = program.find("div", class_="views-field views-field-field-calendar-title").a.string
    faculty = program.find("span", class_="views-field-field-faculty-code").span.string
    department = program.find("span", class_="views-field-field-dept-code").span.string
    level = program.find("span", class_="views-field-field-level-code").span.string
    degree = program.find("span", class_="views-field-field-degree-code").span.string
    num_credits = get_credits(name)
    data = {
        "Name": name,
        "Faculty": faculty,
        "Department": department,
        "Level": level,
        "Degree": degree,
        "Credits": num_credits
    }
    error = ""
    try:
        validate_info(data)
    except ValueError as err:
        error = str(err)

    return (data, error)

def get_all_programs() -> tuple:
    """Gets data for all programs

    Returns:
        tuple: (data, errors) Data is a dictionary containing data for all programs and errors is a list of possible issues
    """
    print("Getting programs...")
    data, errors = get_data(URL, get_program_info)
    print(f"{len(data.index)} programs found")
    print("--------------------------------")
    return (data, errors)
