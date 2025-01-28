import json
import pandas as pd

from functions.data_management.project_handeler import Project


class ExcelDataHandler:
    def __init__(self, file_path_projects, file_path_mapping,
                            sheet_name_price_growth,
                            sheet_name_wage_growth,
                            sheet_name_projects, sheet_name_population, sheet_name_pop_to_traffic):
        """
        Initialiserer klassen med filsti til Excel-dokumentet.
        :param file_path: Filsti til Excel-dokumentet.
        """
        self.file_path = file_path_projects
        self.keyword_mapping = self.read_dict_from_file(file_path_mapping)
        self.price_growth_df = self.get_sheet_from_excel(sheet_name_price_growth)
        self.wage_growth_df = self.get_sheet_from_excel(sheet_name_wage_growth)
        self.projects_df = self.get_sheet_from_excel(sheet_name_projects)
        self.population_df = self.get_sheet_from_excel(sheet_name_population)
        self.pop_to_traffic_df = self.get_sheet_from_excel(sheet_name_pop_to_traffic)
        self.store_projects_in_a_list()
        

    def read_dict_from_file(self, file_path):
        # Read the entire dictionary from the file
        with open(file_path, 'r', encoding='utf-8') as file:
            large_dict = json.load(file)
        
            return large_dict

    def get_sheet_from_excel(self, sheet_name):
        """
        Henter data fra et spesifikt ark i Excel-dokumentet.
        :param sheet_name: Navnet på arket som skal hentes.
        :return: DataFrame med data fra det spesifiserte arket.
        """
        try:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            return df
        except Exception as e:
            print(f"Error reading sheet '{sheet_name}': {e}")
            return None

    def get_value_from_search(self, column_index, search_term):
        """
        Return the value from a specific column in a DataFrame based on a search term in the first column.

        Args:
            df (pd.DataFrame): The DataFrame to search.
            column_index (int): The index (1-based) of the column to return the value from.
            search_term (str): The term to search for in the first column.

        Returns:
            The value from the specified column if a match is found.

        Raises:
            ValueError: If the search term is not found in the first column.
        """
        if column_index < 1 or column_index > len(self.projects_df.columns):
            raise ValueError("Invalid column index. It must be between 1 and the number of columns in the DataFrame.")
        
        if search_term not in self.keyword_mapping:
            raise KeyError(f"Search term '{search_term}' not found in keyword_mapping.txt.")

        keyword = self.keyword_mapping[search_term]

        # Search for the row where the first column matches the search term
        match = self.projects_df[self.projects_df.iloc[:, 0] == keyword]

        # If a match is not found, raise an error
        if match.empty:
            raise ValueError(f"Key '{keyword}' not found in the first column in Prosjekter.xlsx")

        # Return the value from the specified column
        return match.iloc[0, column_index]
    
    def store_projects_in_a_list(self):
        self.projects = []
        num_columns = self.projects_df.shape[1]
        column_names = self.projects_df.columns.tolist()

        for i in range(1, num_columns):
            project_name = column_names[i]
            attr_names = []
            attr_values = []
            for key, val in self.keyword_mapping.items():
                attr_names.append(key)
                attr_values.append(self.get_value_from_search(i, key))
            
            project = Project(project_name, attr_names, attr_values, self.price_growth_df, self.wage_growth_df, self.population_df, self.pop_to_traffic_df)

            self.projects.append(project)




# Eksempel på bruk
if __name__ == "__main__":
    file_path = 'Data/Prosjekter.xlsx'
    data = ExcelDataHandler(file_path)

    print(data.projects[0].D_a1) 
    print(data.projects[0].name) 

