import pandas as pd
from functions.calculation_algorithms.benefit_calculation import net_benefit
from functions.calculation_algorithms.discounted_net_benefit import discounted_net_benefit
from functions.calculation_algorithms.elasticity_factors_timeseries import elasticity_factors_timeseries
from functions.calculation_algorithms.generalized_cost_timeseries import generalized_cost_timeseries
from functions.data_management.output_excel import save_dfs_to_excel
from functions.data_preprocessing.constant_cost.get_constant_cost_timeseries import constant_cost_timeseries
from functions.data_preprocessing.discounting.get_discounting_timeseries import discounting_timeseries
from functions.data_preprocessing.elasticity.elasticity_timeseries import elasticity_timeseries
from functions.data_preprocessing.minutes.get_minutes_used_timeseries import minutes_timeseries
from functions.data_preprocessing.time_value.gen_hour_values_timeseries import hour_cost_timeseries
from functions.data_preprocessing.traffic_numbers.gen_car_fleet_timeseries import vehicle_group_timeseries
from functions.data_preprocessing.traffic_numbers.gen_passenger_timeseries import passenger_timeseries
from functions.data_preprocessing.traffic_numbers.year_aggregated_passengers import year_aggregated_passengers
from functions.data_preprocessing.traffic_numbers.year_aggregated_traffic import year_aggregated_traffic
from functions.data_preprocessing.vehicle_cost.gen_kilometer_cost_timeseries import kilometer_cost_timeseries

def calculate_project(project, scenario = None):

    project.scenario = scenario

    vehicles_ÅDT = vehicle_group_timeseries(project)
    vehicles_ÅT = year_aggregated_traffic(project)
    passengers_ÅDT = passenger_timeseries(project)
    passengers_ÅT = year_aggregated_passengers(project)
    driver_df, passanger_df = hour_cost_timeseries(project)
    fossil_df, electric_df = kilometer_cost_timeseries(project)
    const_a0_df, const_a1_df = constant_cost_timeseries(project)
    costs = generalized_cost_timeseries(project)
    min_a0_df, min_a1_df = minutes_timeseries(project)
    discounting_df = discounting_timeseries(project)
    elasticity = elasticity_timeseries(project)
    elasticity_factors = elasticity_factors_timeseries(project)
    benefit = net_benefit(project)
    discounted_benefit = discounted_net_benefit(project)

    trafikantnytte = discounted_benefit.total.values.sum()
    formatted_nytte = f"{int(trafikantnytte):,}".replace(",", " ")
    formatted_nytte_EFFEKT = f"{int(project.benefit_EFFEKT)*1000000:,}".replace(",", " ")
    trafikantnytte = pd.DataFrame({'trafikantnytte': [formatted_nytte, formatted_nytte_EFFEKT]})

    dataframe_liste = [
        trafikantnytte,
        vehicles_ÅDT.fossil_a0, 
        vehicles_ÅDT.fossil_a1,
        vehicles_ÅDT.electric_a0, 
        vehicles_ÅDT.electric_a1,
        vehicles_ÅDT.all_a0, 
        vehicles_ÅDT.all_a1,
        vehicles_ÅT.fossil_a0, 
        vehicles_ÅT.fossil_a1,
        vehicles_ÅT.electric_a0, 
        vehicles_ÅT.electric_a1,
        vehicles_ÅT.all_a0, 
        vehicles_ÅT.all_a1,
        passengers_ÅDT.FO_a0,
        passengers_ÅDT.FO_a1,
        passengers_ÅDT.EL_a0,
        passengers_ÅDT.EL_a1,
        passengers_ÅT.FO_a0,
        passengers_ÅT.FO_a1,
        passengers_ÅT.EL_a0,
        passengers_ÅT.EL_a1,
        driver_df,
        passanger_df,
        fossil_df,
        electric_df,
        const_a0_df,
        const_a1_df,
        min_a0_df,
        min_a1_df,
        costs.FO_gc0,
        costs.FO_gc1,
        costs.EL_gc0,
        costs.EL_gc1,
        costs.passenger_c0,
        costs.passenger_c1,
        elasticity,
        elasticity_factors.FO,
        elasticity_factors.EL,
        discounting_df,
        benefit.fossil,
        benefit.electric,
        benefit.passenger,
        benefit.total,
        discounted_benefit.fossil,
        discounted_benefit.electric,
        discounted_benefit.passenger,
        discounted_benefit.total,
        ]
    korresponderende_ark_navn = [
    "Trafikantnytte",
    "Kjøretøy_ÅDT_fossil_a0",
    "Kjøretøy_ÅDT_fossil_a1",
    "Kjøretøy_ÅDT_elektrisk_a0",
    "Kjøretøy_ÅDT_elektrisk_a1",
    "Kjøretøy_ÅDT_alle_a0",
    "Kjøretøy_ÅDT_alle_a1",
    "Kjøretøy_ÅT_fossil_a0",
    "Kjøretøy_ÅT_fossil_a1",
    "Kjøretøy_ÅT_elektrisk_a0",
    "Kjøretøy_ÅT_elektrisk_a1",
    "Kjøretøy_ÅT_alle_a0",
    "Kjøretøy_ÅT_alle_a1",
    "Passasjerer_ÅDT_fossil_a0",
    "Passasjerer_ÅDT_fossil_a1",
    "Passasjerer_ÅDT_elektrisk_a0",
    "Passasjerer_ÅDT_elektrisk_a1",
    "Passasjerer_ÅT_fossil_a0",
    "Passasjerer_ÅT_fossil_a1",
    "Passasjerer_ÅT_elektrisk_a0",
    "Passasjerer_ÅT_elektrisk_a1",
    "Timekostnader_Sjårfør",
    "Timekostnader_Passasjer",
    "Kilometerkostnad_fossil",
    "Kilometerkostnad_elektrisk",
    "Konstantledd_a0",
    "Konstantledd_a1",
    "Minutter_a0",
    "Minutter_a1",
    "Generaliserte_kostnader_FO_a0",
    "Generaliserte_kostnader_FO_a1",
    "Generaliserte_kostnader_EL_a0",
    "Generaliserte_kostnader_EL_a1",
    "Generaliserte_kostnader_passasjer_a0",
    "Generaliserte_kostnader_passasjer_a1",
    "Elastisitet",
    "Elastisitetsfaktorer_FO_sjåfør",
    "Elastisitetsfaktorer_EL_sjåfør",
    "Diskontering",
    "Nytte_fossil",
    "Nytte_elektrisk",
    "Nytte_passasjer",
    "Nytte_total",
    "Diskontert_nytte_fossil",
    "Diskontert_nytte_elektrisk",
    "Diskontert_nytte_passasjer",
    "Diskontert_nytte_total",
]

    save_dfs_to_excel(f"{project.name.replace("/", "-")}_{str(scenario)}", dataframe_liste, "./Output/", sheet_names=korresponderende_ark_navn)

    return discounted_benefit.total.values.sum()



        