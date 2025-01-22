
from collections import namedtuple
from functions.calculation_algorithms.benefit_calculation import net_benefit
from functions.data_preprocessing.discounting.get_discounting_timeseries import discounting_timeseries


def discounted_net_benefit(project):

    discounting_df = discounting_timeseries(project)
    benefit = net_benefit(project)

    # Legger sammen konsumentoverskuddet
    electric = benefit.electric.multiply(discounting_df.iloc[:, 0], axis=0)
    fossil = benefit.fossil.multiply(discounting_df.iloc[:, 0], axis=0)
    passenger = benefit.passenger.multiply(discounting_df.iloc[:, 0], axis=0)

    # Trafikantoverskuddet
    total = benefit.total.multiply(discounting_df.iloc[:, 0], axis=0)

    
    values = namedtuple("ElValues", [
            "electric",  
            "fossil", 
            "passenger",
            "total"
        ])

    return values(electric, fossil, passenger, total)