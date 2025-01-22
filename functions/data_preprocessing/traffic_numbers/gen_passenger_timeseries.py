
from collections import namedtuple

import pandas as pd
from functions.calculation_algorithms.elasticity_factors_timeseries import elasticity_factors_timeseries
from functions.data_preprocessing.common.gen_df_timeseries import generate_timeseries
from functions.data_preprocessing.traffic_numbers.gen_car_fleet_timeseries import vehicle_group_timeseries


def passenger_timeseries(project):

    # Overordnet beskrivelse av hvordan tidseriene skal formes
    start_year = int(project.y_open) # Første året (åpningsåret)
    end_year = int(project.y_open) + int(project.n_y_life) # Siste året (analyse slutt)
    model_year = int(project.y_model) # Dette er året ÅDT tallene fra transportmodellen er beregnet for
    growth_rate_gods = project.H_g
    growth_rate_RTM = project.L_g_rtm
    growth_rate_NTM = project.L_g_ntm
    years = [year for year in range(start_year, end_year + 1)]

    vehicles_ÅDT = vehicle_group_timeseries(project)
    elasticity_factors = elasticity_factors_timeseries(project)

    # Andel som kjører elektrisk og andelen som kjører fossil
    share_electric_a0 = vehicles_ÅDT.electric_a0 / vehicles_ÅDT.all_a0
    share_fossil_a0 = vehicles_ÅDT.fossil_a0 / vehicles_ÅDT.all_a0
    share_electric_a1 = vehicles_ÅDT.electric_a1 / vehicles_ÅDT.all_a1
    share_fossil_a1 = vehicles_ÅDT.fossil_a1 / vehicles_ÅDT.all_a1

    CP_heavy_rtm = 0
    CP_t_rtm = project.CP_t
    CP_a_rtm = project.CP_a 
    CP_f_rtm = (project.CP_f + project.CP_hl + project.CP_p + project.CP_ap)
    CP_t_ntm = project.CP_ntm * project.CP_t_share_ntm
    CP_a_ntm = project.CP_ntm * project.CP_a_share_ntm
    CP_f_ntm = project.CP_ntm * project.CP_f_share_ntm

    # Genererer tidseriene
    passenger_data = {
        "gods_RTM": generate_timeseries(start_year, end_year, model_year, CP_heavy_rtm, growth_rate_gods),
        "fritid_RTM": generate_timeseries(start_year, end_year, model_year, CP_t_rtm, growth_rate_RTM),
        "arbeid_RTM": generate_timeseries(start_year, end_year, model_year, CP_a_rtm, growth_rate_RTM),
        "tjeneste_RTM": generate_timeseries(start_year, end_year, model_year, CP_f_rtm, growth_rate_RTM),
        "fritid_NTM": generate_timeseries(start_year, end_year, model_year, CP_t_ntm, growth_rate_NTM),
        "arbeid_NTM": generate_timeseries(start_year, end_year, model_year, CP_a_ntm, growth_rate_NTM),
        "tjeneste_NTM": generate_timeseries(start_year, end_year, model_year, CP_f_ntm, growth_rate_NTM)}

    passenger_a1_all = pd.DataFrame(passenger_data, index=years)

    CP_t_EL_rtm_a0 = passenger_a1_all * share_electric_a0 * elasticity_factors.EL
    CP_t_FO_rtm_a0 = passenger_a1_all * share_fossil_a0 * elasticity_factors.FO
    CP_t_EL_rtm_a1 = passenger_a1_all * share_electric_a1
    CP_t_FO_rtm_a1 = passenger_a1_all * share_fossil_a1



    # Create a named tuple for the return
    AADTDataFrames = namedtuple('PassengerDataFrames', ['EL_a0','EL_a1', 'FO_a0','FO_a1'])
    
    return AADTDataFrames(CP_t_EL_rtm_a0, CP_t_EL_rtm_a1, CP_t_FO_rtm_a0, CP_t_FO_rtm_a1)


