from collections import namedtuple
import pandas as pd

from functions.calculation_algorithms.generalized_cost_timeseries import generalized_cost_timeseries
from functions.data_preprocessing.traffic_numbers.year_aggregated_passengers import year_aggregated_passengers
from functions.data_preprocessing.traffic_numbers.year_aggregated_traffic import year_aggregated_traffic

def net_benefit(project):
    """
    Pris (Y-akse)
    
    |\
    | \   (Etterspørselskurven)
    |  \
    |   \
    |____\    Kvantum (X-akse)

    Når kostnaden reduseres for brukerene av den nye veien øker konsumentoverskuddet. 
    Som følge av den reduserte kostnaden vil også flere biler (kvantum øker) velge å benytte seg av veien,
    iform av: flere handleturer, flere besøk til familie og venner, overføring fra andre veier osv.

    Derfor regner vi ut rektangelet (eksisterende agenters nytteendring)
    og trekanten (tilkommende agenters nytte)

    """
    
    vehicles_YDT = year_aggregated_traffic(project)
    passengers_YDT = year_aggregated_passengers(project)
    costs = generalized_cost_timeseries(project)

    # areal av trekant = 0.5 * (K0 - K1) * (Q1 - Q0)
    # Trekantberegning (Tilkommende trafikanters konsumentoverskudd)
    triangle_EL = 0.5 * (costs.EL_gc0 - costs.EL_gc1) * (vehicles_YDT.electric_a1 - vehicles_YDT.electric_a0)
    triangle_FO = 0.5 * (costs.FO_gc0 - costs.FO_gc1) * (vehicles_YDT.fossil_a1 - vehicles_YDT.fossil_a0)
    triangle_passenger_FO = 0.5 * (costs.passenger_c0 - costs.passenger_c1) * (passengers_YDT.FO_a1 - passengers_YDT.FO_a0)
    triangle_passenger_EL = 0.5 * (costs.passenger_c0 - costs.passenger_c1) * (passengers_YDT.EL_a1 - passengers_YDT.EL_a0)

    # areal av rektangel = (K0 - K1) * Q0
    # Rektangelberegning (Nytteendring i konsumentoverskuddet til eksisterende trafiaknter)
    rectangle_EL = (costs.EL_gc0 - costs.EL_gc1) * (vehicles_YDT.electric_a0)
    rectangle_FO = (costs.FO_gc0 - costs.FO_gc1) * (vehicles_YDT.fossil_a0)
    rectangle_passenger_FO = (costs.passenger_c0 - costs.passenger_c1) * (passengers_YDT.FO_a0)
    rectangle_passenger_EL = (costs.passenger_c0 - costs.passenger_c1) * (passengers_YDT.EL_a0)
    
    # Legger sammen konsumentoverskuddet
    electric = triangle_EL + rectangle_EL
    fossil = triangle_FO + rectangle_FO
    passenger = triangle_passenger_FO + triangle_passenger_EL + rectangle_passenger_FO + rectangle_passenger_EL

    # Trafikantoverskuddet
    total = electric + fossil + passenger

    
    values = namedtuple("ElValues", [
            "electric",  
            "fossil", 
            "passenger",
            "total"
        ])

    return values(electric, fossil, passenger, total)