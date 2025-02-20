from functions.calculation_algorithms.calculate_project import calculate_project
from functions.data_management.load_project_data import load_data
from functions.data_management.output_main import load_excel_files


if __name__ == "__main__":
    data = load_data(project_file_name="Prosjekter")

    for project in data.projects:

        scenarios = ["Standard"]

        for s in scenarios:
            trafikantnytte = calculate_project(project=project, scenario=s)


    load_excel_files("Output//")