from functions.calculation_algorithms.calculate_project import calculate_project
from functions.data_management.load_project_data import load_data
from functions.data_management.output_main import load_excel_files


if __name__ == "__main__":
    data = load_data(project_file_name="Prosjekter")

    # I data filen finner du alle prosjektene listet som objekter i data.projects
    # Prosjekt objektet inneholder alle tabellene, og variablene fra 'keyword_mapping.txt'

    for project in data.projects:

        # Disse scenarione finner du under "Befolkningsfremskrivelser"-arket i inndata filen.
        # Standard bruker standard forutsetninger.
        # ["Hovedalternativet (MMMM)", "Høy nasjonal vekst (HHMH)", "Lav nasjonal vekst (LLML)"]
        scenarios = ["Standard"]

        for s in scenarios:
            trafikantnytte = calculate_project(project=project, scenario=s)

    # Her lastes alle output filene inn og genrerer projects_data.xlsx
    load_excel_files("Output//")