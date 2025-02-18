import numpy as np
import pandas as pd

def generate_timeseries(project, initial_value, growth_rate, decay_list):
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
    pop_to_traffic = project.pop_to_traffic_df # Brukes ikke lengre
    adj_traffic_factor = project.adj_traffic

    years = range(start_year, end_year + 1)

    changes = []

    # Her går det ann å bruke rullwt anitt av de 5 siste årsendringene som videre vekst.
    # Ett problem her er at nå vil godstransport få samme vekst som lett transport de første årene frem til 2050
    # Her går det ann å endre inisialverdien i modell året for scenario med lavere vekst og høyere vekst.
    # Øsnker å modellere en slags prosent basert på årstallet, som blir sterkere når året blir stort.
    # Det må være litt som en logistisk synkende faktor, og en måte å justere når mellom 0 og 100 år den skal begynne å synke.

    rolling_mean_prc_change = 0

    for y in years:
        try:
            if y in befolkning['Tid'].values and (y + 1) in befolkning['Tid'].values:
                curr_year = befolkning.loc[befolkning['Tid'] == y, f'{fylke}_{scenario}'].iloc[0]
                next_year = befolkning.loc[befolkning['Tid'] == (y + 1), f'{fylke}_{scenario}'].iloc[0]
                region_factor = project.transport_el
                prc_change = ((next_year - curr_year) / curr_year) * region_factor
            else:
                if rolling_mean_prc_change != 0:
                    prc_change = rolling_mean_prc_change
                else:
                    prc_change = growth_rate

            if len(changes) > 5:
                rolling_mean_prc_change = np.mean([x - 1 for x in changes[-5:]])

            changes.append(1 + prc_change)
        except:
            prc_change = growth_rate
            changes.append(1 + prc_change)

    # Initialize the values list with None for all years
    values = [None] * len(years)

    # Find the index of the model value year
    initial_year_index = model_year - start_year # ex. 2030 - 2029 = 1 (index i listen values)

    
    try:
        MMMM_model_year = befolkning.loc[befolkning['Tid'] == model_year, f'{fylke}_Hovedalternativet (MMMM)'].iloc[0]
        scenario_model_year = befolkning.loc[befolkning['Tid'] == model_year, f'{fylke}_{scenario}'].iloc[0]
        scenario_prc_change = ((scenario_model_year - MMMM_model_year) / MMMM_model_year) 
    except:
        scenario_prc_change = 0

    # Set the initial value at its respective year
    values[initial_year_index] = initial_value * (1 + scenario_prc_change) * adj_traffic_factor # ex. ÅDT i år 2030

    # Fill in the values for years before the initial year (decreasing backward)
    for i in range(initial_year_index - 1, -1, -1):
        values[i] = values[i + 1] / changes[i]

    # Fill in the values for years after the initial year (increasing forward)
    for i in range(initial_year_index, len(changes) - 1):
        values[i + 1] = values[i] * changes[i]

    for i in range(len(values)):
        values[i] = values[i] * decay_list[i]
        
    return pd.Series(data=values, index=years, name="Value")

