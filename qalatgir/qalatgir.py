import math

import numpy as np
import pandas as pd


def get_consecutive_missing(values):
    start = 0
    null_found = False
    misses = []
    for i, v in enumerate(values):
        if np.isnan(v) or not math.isfinite(v):
            null_found = True
            start = i
        elif null_found:
            misses.append((start, i))
            null_found = False

    return misses


def average_interpolate(data, miss):

    miss_count = miss[1] - miss[0]
    start_value = data.iloc[miss[0] - 1]['value']
    end_value = data.iloc[miss[1]]['value']
    change = (end_value - start_value) / (miss_count + 1)

    for j, i in enumerate(range(*miss)):
        data.iloc[i] = (j + 1) * change + data.iloc[miss[0] - 1]


def interpolate_missing(data, step, misses):
    for miss in misses:
        miss_count = miss[1] - miss[0]
        if miss_count < 2 or (miss_count < 4 and step < 60):
            average_interpolate(data, miss)


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
    misses = get_consecutive_missing(data['value'])
    interpolate_missing(data, step, misses)
    return data
