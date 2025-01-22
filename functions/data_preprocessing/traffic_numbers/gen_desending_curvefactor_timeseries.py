import numpy as np
import pandas as pd

def gen_curvefactor_timeseries(start_year, end_year, model_year, decreasing_end_year, factor):
    # Genererer en tidsserie med år fra start til slutt
    years = np.arange(start_year, end_year + 1)

    # Definerer det maksimale og minimale året for beregning
    max_val = decreasing_end_year
    min_val = model_year

    range_diff = max_val - min_val
    values = []

    for year in years:
        if year < model_year:
            value = 1  # Holder verdien på 1 frem til model_year
        elif year <= decreasing_end_year:
            A3 = year - model_year
            value = 1 * ((1 - A3 / range_diff) ** factor)
            if value < 0:
                value = 0
        else:
            value = 0
        values.append(value)

    # Returnerer en pandas Series med verdiene og år som indeks
    return pd.Series(data=values, index=years, name="Decay")