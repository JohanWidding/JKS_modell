from functions.calculation_algorithms.calculate_project import calculate_project
from functions.data_management.load_project_data import load_data


if __name__ == "__main__":
    data = load_data()

    for project in data.projects:

        scenarios = ["MMMM", "LLML", "HHMH"]

        for s in scenarios:
            trafikantnytte = calculate_project(prosjekt=project, scenario=s)

        