from bs4 import BeautifulSoup, PageElement
import requests
import pandas as pd
from typing import Callable

ERRORS = []


def get_last_page_number(soup: BeautifulSoup) -> int:
    """Finds the last page of courses

    Args:
        soup (BeautifulSoup): soup of main page

    Returns:
        int: Last page number
    """
    pager_last_list_elements = soup.find_all("li", class_="pager-last last")[0]
    pager_link = pager_last_list_elements.contents[0]
    pagination_href = pager_link['href']
    query_param_location = pagination_href.find("=")
    last_page_number = int(pagination_href[query_param_location + 1:])
    return last_page_number


def get_credits(title: str) -> float:
    """Get the number of credits for a course or program

    Args:
        title (str): Title of course or program containing credit info

    Returns:
        float: Number of credits 
    """
    # Find end index of credit substring
    end_index = title.find(" credit")
    if end_index == -1:
        end_index = title.find(" crédit")

    # Find start index of credit substring
    start_index = title.rfind("(", end_index - 8, end_index) + 1

    # If no credit info is found, assume 0 credits
    if end_index == -1 or start_index == 0:
        return 0.0
    
    # If any issues are encountered, return 0
    try:
        num_credits = float(title[start_index: end_index])
    except ValueError:
        try:
            num_credits = float(title[start_index: end_index].split("-")[0])
        except:
            return 0.0

    return num_credits

def validate_info(info: dict) -> None:
    """Validated info in the data dictionary

    Args:
        info (dict): Course or program info

    Raises:
        ValueError: Raised if some data is missing
    """
    error_values = []
    for k, v in info.items():
        if not v and v != 0:
            error_values.append(k)
    if len(error_values) > 0:
        raise ValueError(f"Could not find data for {','.join(error_values)}. Data: {info}")

def get_all_info(soup: BeautifulSoup, get_data_method: Callable[[PageElement], dict]) -> tuple: # pylint: disable=unsubscriptable-object
    """Gets all courses or program data in a page

    Args:
        soup (BeautifulSoup): soup object of page to scrape
        get_data_method (Callable[[PageElement], dict]): Method to extract info from single course or program

    Returns:
        tuple: (all_data, errors) all_data is a dictionary containing data for all courses/programs on a page and errors is a list of string of possible errors
    """
    
    rows = soup.findAll("div", class_="views-row")
    all_data = {}
    errors = []
    for row in rows:
        data, error = get_data_method(row)
        if error:
            errors.append(error)
        if not all_data:
            all_data = {k: [v] for (k, v) in data.items()}
        else:
            for k in all_data.keys():
                all_data[k].append(data[k])
        
    
    return (all_data, error)

def go_through_all_pages(soup: BeautifulSoup, url: str, get_data_method: Callable[[PageElement], dict]) -> tuple: # pylint: disable=unsubscriptable-object
    """Goes through all pages on McGill website and extracts data from each one

    Args:
        soup (BeautifulSoup): soup object of course or program search page
        url (str): base url to loop through pagination
        get_data_method (Callable[[PageElement], dict]): method to extract data from single course/program

    Returns:
        tuple: (all_data, errors) all_data is a dictionary containing data for all courses/programs and errors is a list of string of possible issues 
    """
    all_data = {}

    num_pages = get_last_page_number(soup)
    # num_pages = 1
    errors = []
    for page_num in range(num_pages + 1):
        page_url = url + f"?page={page_num}"
        print(f"Page {page_num} / {num_pages}")
        page = requests.get(page_url)
        page_soup = BeautifulSoup(page.content, "html.parser")
        page_data, error = get_all_info(page_soup, get_data_method)
        if not all_data:
            all_data = {k: v for (k, v) in page_data.items()}
        else:
           for k in all_data.keys():
                all_data[k] += page_data[k] 
        if error:
            errors += error
    return (all_data, errors)
    

def get_data(url: str, get_data_method: Callable[[PageElement], dict]) -> tuple: # pylint: disable=unsubscriptable-object
    """Extracts data from all pages into a pandas dataframe

    Args:
        url (str): Base url to get data from 
        get_data_method (Callable[[PageElement], dict]): Method to extract data from single course/program

    Returns:
        tuple: (df, errors) df is a dataframe objects containing all data and errors is a list of string of possible issues
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    data, errors  = go_through_all_pages(soup, url, get_data_method)

    df = pd.DataFrame(data=data)
    return (df, errors)




