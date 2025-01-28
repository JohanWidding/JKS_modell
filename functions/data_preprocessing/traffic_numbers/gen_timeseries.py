import pandas as pd

def generate_timeseries(project, initial_value, growth_rate):
    """
    Generates a time series with yearly values based on compound growth.

    Parameters:
    - start_year (int): The starting year of the time series.
    - end_year (int): The ending year of the time series.
    - initial_value (float): The value in the initial_year.
    - growth_rate (float): The annual growth rate as a decimal (e.g., 0.05 for 5%).
    - initial_year (int): The year where the initial_value is defined.

    Returns:
    - pd.Series: A pandas Series with years as the index and calculated values.
    """
    start_year = int(project.y_open) # Første året (åpningsåret)
    end_year = int(project.y_open) + int(project.n_y_life) # Siste året (analyse slutt)
    model_year = int(project.y_model) # Dette er året ÅDT tallene fra transportmodellen er beregnet for
    fylke = project.region
    scenario = project.scenario

    befolkning = project.population_df
    pop_to_traffic = project.pop_to_traffic_df

    years = range(start_year, end_year + 1)

    changes = []

    for y in years:
        if y in befolkning['Tid'].values and (y + 1) in befolkning['Tid'].values:
            curr_year = befolkning.loc[befolkning['Tid'] == y, f'{fylke}_{scenario}'].iloc[0]
            next_year = befolkning.loc[befolkning['Tid'] == (y + 1), f'{fylke}_{scenario}'].iloc[0]
            prc_change = 1 + ((next_year - curr_year) / curr_year)
        else:
            prc_change = 1 + growth_rate

        changes.append(prc_change)

    # Initialize the values list with None for all years
    values = [None] * len(years)

    # Find the index of the model value year
    initial_year_index = model_year - start_year # ex. 2030 - 2029 = 1 (index i listen values)

    # Set the initial value at its respective year
    values[initial_year_index] = initial_value # ex. ÅDT i år 2030

    # Fill in the values for years before the initial year (decreasing backward)
    for i in range(initial_year_index - 1, -1, -1):
        values[i] = values[i + 1] / changes[i]

    # Fill in the values for years after the initial year (increasing forward)
    for i in range(initial_year_index, len(changes) - 1):
        values[i + 1] = values[i] * changes[i]
        
    return pd.Series(data=values, index=years, name="Value")

