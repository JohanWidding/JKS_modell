from collections import namedtuple
import pandas as pd


try:
    from functions.calculation_algorithms.elasticity_factors_timeseries import elasticity_factors_timeseries
    from functions.data_preprocessing.traffic_numbers.gen_desending_curvefactor_timeseries import gen_linear_timeseries
    from functions.data_preprocessing.traffic_numbers.gen_timeseries import generate_timeseries
    from functions.data_preprocessing.traffic_numbers.logistic_decay_list import logistic_decay_values
except ModuleNotFoundError:
    import sys
    import os

    # Append the project root directory dynamically
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

    # Retry import after fixing sys.path
    from functions.calculation_algorithms.elasticity_factors_timeseries import elasticity_factors_timeseries
    from functions.data_preprocessing.traffic_numbers.gen_desending_curvefactor_timeseries import gen_linear_timeseries
    from functions.data_preprocessing.traffic_numbers.gen_timeseries import generate_timeseries
    from functions.data_preprocessing.traffic_numbers.logistic_decay_list import logistic_decay_values


def vehicle_group_timeseries(project):

    # Overordnet beskrivelse av hvordan tidseriene skal formes
    start_year = int(project.y_open) # Første året (åpningsåret)
    end_year = int(project.y_open) + int(project.n_y_life) # Siste året (analyse slutt)
    model_year = int(project.y_model) # Dette er året ÅDT tallene fra transportmodellen er beregnet for
    growth_rate_gods = project.H_g
    growth_rate_RTM = project.L_g_rtm
    growth_rate_NTM = project.L_g_ntm
    

    # Antall fossildrevene kjøretøy i de ulike reisehensikt-gruppene (ANTALL biler i modell året)
    FO_gods_RTM = project.gods * project.share_fossil_H_model
    FO_fritid_RTM = (project.FO_f + project.FO_hl + project.FO_p + project.FO_ap)
    FO_arbeid_RTM = project.FO_a
    FO_tjeneste_RTM = project.FO_t 
    FO_fritid_NTM = project.FO_ntm * project.FO_f_share_ntm
    FO_arbeid_NTM = project.FO_ntm * project.FO_a_share_ntm
    FO_tjeneste_NTM = project.FO_ntm * project.FO_t_share_ntm

    # Antall elektriske kjøretøy i de ulike reisehensikt-gruppene (ANTALL biler i modell året)
    EL_gods_RTM = project.gods * (1 - project.share_fossil_H_model) 
    EL_fritid_RTM = (project.EL_f + project.EL_hl + project.EL_p + project.EL_ap)
    EL_arbeid_RTM = project.EL_a
    EL_tjeneste_RTM = project.EL_t
    EL_fritid_NTM = project.EL_ntm * project.EL_f_share_ntm
    EL_arbeid_NTM = project.EL_ntm * project.EL_a_share_ntm
    EL_tjeneste_NTM = project.EL_ntm * project.EL_t_share_ntm

    sum_EL = project.EL_ntm + EL_tjeneste_RTM + EL_arbeid_RTM + EL_fritid_RTM
    sum_FO = project.FO_ntm + FO_tjeneste_RTM + FO_arbeid_RTM + FO_fritid_RTM

    end_year_of_fossil_light = project.y_nofossil_L
    end_year_of_fossil_heavy = project.y_nofossil_H
    share_fossil_light_open = project.share_fossil_L_open
    share_fossil_heavy_open = project.share_fossil_H_open
    
    share_fossil_light_model_ntm = 0.0001 if (project.FO_ntm + project.EL_ntm) == 0 else project.FO_ntm / (project.FO_ntm + project.EL_ntm)
    share_fossil_light_model_f = 0.0001 if (FO_fritid_RTM + EL_fritid_RTM) == 0 else FO_fritid_RTM / (FO_fritid_RTM + EL_fritid_RTM)
    share_fossil_light_model_a = 0.0001 if (FO_arbeid_RTM + EL_arbeid_RTM) == 0 else FO_arbeid_RTM / (FO_arbeid_RTM + EL_arbeid_RTM)
    share_fossil_light_model_t = 0.0001 if (FO_tjeneste_RTM + EL_tjeneste_RTM) == 0 else FO_tjeneste_RTM / (FO_tjeneste_RTM + EL_tjeneste_RTM)
    share_fossil_heavy_model = project.share_fossil_H_model

    # Ukategorisert (Sverigeturer og flyplassreiser)
    U_swe_fly = project.CD_sverige + project.CD_flyplass
    FO_swe_fly = U_swe_fly * share_fossil_light_model_ntm
    EL_swe_fly = U_swe_fly - FO_swe_fly
    # Kategoriserer disse som fritidsreisende
    # Fritidsreisende har lavest tidsverdi
    FO_fritid_NTM += FO_swe_fly
    EL_fritid_NTM += EL_swe_fly

    # Generer faktor-serier for å kunne justere på andelen elektriske kjøretøy i forhold til fossildrevne. (elektriske kjøretøy andel øker, fossildrevne andel synker)
    decay_series_light_NTM = gen_linear_timeseries(start_year, end_year, model_year, end_year_of_fossil_light, share_fossil_light_open, share_fossil_light_model_ntm)
    decay_series_light_f = gen_linear_timeseries(start_year, end_year, model_year, end_year_of_fossil_light, share_fossil_light_open, share_fossil_light_model_f)
    decay_series_light_a = gen_linear_timeseries(start_year, end_year, model_year, end_year_of_fossil_light, share_fossil_light_open, share_fossil_light_model_a)
    decay_series_light_t = gen_linear_timeseries(start_year, end_year, model_year, end_year_of_fossil_light, share_fossil_light_open, share_fossil_light_model_t)
    decay_series_heavy = gen_linear_timeseries(start_year, end_year, model_year, end_year_of_fossil_heavy, share_fossil_heavy_open, share_fossil_heavy_model)


    # Dersom noen trafikantgrupper skal variere ekstraordinært. ex. Mer hjemmekontor -> tjenestereisende avtar
    decay_factors_non = [1 for i in range(100)]
    decay_factors_tjeneste = logistic_decay_values(t0=project.midt_y_t, x=project.midt_bunn_t)
    decay_factors_arbeid = logistic_decay_values(t0=project.midt_y_a, x=project.midt_bunn_a)
    decay_factors_fritid = logistic_decay_values(t0=project.midt_y_f, x=project.midt_bunn_f)

    # Genererer tidseriene
    fossil_to_electric = {
        "gods_RTM": generate_timeseries(project, FO_gods_RTM, growth_rate_gods, decay_factors_non) * (decay_series_heavy),
        "fritid_RTM": generate_timeseries(project, FO_fritid_RTM, growth_rate_RTM, decay_factors_fritid) * (decay_series_light_f),
        "arbeid_RTM": generate_timeseries(project, FO_arbeid_RTM, growth_rate_RTM, decay_factors_arbeid) * (decay_series_light_a),
        "tjeneste_RTM": generate_timeseries(project, FO_tjeneste_RTM, growth_rate_RTM, decay_factors_tjeneste) * (decay_series_light_t),
        "fritid_NTM": generate_timeseries(project, FO_fritid_NTM, growth_rate_NTM, decay_factors_fritid) * (decay_series_light_NTM),
        "arbeid_NTM": generate_timeseries(project, FO_arbeid_NTM, growth_rate_NTM, decay_factors_arbeid) * (decay_series_light_NTM),
        "tjeneste_NTM": generate_timeseries(project, FO_tjeneste_NTM, growth_rate_NTM, decay_factors_tjeneste) * (decay_series_light_NTM)}
    # Bilene som "forsvinner" ovenfor i fossil_data blir til elbiler
    fossil_data = {
        "gods_RTM": generate_timeseries(project, FO_gods_RTM, growth_rate_gods, decay_factors_non),
        "fritid_RTM": generate_timeseries(project, FO_fritid_RTM, growth_rate_RTM, decay_factors_fritid),
        "arbeid_RTM": generate_timeseries(project, FO_arbeid_RTM, growth_rate_RTM, decay_factors_arbeid),
        "tjeneste_RTM": generate_timeseries(project, FO_tjeneste_RTM, growth_rate_RTM, decay_factors_tjeneste),
        "fritid_NTM": generate_timeseries(project, FO_fritid_NTM, growth_rate_NTM, decay_factors_fritid),
        "arbeid_NTM": generate_timeseries(project, FO_arbeid_NTM, growth_rate_NTM, decay_factors_arbeid),
        "tjeneste_NTM": generate_timeseries(project, FO_tjeneste_NTM, growth_rate_NTM, decay_factors_tjeneste)
    }
    electric_data = {
        "gods_RTM": generate_timeseries(project, EL_gods_RTM, growth_rate_gods, decay_factors_non),
        "fritid_RTM": generate_timeseries(project, EL_fritid_RTM, growth_rate_RTM, decay_factors_fritid),
        "arbeid_RTM": generate_timeseries(project, EL_arbeid_RTM, growth_rate_RTM, decay_factors_arbeid),
        "tjeneste_RTM": generate_timeseries(project, EL_tjeneste_RTM, growth_rate_RTM, decay_factors_tjeneste),
        "fritid_NTM": generate_timeseries(project, EL_fritid_NTM, growth_rate_NTM, decay_factors_fritid),
        "arbeid_NTM": generate_timeseries(project, EL_arbeid_NTM, growth_rate_NTM, decay_factors_arbeid),
        "tjeneste_NTM": generate_timeseries(project, EL_tjeneste_NTM, growth_rate_NTM, decay_factors_tjeneste)
    }
    

    # Create DataFrames for fossil and electric
    
    fossil_to_electric_df = pd.DataFrame(fossil_to_electric, index=decay_series_light_NTM.index)
    fossil_df = pd.DataFrame(fossil_data, index=decay_series_light_NTM.index)
    #Legger sammen de elektiske bilene og de fossildrevene bilene som har overgått til el
    electric_df = pd.DataFrame(electric_data, index=decay_series_light_NTM.index) + (fossil_df - fossil_to_electric_df)
    fossil_df = fossil_to_electric_df.copy()
    
    
    
    elasticity_factors = elasticity_factors_timeseries(project)

    traffic_EL_a0 = electric_df * elasticity_factors.EL
    traffic_FO_a0 = fossil_df * elasticity_factors.FO

    # Create DataFrame for total ÅDT numbers
    total_df_a0 = traffic_FO_a0 + traffic_EL_a0
    total_df_a1 = fossil_df + electric_df


    # Create a named tuple for the return
    AADTDataFrames = namedtuple('AADTDataFrames', ['fossil_a0', 'electric_a0', 'fossil_a1', 'electric_a1', 'all_a0', 'all_a1'])
    
    return AADTDataFrames(fossil_a0=traffic_FO_a0, electric_a0=traffic_EL_a0, fossil_a1=fossil_df, electric_a1=electric_df, all_a0=total_df_a0, all_a1=total_df_a1)



if __name__ == "__main__":
    # Try importing again
    from functions.data_management.load_project_data import load_data

    # Load the first project from the "Prosjekter" dataset
    project = load_data(project_file_name="Prosjekter").projects[0]

    # Run the function
    aadt_data = vehicle_group_timeseries(project)

    print(aadt_data.fossil_a1)
    print(aadt_data.electric_a1)

