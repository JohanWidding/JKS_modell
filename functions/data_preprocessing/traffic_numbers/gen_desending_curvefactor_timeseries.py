import numpy as np
import pandas as pd

def gen_linear_timeseries(start_year, end_year, model_year, decreasing_end_year, share_start, share_model_year):
    """
    Genererer en tidsserie med lineær vekst fra startverdien til 1 og deretter lineær nedgang til 0.
    
    Parametere:
    - start_year: Startåret for tidsserien.
    - end_year: Sluttåret for tidsserien.
    - model_year: Året hvor funksjonen når 1.
    - decreasing_end_year: Året hvor funksjonen treffer 0.
    - share_start: Startverdien (mellom 0 og 1).
    - share_model_year: Andel ved model_year.

    Returnerer:
    - En pandas Series med verdiene for hvert år.
    """
    years = np.arange(start_year, end_year + 1)
    values = []

    if share_start >= share_model_year:
        # Beholder original logikk dersom startandelen er større enn eller lik modelandelen
        start_value = share_start / share_model_year  # Prosentvis endring fra andel til modell år til start år.
        for year in years:
            if year < model_year:
                value = start_value + ((year - start_year) / (model_year - start_year))
            elif year <= decreasing_end_year:
                value = 1 - ((year - model_year) / (decreasing_end_year - model_year))
            else:
                value = 0
            values.append(value)
    else:
        # Bruker ny logikk dersom startandelen er mindre enn modelandelen
        for year in years:
            if year < model_year:
                value = share_start + (share_model_year - share_start) * ((year - start_year) / (model_year - start_year))
            elif year <= decreasing_end_year:
                value = 1 - ((year - model_year) / (decreasing_end_year - model_year))
            else:
                value = 0
            values.append(value)

    return pd.Series(data=values, index=years, name="Linear Decay")

if __name__ == "__main__":
    # Testkjøring
    series1 = gen_linear_timeseries(2029, 2060, 2036, 2050, 0.8, 0.5)  # Beholder original logikk
    series2 = gen_linear_timeseries(2029, 2060, 2036, 2050, 0.6, 1)  # Bruker ny logikk
    
    print(series1)
    print(series2)
