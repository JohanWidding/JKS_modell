

from functions.data_management.get_data_from_excel import ExcelDataHandler


def load_data():
    file_path_projects = 'data/Prosjekter.xlsx'
    file_path_mapping = 'data/keyword_mapping.txt'
    sheet_name_price_growth = 'Tabell prisvekst'
    sheet_name_wage_growth = 'Tabell lønnsvekst'
    sheet_name_projects = "ProsjektData"
    sheet_name_population = "Befolkningsfremskrivinger"

    data = ExcelDataHandler(file_path_projects, 
                            file_path_mapping,
                            sheet_name_price_growth,
                            sheet_name_wage_growth,
                            sheet_name_projects,
                            sheet_name_population)
    return data