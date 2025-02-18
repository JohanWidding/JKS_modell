import numpy as np
import pandas as pd

def gen_linear_timeseries(start_year, end_year, model_year, decreasing_end_year, start_value):
    """
    Genererer en tidsserie med lineær vekst fra startverdien til 1 og deretter lineær nedgang til 0.

    Parametere:
    - start_year: Startåret for tidsserien.
    - end_year: Sluttåret for tidsserien.
    - model_year: Året hvor funksjonen når 1.
    - start_value: Startverdien (mellom 0 og 1).
    - decreasing_end_year: Året hvor funksjonen treffer 0.

    Returnerer:
    - En pandas Series med verdiene for hvert år.
    """
    start_value = 1 + start_value
    # Generer en tidsserie med år fra start til slutt
    years = np.arange(start_year, end_year + 1)
    values = []

    for year in years:
        if year < model_year:
            value = start_value + (1 - start_value) * ((year - start_year) / (model_year - start_year))
        elif year <= decreasing_end_year:
            value = 1 - ((year - model_year) / (decreasing_end_year - model_year))
        else:
            value = 0

        values.append(value)

    # Returnerer en pandas Series med verdiene og år som indeks
    return pd.Series(data=values, index=years, name="Linear Decay")

