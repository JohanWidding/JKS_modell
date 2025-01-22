import pandas as pd
from collections import namedtuple
from functions.calculation_algorithms.generalized_cost_timeseries import generalized_cost_timeseries
from functions.data_preprocessing.constant_cost.get_constant_cost_timeseries import constant_cost_timeseries
from functions.data_preprocessing.elasticity.elasticity_timeseries import elasticity_timeseries
from functions.data_preprocessing.minutes.get_minutes_used_timeseries import minutes_timeseries
from functions.data_preprocessing.time_value.gen_hour_values_timeseries import hour_cost_timeseries
from functions.data_preprocessing.vehicle_cost.gen_kilometer_cost_timeseries import kilometer_cost_timeseries

def elasticity_factors_timeseries(project):


    gc = generalized_cost_timeseries(project)
    el = elasticity_timeseries(project)


    # elasticity_factor = (cost_before / cost_after) ** el

    # Bruker vektsfaktoren for å skalere timesverdiene
    FO = (gc.FO_gc0 / gc.FO_gc1) ** el
    EL = (gc.EL_gc0 / gc.EL_gc1) ** el
    

    ElValues = namedtuple("ElValues", [
        "FO",  
        "EL"
    ])

    return ElValues(FO, EL)