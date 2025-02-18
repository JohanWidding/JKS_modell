import os
import pandas as pd
from collections import defaultdict

from functions.data_management.excel_main_template import dump_projects_to_excel

class ExcelFile:
    def __init__(self, variation: str, df: pd.DataFrame):
        self.variation = variation  # Variation identifier from the filename.
        self.df = df                # The loaded Pandas DataFrame.

def clean_header(header: str) -> str:
    """
    Cleans the header by stripping whitespace and replacing underscores with spaces.
    """
    return header.strip().replace("_", " ")

def determine_project_and_scenario(raw_header: str, all_headers: set) -> (str, str):
    """
    Given a raw header and a set of all raw headers, determine the project and scenario.

    If there exists another header in all_headers that is a proper prefix of raw_header,
    we use the longest such candidate as the project base. The scenario is the remaining
    part of raw_header (trimmed). If no extra text is found, the scenario defaults to "Main".
    Otherwise, if no candidate exists, the entire raw_header is used as the project and the
    scenario is "Main".
    
    The project name is enforced to be at least 7 characters long.
    """
    # Identify candidate base headers that are strictly shorter and are prefixes of raw_header.
    candidates = [h for h in all_headers if h != raw_header and raw_header.startswith(h)]
    if candidates:
        base = max(candidates, key=len)
        scenario = raw_header[len(base):].strip()
        if not scenario:
            scenario = "Main"
    else:
        base = raw_header
        scenario = "Main"
    return base, scenario

def load_excel_files(folder_path: str):
    """
    Loads Excel files from the specified folder and organizes them into a nested dictionary.
    
    Filename format is assumed to be:
    
        "Header___Variation.xlsx"
    
    - The "Header" part (before "___") represents the project and, optionally, the scenario.
    - If no "___" is found, variation defaults to "Standard".
    - In the two-pass approach:
        1. Each file is loaded with its cleaned raw header.
        2. We then collect all unique raw headers.
           For each file, if a shorter header exists that is a prefix of its header,
           that shorter header is used as the project and the remainder becomes the scenario.
           If no such candidate exists, the file is assigned to project = raw header and scenario = "Main".
    
    Returns:
        dict: A nested dictionary of the form:
              { project (str): { scenario (str): [list of ExcelFile objects] } }
    """
    filenames = [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]
    files_info = []  # List to hold tuples: (raw_header, ExcelFile object)
    
    # First pass: load files and record their raw headers.
    for filename in filenames:
        file_path = os.path.join(folder_path, filename)
        if "___" in filename:
            header_part, variation_part = filename.rsplit("___", 1)
        else:
            header_part, variation_part = filename, "Standard.xlsx"
        
        raw_header = clean_header(header_part)
        variation = variation_part.strip().replace("_", " ").replace(".xlsx", "")
        df = pd.read_excel(file_path, sheet_name=0)
        excel_file_obj = ExcelFile(variation, df)
        files_info.append((raw_header, excel_file_obj))
    
    # Collect all unique raw headers.
    all_headers = {raw_header for raw_header, _ in files_info}
    
    # Second pass: determine project and scenario based on prefix relationships.
    files_dict = defaultdict(lambda: defaultdict(list))
    
    for raw_header, excel_file_obj in files_info:
        project, scenario = determine_project_and_scenario(raw_header, all_headers)
        files_dict[project][scenario].append(excel_file_obj)

    # Print structured results
    dump_projects_to_excel(files_dict, "projects_data.xlsx")
    

