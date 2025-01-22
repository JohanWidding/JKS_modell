

import pandas as pd
from functions.data_preprocessing.common.gen_df_timeseries import generate_timeseries


def minutes_timeseries(project):
    # Definer de viktigste parameterne for tidsserien
    start_year = int(project.y_open)  # Åpningsåret
    end_year = int(project.y_open) + int(project.n_y_life)  # Siste året i analysen
    growth_rate = 0 # Tidsbruken er konstant for alle år

    # Henter tidsbruken i de ulike alternativene for lette og tunge kjøretøy
    minutes_a0_light = project.TL_a0
    minutes_a0_heavy = project.TH_a0
    minutes_a1_light = project.TL_a1
    minutes_a1_heavy = project.TH_a1

    a0_data = {
        "gods_RTM": generate_timeseries(start_year, end_year, start_year, minutes_a0_heavy, growth_rate),
        "fritid_RTM": generate_timeseries(start_year, end_year, start_year, minutes_a0_light, growth_rate),
        "arbeid_RTM": generate_timeseries(start_year, end_year, start_year, minutes_a0_light, growth_rate),
        "tjeneste_RTM": generate_timeseries(start_year, end_year, start_year, minutes_a0_light, growth_rate),
        "fritid_NTM": generate_timeseries(start_year, end_year, start_year, minutes_a0_light, growth_rate),
        "arbeid_NTM": generate_timeseries(start_year, end_year, start_year, minutes_a0_light, growth_rate),
        "tjeneste_NTM": generate_timeseries(start_year, end_year, start_year, minutes_a0_light, growth_rate)}
    a1_data = {
        "gods_RTM": generate_timeseries(start_year, end_year, start_year, minutes_a1_heavy, growth_rate),
        "fritid_RTM": generate_timeseries(start_year, end_year, start_year, minutes_a1_light, growth_rate),
        "arbeid_RTM": generate_timeseries(start_year, end_year, start_year, minutes_a1_light, growth_rate),
        "tjeneste_RTM": generate_timeseries(start_year, end_year, start_year, minutes_a1_light, growth_rate),
        "fritid_NTM": generate_timeseries(start_year, end_year, start_year, minutes_a1_light, growth_rate),
        "arbeid_NTM": generate_timeseries(start_year, end_year, start_year, minutes_a1_light, growth_rate),
        "tjeneste_NTM": generate_timeseries(start_year, end_year, start_year, minutes_a1_light, growth_rate)}
    

    a0_df = pd.DataFrame(a0_data, index=[year for year in range(start_year, end_year + 1)])
    a1_df = pd.DataFrame(a1_data, index=[year for year in range(start_year, end_year + 1)])

    return a0_df, a1_df