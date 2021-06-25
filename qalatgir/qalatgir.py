import math
import datetime as dt

import numpy as np
import pandas as pd


def get_consecutive_missing(values):
    start = 0
    null_found = False
    misses = []
    for i, v in enumerate(values):
        if invalid_value(v) and not null_found:
            null_found = True
            start = i
        elif invalid_value(v):
            continue
        elif null_found:
            misses.append((start, i))
            null_found = False

    return misses


def invalid_value(v):
    return np.isnan(v) or not math.isfinite(v)


def neighbors_interpolate(data, miss_start, miss_end):

    miss_count = miss_end - miss_start
    start_value = data.iloc[miss_start - 1]['value']
    end_value = data.iloc[miss_end]['value']
    change = (end_value - start_value) / (miss_count + 1)

    for j, i in enumerate(range(miss_start, miss_end)):
        data.iloc[i] = (j + 1) * change + data.iloc[miss_start - 1]


def daily_average(data):
    return data.groupby([data.index.hour, data.index.minute]).mean()


def daily_average_interpolate(data, miss_start, miss_end):
    daily_vag = daily_average(data)
    for i in range(miss_start, miss_end):
        missed_time = data.index[i]
        data.loc[missed_time] = daily_vag.loc[missed_time.hour, missed_time.minute]

    return data


def interpolate_missing(data, step, misses):
    for miss_start, miss_end in misses:
        miss_count = miss_end - miss_start
        if miss_count < 2 or step*miss_count <= dt.timedelta(hours=1):
            neighbors_interpolate(data, miss_start, miss_end)
        else:
            daily_average_interpolate(data, miss_start, miss_end)


def add_slots_for_missing(data, step):
    data = pd.DataFrame(data)
    start = data.iloc[0]['time']
    end = data.iloc[-1]['time']
    data.set_index(['time'], inplace=True)
    times = pd.date_range(start, end, freq=step)
    return data.reindex(times)


def fill_missing(data, step):
    step = dt.timedelta(minutes=step) if type(step) == int else step
    if not len(data):
        return data
    data = add_slots_for_missing(data, step)
    misses = get_consecutive_missing(data['value'])
    interpolate_missing(data, step, misses)
    return data
