import pandas as pd

def discounting_timeseries(project):
    # Definer de viktigste parameterne for tidsserien
    start_year = int(project.y_open)  # Åpningsåret
    end_year = int(project.y_open) + int(project.n_y_life)  # Siste året i analysen
    ratechange_year = int(project.y_open) + int(project.n_y_r1)  # Året hvor renten endres
    early_rate = project.r_1  # Rente før endringen
    late_rate = project.r_2  # Rente etter endringen

    # Opprett en DataFrame med årene
    years = list(range(start_year, end_year + 1))
    timeseries_df = pd.DataFrame({'Year': years})

    # Beregn diskonteringsfaktorene
    timeseries_df['Discount Factor'] = 1.0  # Initialiser diskonteringsfaktoren for det første året

    for i in range(1, len(timeseries_df)):
        prev_factor = timeseries_df.loc[i - 1, 'Discount Factor']
        current_year = timeseries_df.loc[i, 'Year']

        # Bestem diskonteringsrenten basert på året
        if current_year <= ratechange_year:
            current_rate = early_rate
        else:
            current_rate = late_rate

        # Beregn diskonteringsfaktoren for det nåværende året
        timeseries_df.loc[i, 'Discount Factor'] = prev_factor / (1 + current_rate)

    # Sett året som indeks
    timeseries_df.set_index('Year', inplace=True)

    return timeseries_df
