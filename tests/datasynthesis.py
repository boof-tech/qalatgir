import datetime as dt
from typing import Union

import numpy as np
import pandas as pd


def seconds(delta: dt.timedelta):
    return 24 * 60 * 60 * delta.days + delta.seconds


def unit_function_pattern(step: Union[int, dt.timedelta], days=31) -> pd.DataFrame:
    """Creates one month of data with unit function pattern, like: ____----___"""

    step = dt.timedelta(minutes=step) if type(step) == int else step
    times = pd.date_range(dt.date(2021, 1, 1), dt.date(2021, 1, 1) + dt.timedelta(days=days), freq=step)

    data_point_in_day = seconds(dt.timedelta(days=1)) // seconds(step)
    usage_start = seconds(dt.timedelta(hours=12)) // seconds(step)
    usage_end = seconds(dt.timedelta(hours=20)) // seconds(step)

    values = np.ones(shape=len(times))
    for d in range((times[-1] - times[0]).days):
        offset = d * data_point_in_day
        values[offset:offset + data_point_in_day] = 4000 + np.random.rand() * 100
        values[offset + usage_start:offset + usage_end] = 9000 + np.random.rand() * 500
    df = pd.DataFrame({'time': times, 'value': values})
    return df
