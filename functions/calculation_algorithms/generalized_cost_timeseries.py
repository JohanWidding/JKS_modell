import pandas as pd
from collections import namedtuple
from functions.data_preprocessing.constant_cost.get_constant_cost_timeseries import constant_cost_timeseries
from functions.data_preprocessing.minutes.get_minutes_used_timeseries import minutes_timeseries
from functions.data_preprocessing.time_value.gen_hour_values_timeseries import hour_cost_timeseries
from functions.data_preprocessing.vehicle_cost.gen_kilometer_cost_timeseries import kilometer_cost_timeseries

def generalized_cost_timeseries(project):
    # Definer de viktigste parameterne for tidsserien
    start_year = int(project.y_open)  # Åpningsåret
    end_year = int(project.y_open) + int(project.n_y_life)  # Siste året i analysen
    ratechange_year = int(project.y_open) + int(project.n_y_r1)  # Året hvor renten endres
    early_rate = project.r_1  # Rente før endringen
    late_rate = project.r_2  # Rente etter endringen

    # Antall kilometer i begge alternativene
    kilometers_a0 = project.D_a0
    kilometers_a1 = project.D_a1

    # Litt dobbeltarbeid kansje, men gjør koden mer modelær med at funksjonen har færre input
    # Regner ut tidseriene for kostnader
    driver_df, passanger_df = hour_cost_timeseries(project)
    fossil_df, electric_df = kilometer_cost_timeseries(project)
    const_a0_df, const_a1_df = constant_cost_timeseries(project)
    min_a0_df, min_a1_df = minutes_timeseries(project)

    FO_gc0 = ((driver_df / 60) * min_a0_df) + (fossil_df * kilometers_a0) + const_a0_df
    EL_gc0 = ((driver_df / 60) * min_a0_df) + (electric_df * kilometers_a0) + const_a0_df
    FO_gc1 = ((driver_df / 60) * min_a1_df) + (fossil_df * kilometers_a1) + const_a1_df
    EL_gc1 = ((driver_df / 60) * min_a1_df) + (electric_df * kilometers_a1) + const_a1_df

    passanger_c0 = ((passanger_df / 60) * min_a0_df)
    passanger_c1 = ((passanger_df / 60) * min_a1_df)

    Costs = namedtuple("Costs", [
    "FO_gc0", "EL_gc0", "FO_gc1", "EL_gc1", 
    "passenger_c0", "passenger_c1"
    ])
    

    return Costs(FO_gc0, EL_gc0, FO_gc1, EL_gc1, 
             passanger_c0, passanger_c1)