from functions.calculation_algorithms.calculate_project import calculate_project
from functions.data_management.load_project_data import load_data


if __name__ == "__main__":
    data = load_data()

    for project in data.projects:

        scenarios = ["Hovedalternativet (MMMM)", "Lav nasjonal vekst (LLML)", "Høy nasjonal vekst (HHMH)"]

        trafikantnytte_liste = []

        for s in scenarios:
            trafikantnytte = calculate_project(project=project, scenario=s)

            trafikantnytte_liste.append(trafikantnytte)

        for i in range(len(trafikantnytte_liste)):
            print(f"{project.name}_{scenarios[i]}: {f"{int(trafikantnytte_liste[i]):,}".replace(",", " ")}  ({round((trafikantnytte_liste[i]-trafikantnytte_liste[0])/trafikantnytte_liste[0],2)} %)")