import pandas as pd
from math import prod

from functions.data_preprocessing.common.gen_df_timeseries import generate_timeseries

def hour_cost_timeseries(project):

    # Lønnstabell
    wagegrowth_df = project.wage_growth_df
    wagegrowth_df.iloc[0] = wagegrowth_df.iloc[0].astype(int)  # Set first row to int
    wagegrowth_df.iloc[1] = wagegrowth_df.iloc[1].astype(float)  # Set second row to float

    # Overordnet beskrivelse av hvordan tidseriene skal formes
    start_year = int(project.y_open) # Første året (åpningsåret)
    end_year = int(project.y_open) + int(project.n_y_life) # Siste året (analyse slutt)
    baseline_year = int(project.y_baseline) # Dette er sammenligningsåret
    wage_given_year = int(project.y_salary) # Dette er året timesverdiene er gitt i
    growth_rate_onwords = project.y_wage_growth


    # Bruker lønnstabellen for å finne en vekstfaktor for å finne verdien i åpningsåret (gitt i sammenligningsår-kroner)
    years = [year for year in range(wage_given_year + 1, start_year + 1)]
    # Beregner vekstrater for hvert år i 'years'
    growth_rates = []

    for year in years:
        if year in wagegrowth_df.iloc[:, 0].values and year <= baseline_year:
            growth_rate = wagegrowth_df[wagegrowth_df.iloc[:, 0] == year].iloc[0, 1]
        else:
            growth_rate = 1 + growth_rate_onwords

        growth_rates.append(growth_rate)

    # Vekstfaktoren er produktet av vekstrate listen
    growth_factor = prod(growth_rates)

    # Bruker vektsfaktoren for å skalere timesverdiene
    hourcost_driver_t_rtm = project.cost_t_rtm_d * growth_factor
    hourcost_driver_a_rtm = project.cost_a_rtm_d * growth_factor
    hourcost_driver_f_rtm = project.cost_f_rtm_d * growth_factor
    hourcost_driver_a_ntm = project.cost_a_ntm_d * growth_factor
    hourcost_driver_t_ntm = project.cost_t_ntm_d * growth_factor
    hourcost_driver_f_ntm = project.cost_f_ntm_d * growth_factor

    hourcost_passanger_t_rtm = project.cost_t_rtm_p * growth_factor
    hourcost_passanger_a_rtm = project.cost_a_rtm_p * growth_factor
    hourcost_passanger_f_rtm = project.cost_f_rtm_p * growth_factor
    hourcost_passanger_t_ntm = project.cost_t_ntm_p * growth_factor
    hourcost_passanger_a_ntm = project.cost_a_ntm_p * growth_factor
    hourcost_passanger_f_ntm = project.cost_f_ntm_p * growth_factor

    hourcost_driver_heavy = project.cost_H_d * growth_factor

    # Genererer tidseriene
    driver_data = {
        "gods_RTM": generate_timeseries(start_year, end_year, start_year, hourcost_driver_heavy, growth_rate_onwords),
        "fritid_RTM": generate_timeseries(start_year, end_year, start_year, hourcost_driver_f_rtm, growth_rate_onwords),
        "arbeid_RTM": generate_timeseries(start_year, end_year, start_year, hourcost_driver_a_rtm, growth_rate_onwords),
        "tjeneste_RTM": generate_timeseries(start_year, end_year, start_year, hourcost_driver_t_rtm, growth_rate_onwords),
        "fritid_NTM": generate_timeseries(start_year, end_year, start_year, hourcost_driver_f_ntm, growth_rate_onwords),
        "arbeid_NTM": generate_timeseries(start_year, end_year, start_year, hourcost_driver_a_ntm, growth_rate_onwords),
        "tjeneste_NTM": generate_timeseries(start_year, end_year, start_year, hourcost_driver_t_ntm, growth_rate_onwords)}
    passanger_data = {
        "gods_RTM": generate_timeseries(start_year, end_year, start_year, hourcost_driver_heavy, growth_rate_onwords),
        "fritid_RTM": generate_timeseries(start_year, end_year, start_year, hourcost_passanger_f_rtm, growth_rate_onwords),
        "arbeid_RTM": generate_timeseries(start_year, end_year, start_year, hourcost_passanger_a_rtm, growth_rate_onwords),
        "tjeneste_RTM": generate_timeseries(start_year, end_year, start_year, hourcost_passanger_t_rtm, growth_rate_onwords),
        "fritid_NTM": generate_timeseries(start_year, end_year, start_year, hourcost_passanger_f_ntm, growth_rate_onwords),
        "arbeid_NTM": generate_timeseries(start_year, end_year, start_year, hourcost_passanger_a_ntm, growth_rate_onwords),
        "tjeneste_NTM": generate_timeseries(start_year, end_year, start_year, hourcost_passanger_t_ntm, growth_rate_onwords)}
    

    driver_df = pd.DataFrame(driver_data, index=[year for year in range(start_year, end_year + 1)])
    passanger_df = pd.DataFrame(passanger_data, index=[year for year in range(start_year, end_year + 1)])

    return driver_df, passanger_df

