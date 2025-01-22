import pandas as pd

from functions.data_preprocessing.common.gen_df_timeseries import generate_timeseries

def elasticity_timeseries(project):
    # Definer de viktigste parameterne for tidsserien
    start_year = int(project.y_open)  # Åpningsåret
    end_year = int(project.y_open) + int(project.n_y_life)  # Siste året i analysen
    growth_rate = 0 # elastisiteten er konstant for alle år


    # Henter elastisitet-verdiene
    el_t_rtm = project.L_t_elasticity_rtm
    el_a_rtm = project.L_a_elasticity_rtm
    el_f_rtm = project.L_f_elasticity_rtm
    el_t_ntm = project.L_t_elasticity_ntm
    el_a_ntm = project.L_a_elasticity_ntm
    el_f_ntm = project.L_f_elasticity_ntm
    el_heavy = project.H_elasticity

    el_data = {
        "gods_RTM": generate_timeseries(start_year, end_year, start_year, el_heavy, growth_rate),
        "fritid_RTM": generate_timeseries(start_year, end_year, start_year, el_f_rtm, growth_rate),
        "arbeid_RTM": generate_timeseries(start_year, end_year, start_year, el_a_rtm, growth_rate),
        "tjeneste_RTM": generate_timeseries(start_year, end_year, start_year, el_t_rtm, growth_rate),
        "fritid_NTM": generate_timeseries(start_year, end_year, start_year, el_f_ntm, growth_rate),
        "arbeid_NTM": generate_timeseries(start_year, end_year, start_year, el_a_ntm, growth_rate),
        "tjeneste_NTM": generate_timeseries(start_year, end_year, start_year, el_t_ntm, growth_rate)
    }
    

    el_df = pd.DataFrame(el_data, index=[year for year in range(start_year, end_year + 1)])

    

    return el_df