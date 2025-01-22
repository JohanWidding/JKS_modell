import pandas as pd
from math import prod

from functions.data_preprocessing.common.gen_df_timeseries import generate_timeseries

def kilometer_cost_timeseries(project):

    # Lønnstabell
    price_growth_df = project.price_growth_df
    price_growth_df.iloc[0] = price_growth_df.iloc[0].astype(int)  # Set first row to int
    price_growth_df.iloc[1] = price_growth_df.iloc[1].astype(float)  # Set second row to float

    # Overordnet beskrivelse av hvordan tidseriene skal formes
    start_year = int(project.y_open) # Første året (åpningsåret)
    end_year = int(project.y_open) + int(project.n_y_life) # Siste året (analyse slutt)
    baseline_year = int(project.y_baseline) # Dette er sammenligningsåret
    wage_given_year = int(project.y_carcost) # Dette er året kilometer kostnadene er gitt i
    growth_rate_onwords = project.y_price_growth
    growth_rate_onwords_as_desimal = growth_rate_onwords - 1

    # Bruker lønnstabellen for å finne en vekstfaktor for å finne verdien i åpningsåret (gitt i sammenligningsår-kroner)
    years = [year for year in range(wage_given_year + 1, start_year + 1)]
    # Beregner vekstrater for hvert år i 'years'
    growth_rates = []

    for year in years:
        if year in price_growth_df.iloc[:, 0].values and year <= baseline_year:
            growth_rate = price_growth_df[price_growth_df.iloc[:, 0] == year].iloc[0, 1]
        else:
            growth_rate = growth_rate_onwords

        growth_rates.append(growth_rate)

    # Vekstfaktoren er produktet av vekstrate listen
    growth_factor = prod(growth_rates)

    kilometer_cost_FO_light = (project.cost_FO_L_fuel + project.cost_FO_L_oil_tire + project.cost_FO_L_rep + project.cost_FO_L_capital) * growth_factor
    kilometer_cost_FO_heavy = (project.cost_FO_H_fuel + project.cost_FO_H_oil_tire + project.cost_FO_H_rep + project.cost_FO_H_capital) * growth_factor
    kilometer_cost_EL_light = (project.cost_EL_L_fuel + project.cost_EL_L_oil_tire + project.cost_EL_L_rep + project.cost_EL_L_capital) * growth_factor
    kilometer_cost_EL_heavy = (project.cost_EL_H_fuel + project.cost_EL_H_oil_tire + project.cost_EL_H_rep + project.cost_EL_H_capital) * growth_factor

    # Bruker vektsfaktoren for å skalere timesverdiene
    kilometer_cost_FO_t_rtm = kilometer_cost_FO_light
    kilometer_cost_FO_a_rtm = kilometer_cost_FO_light
    kilometer_cost_FO_f_rtm = kilometer_cost_FO_light
    kilometer_cost_FO_t_ntm = kilometer_cost_FO_light
    kilometer_cost_FO_a_ntm = kilometer_cost_FO_light
    kilometer_cost_FO_f_ntm = kilometer_cost_FO_light

    kilometer_cost_EL_t_rtm = kilometer_cost_EL_light
    kilometer_cost_EL_a_rtm = kilometer_cost_EL_light
    kilometer_cost_EL_f_rtm = kilometer_cost_EL_light
    kilometer_cost_EL_t_ntm = kilometer_cost_EL_light
    kilometer_cost_EL_a_ntm = kilometer_cost_EL_light
    kilometer_cost_EL_f_ntm = kilometer_cost_EL_light

    kilometer_cost_FO_heavy = kilometer_cost_FO_heavy
    kilometer_cost_EL_heavy = kilometer_cost_EL_heavy

    # Genererer tidseriene
    fossil_data = {
        "gods_RTM": generate_timeseries(start_year, end_year, start_year, kilometer_cost_FO_heavy, growth_rate_onwords_as_desimal),
        "fritid_RTM": generate_timeseries(start_year, end_year, start_year, kilometer_cost_FO_f_rtm, growth_rate_onwords_as_desimal),
        "arbeid_RTM": generate_timeseries(start_year, end_year, start_year, kilometer_cost_FO_a_rtm, growth_rate_onwords_as_desimal),
        "tjeneste_RTM": generate_timeseries(start_year, end_year, start_year, kilometer_cost_FO_t_rtm, growth_rate_onwords_as_desimal),
        "fritid_NTM": generate_timeseries(start_year, end_year, start_year, kilometer_cost_FO_f_ntm, growth_rate_onwords_as_desimal),
        "arbeid_NTM": generate_timeseries(start_year, end_year, start_year, kilometer_cost_FO_a_ntm, growth_rate_onwords_as_desimal),
        "tjeneste_NTM": generate_timeseries(start_year, end_year, start_year, kilometer_cost_FO_t_ntm, growth_rate_onwords_as_desimal)}
    electric_data = {
        "gods_RTM": generate_timeseries(start_year, end_year, start_year, kilometer_cost_EL_heavy, growth_rate_onwords_as_desimal),
        "fritid_RTM": generate_timeseries(start_year, end_year, start_year, kilometer_cost_EL_f_rtm, growth_rate_onwords_as_desimal),
        "arbeid_RTM": generate_timeseries(start_year, end_year, start_year, kilometer_cost_EL_a_rtm, growth_rate_onwords_as_desimal),
        "tjeneste_RTM": generate_timeseries(start_year, end_year, start_year, kilometer_cost_EL_t_rtm, growth_rate_onwords_as_desimal),
        "fritid_NTM": generate_timeseries(start_year, end_year, start_year, kilometer_cost_EL_f_ntm, growth_rate_onwords_as_desimal),
        "arbeid_NTM": generate_timeseries(start_year, end_year, start_year, kilometer_cost_EL_a_ntm, growth_rate_onwords_as_desimal),
        "tjeneste_NTM": generate_timeseries(start_year, end_year, start_year, kilometer_cost_EL_t_ntm, growth_rate_onwords_as_desimal)}
    

    fossil_df = pd.DataFrame(fossil_data, index=[year for year in range(start_year, end_year + 1)])
    electric_df = pd.DataFrame(electric_data, index=[year for year in range(start_year, end_year + 1)])

    return fossil_df, electric_df

