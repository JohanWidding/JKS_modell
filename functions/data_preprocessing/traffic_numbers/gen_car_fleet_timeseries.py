import pandas as pd
from collections import namedtuple
from functions.calculation_algorithms.elasticity_factors_timeseries import elasticity_factors_timeseries
from functions.data_preprocessing.traffic_numbers.gen_desending_curvefactor_timeseries import gen_curvefactor_timeseries
from functions.data_preprocessing.traffic_numbers.gen_timeseries import generate_timeseries

def vehicle_group_timeseries(project):

    # Overordnet beskrivelse av hvordan tidseriene skal formes
    start_year = int(project.y_open) # Første året (åpningsåret)
    end_year = int(project.y_open) + int(project.n_y_life) # Siste året (analyse slutt)
    model_year = int(project.y_model) # Dette er året ÅDT tallene fra transportmodellen er beregnet for
    growth_rate_gods = project.H_g
    growth_rate_RTM = project.L_g_rtm
    growth_rate_NTM = project.L_g_ntm
    end_year_of_fossil_light = project.y_nofossil_L
    end_year_of_fossil_heavy = project.y_nofossil_H
    decay_factor_fossil_light = project.curvature_fossil_L
    decay_factor_fossil_heavy = project.curvature_fossil_H

    # Antall fossildrevene kjøretøy i de ulike reisehensikt-gruppene (ANTALL biler i modell året)
    FO_gods_RTM = project.gods * project.H_FO_share
    FO_fritid_RTM = (project.FO_f + project.FO_hl + project.FO_p + project.FO_ap)
    FO_arbeid_RTM = project.FO_a
    FO_tjeneste_RTM = project.FO_t 
    FO_fritid_NTM = project.FO_ntm * project.FO_f_share_ntm
    FO_arbeid_NTM = project.FO_ntm * project.FO_a_share_ntm
    FO_tjeneste_NTM = project.FO_ntm * project.FO_t_share_ntm

    # Antall elektriske kjøretøy i de ulike reisehensikt-gruppene (ANTALL biler i modell året)
    EL_gods_RTM = project.gods * (1 - project.H_FO_share) if project.H_FO_share != 0 else 1
    EL_fritid_RTM = (project.EL_f + project.EL_hl + project.EL_p + project.EL_ap)
    EL_arbeid_RTM = project.EL_a
    EL_tjeneste_RTM = project.EL_t
    EL_fritid_NTM = project.EL_ntm * project.EL_f_share_ntm
    EL_arbeid_NTM = project.EL_ntm * project.EL_a_share_ntm
    EL_tjeneste_NTM = project.EL_ntm * project.EL_t_share_ntm

    # Generer faktorserier for å kunne justere på andelen elektriske kjøretøy i forhold til fossildrevne. (elektriske kjøretøy øker, fossildrevne synker)
    decay_series_light = gen_curvefactor_timeseries(start_year, end_year, model_year, end_year_of_fossil_light, decay_factor_fossil_light)
    decay_series_heavy = gen_curvefactor_timeseries(start_year, end_year, model_year, end_year_of_fossil_heavy, decay_factor_fossil_heavy)
    incremental_series_light = (1 - decay_series_light)
    incremental_series_heavy = (1 - decay_series_heavy)

    # Genererer tidseriene
    fossil_data = {
        "gods_RTM": generate_timeseries(project, FO_gods_RTM, growth_rate_gods) * (decay_series_heavy),
        "fritid_RTM": generate_timeseries(project, FO_fritid_RTM, growth_rate_RTM) * (decay_series_light),
        "arbeid_RTM": generate_timeseries(project, FO_arbeid_RTM, growth_rate_RTM) * (decay_series_light),
        "tjeneste_RTM": generate_timeseries(project, FO_tjeneste_RTM, growth_rate_RTM) * (decay_series_light),
        "fritid_NTM": generate_timeseries(project, FO_fritid_NTM, growth_rate_NTM) * (decay_series_light),
        "arbeid_NTM": generate_timeseries(project, FO_arbeid_NTM, growth_rate_NTM) * (decay_series_light),
        "tjeneste_NTM": generate_timeseries(project, FO_tjeneste_NTM, growth_rate_NTM) * (decay_series_light)}
    # Bilene som "forsvinner" ovenfor i fossil_data bli til elbiler
    fossil_to_electric = {
        "gods_RTM": generate_timeseries(project, FO_gods_RTM, growth_rate_gods) * (incremental_series_heavy),
        "fritid_RTM": generate_timeseries(project, FO_fritid_RTM, growth_rate_RTM) * (incremental_series_light),
        "arbeid_RTM": generate_timeseries(project, FO_arbeid_RTM, growth_rate_RTM) * (incremental_series_light),
        "tjeneste_RTM": generate_timeseries(project, FO_tjeneste_RTM, growth_rate_RTM) * (incremental_series_light),
        "fritid_NTM": generate_timeseries(project, FO_fritid_NTM, growth_rate_NTM) * (incremental_series_light),
        "arbeid_NTM": generate_timeseries(project, FO_arbeid_NTM, growth_rate_NTM) * (incremental_series_light),
        "tjeneste_NTM": generate_timeseries(project, FO_tjeneste_NTM, growth_rate_NTM) * (incremental_series_light) 
    }
    electric_data = {
        "gods_RTM": generate_timeseries(project, EL_gods_RTM, growth_rate_gods),
        "fritid_RTM": generate_timeseries(project, EL_fritid_RTM, growth_rate_RTM),
        "arbeid_RTM": generate_timeseries(project, EL_arbeid_RTM, growth_rate_RTM),
        "tjeneste_RTM": generate_timeseries(project, EL_tjeneste_RTM, growth_rate_RTM),
        "fritid_NTM": generate_timeseries(project, EL_fritid_NTM, growth_rate_NTM),
        "arbeid_NTM": generate_timeseries(project, EL_arbeid_NTM, growth_rate_NTM),
        "tjeneste_NTM": generate_timeseries(project, EL_tjeneste_NTM, growth_rate_NTM)
    }
    

    # Create DataFrames for fossil and electric
    fossil_df = pd.DataFrame(fossil_data, index=decay_series_light.index)
    fossil_to_electric_df = pd.DataFrame(fossil_to_electric, index=decay_series_light.index)
    electric_df = pd.DataFrame(electric_data, index=decay_series_light.index) + fossil_to_electric_df
    
    
    elasticity_factors = elasticity_factors_timeseries(project)

    traffic_EL_a0 = electric_df * elasticity_factors.EL
    traffic_FO_a0 = fossil_df * elasticity_factors.FO

    # Create DataFrame for total ÅDT numbers
    total_df_a0 = traffic_FO_a0 + traffic_EL_a0
    total_df_a1 = fossil_df + electric_df


    # Create a named tuple for the return
    AADTDataFrames = namedtuple('AADTDataFrames', ['fossil_a0', 'electric_a0', 'fossil_a1', 'electric_a1', 'all_a0', 'all_a1'])
    
    return AADTDataFrames(fossil_a0=traffic_FO_a0, electric_a0=traffic_EL_a0, fossil_a1=fossil_df, electric_a1=electric_df, all_a0=total_df_a0, all_a1=total_df_a1)



