

from collections import namedtuple
from functions.calculation_algorithms.elasticity_factors_timeseries import elasticity_factors_timeseries
from functions.data_preprocessing.traffic_numbers.gen_car_fleet_timeseries import vehicle_group_timeseries


def year_aggregated_traffic(project):

    vehicles = vehicle_group_timeseries(project)

    traffic_FO_a0 = vehicles.fossil_a0 * 365
    traffic_EL_a0 = vehicles.electric_a0 * 365
    fossil_df = vehicles.fossil_a1 * 365
    electric_df = vehicles.electric_a1 * 365
    total_df_a0 = vehicles.all_a0 * 365
    total_df_a1 = vehicles.all_a1 * 365

    # Create a named tuple for the return
    AADTDataFrames = namedtuple('AADTDataFrames', ['fossil_a0', 'electric_a0', 'fossil_a1', 'electric_a1', 'all_a0', 'all_a1'])
    
    return AADTDataFrames(fossil_a0=traffic_FO_a0, electric_a0=traffic_EL_a0, fossil_a1=fossil_df, electric_a1=electric_df, all_a0=total_df_a0, all_a1=total_df_a1)