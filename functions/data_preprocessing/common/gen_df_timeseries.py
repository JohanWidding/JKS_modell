import pandas as pd

def generate_timeseries(start_year, end_year, initial_year, initial_value, growth_rate):
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
    years = range(start_year, end_year + 1)
    values = [initial_value * ((1 + growth_rate) ** (year - initial_year)) for year in years]
    
    return pd.Series(data=values, index=years, name="Value")

