from courses import get_all_courses
from programs import get_all_programs
import pandas as pd
import time

def main():
    """Method for getting course and program data and saving it to an excel sheet in the root directory
    """
    courses, course_errors = get_all_courses()
    programs, program_errors = get_all_programs()

    with pd.ExcelWriter("./McGill.xlsx") as writer: # pylint: disable=abstract-class-instantiated
        courses.to_excel(writer, sheet_name="Courses")
        programs.to_excel(writer, sheet_name="Programs")

    if course_errors:
        print(f"{len(course_errors)} possible course errors:")
        for error in course_errors:
            print(error)
    if program_errors:
        print(f"{len(program_errors)} possible program errors:")
        for error in program_errors:
            print(error)

if __name__ == "__main__":
    tic = time.perf_counter()
    main()
    toc = time.perf_counter()
    print("Done")
    print(f"Operation took {toc-tic:0.4f} seconds")