

from collections import namedtuple
from functions.calculation_algorithms.elasticity_factors_timeseries import elasticity_factors_timeseries
from functions.data_preprocessing.traffic_numbers.gen_car_fleet_timeseries import vehicle_group_timeseries
from functions.data_preprocessing.traffic_numbers.gen_passenger_timeseries import passenger_timeseries


def year_aggregated_passengers(project):

    passengers = passenger_timeseries(project)

    CP_t_EL_rtm_a0 = passengers.EL_a0 * 365
    CP_t_FO_rtm_a0 = passengers.FO_a0 * 365
    CP_t_EL_rtm_a1 = passengers.EL_a1 * 365
    CP_t_FO_rtm_a1 = passengers.FO_a1 * 365

    # Create a named tuple for the return
    AADTDataFrames = namedtuple('PassengerDataFrames', ['EL_a0','EL_a1', 'FO_a0','FO_a1'])
    
    return AADTDataFrames(CP_t_EL_rtm_a0, CP_t_EL_rtm_a1, CP_t_FO_rtm_a0, CP_t_FO_rtm_a1)