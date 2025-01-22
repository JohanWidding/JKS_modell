

import pandas as pd
from functions.data_preprocessing.common.gen_df_timeseries import generate_timeseries


def constant_cost_timeseries(project):
    # Definer de viktigste parameterne for tidsserien
    start_year = int(project.y_open)  # Åpningsåret
    end_year = int(project.y_open) + int(project.n_y_life)  # Siste året i analysen
    growth_rate = 0 # Restleddet er konstant for alle år

    # Henter restledd
    L_rest_a0 = project.L_rest_a0
    L_rest_a1 = project.L_rest_a1
    H_rest_a0 = project.H_rest_a0
    H_rest_a1 = project.H_rest_a1

    a0_data = {
        "gods_RTM": generate_timeseries(start_year, end_year, start_year, H_rest_a0, growth_rate),
        "fritid_RTM": generate_timeseries(start_year, end_year, start_year, L_rest_a0, growth_rate),
        "arbeid_RTM": generate_timeseries(start_year, end_year, start_year, L_rest_a0, growth_rate),
        "tjeneste_RTM": generate_timeseries(start_year, end_year, start_year, L_rest_a0, growth_rate),
        "fritid_NTM": generate_timeseries(start_year, end_year, start_year, L_rest_a0, growth_rate),
        "arbeid_NTM": generate_timeseries(start_year, end_year, start_year, L_rest_a0, growth_rate),
        "tjeneste_NTM": generate_timeseries(start_year, end_year, start_year, L_rest_a0, growth_rate)}
    a1_data = {
        "gods_RTM": generate_timeseries(start_year, end_year, start_year, H_rest_a1, growth_rate),
        "fritid_RTM": generate_timeseries(start_year, end_year, start_year, L_rest_a1, growth_rate),
        "arbeid_RTM": generate_timeseries(start_year, end_year, start_year, L_rest_a1, growth_rate),
        "tjeneste_RTM": generate_timeseries(start_year, end_year, start_year, L_rest_a1, growth_rate),
        "fritid_NTM": generate_timeseries(start_year, end_year, start_year, L_rest_a1, growth_rate),
        "arbeid_NTM": generate_timeseries(start_year, end_year, start_year, L_rest_a1, growth_rate),
        "tjeneste_NTM": generate_timeseries(start_year, end_year, start_year, L_rest_a1, growth_rate)}
    

    a0_df = pd.DataFrame(a0_data, index=[year for year in range(start_year, end_year + 1)])
    a1_df = pd.DataFrame(a1_data, index=[year for year in range(start_year, end_year + 1)])

    return a0_df, a1_df