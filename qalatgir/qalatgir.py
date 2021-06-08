import datetime as dt

import numpy as np
import pandas as pd


def missed(data, time):
    for d in data:
        if d['time'] == time:
            return False
    return True


def add_slots_for_missing(data, step):
    data = pd.DataFrame(data)
    start = data.iloc[0]['time']
    end = data.iloc[-1]['time']
    data.set_index(['time'], inplace=True)
    times = pd.date_range(start, end, freq=f'{step * 60}s')
    return data.reindex(times)


def fill_missing(data, step):
    if not len(data):
        return data
    data = add_slots_for_missing(data, step)

    return data
