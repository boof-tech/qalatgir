import math
import datetime as dt

import numpy as np
import pandas as pd
import numba


@numba.jit(cache=True, nopython=True)
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


@numba.jit(cache=True, nopython=True)
def invalid_value(v):
    return np.isnan(v) or not math.isfinite(v)


def data_point_per_hour(step):
    if isinstance(step, int):
        return 60 // step
    else:
        return 3600 // step.seconds


def minutes_data_count(minutes, step):
    if isinstance(step, int):
        return minutes // step
    else:
        return minutes * 60 // step.seconds


def neighbors_interpolate(data, miss_start, miss_end):
    miss_count = miss_end - miss_start
    start_value = data.iloc[miss_start - 1]['value']
    end_value = data.iloc[miss_end]['value']
    change = (end_value - start_value) / (miss_count + 1)

    for j, i in enumerate(range(miss_start, miss_end)):
        data.iloc[i] = (j + 1) * change + data.iloc[miss_start - 1]


def seconds(delta):
    return delta.days * 24 * 3600 + delta.seconds


def daily_average(arr, step_seconds, days, start_hour, start_minute):
    points_per_day = (24 * 3600) // step_seconds
    data_place = np.empty(points_per_day * (days + 2))
    data_place.fill(np.nan)
    offset = (start_hour * 3600) // step_seconds + (start_minute * 60) // step_seconds
    data_place[offset:offset + len(arr)] = arr
    data_stride = data_place.strides
    daily_table = np.lib.stride_tricks.as_strided(data_place,
                                                  shape=(days + 1, points_per_day),
                                                  strides=(data_stride[0] * points_per_day, data_stride[0]))
    return np.nanmean(daily_table, axis=0)


def daily_average_interpolate(arr, daily_vag, miss_start, miss_end, step, step_seconds, start_hour, start_minute):
    offset = (start_hour * 3600) // step_seconds + (start_minute * 60) // step_seconds
    data_point_per_day = ((24 * 3600) // step.seconds)
    days = len(arr) // data_point_per_day + 1
    repeated_daily = np.tile(daily_vag, days)
    arr[miss_start:miss_end] = repeated_daily[offset + miss_start:offset + miss_end]
    return arr


def interpolate_missing(data, step, misses):
    for miss_start, miss_end in misses:
        miss_count = miss_end - miss_start
        if miss_count < 2 or step * miss_count <= dt.timedelta(hours=1):
            neighbors_interpolate(data, miss_start, miss_end)
        else:
            daily_avg = daily_average(data['value'].to_numpy(),
                                      step_seconds=step.seconds, days=(data.index[-1] - data.index[0]).days,
                                      start_hour=data.index[0].hour, start_minute=data.index[0].minute)

            data['value'] = daily_average_interpolate(data['value'].to_numpy(),
                                                      daily_avg, miss_start, miss_end, step, step_seconds=step.seconds,
                                                      start_hour=data.index[0].hour, start_minute=data.index[0].minute)


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
    misses = get_consecutive_missing(data['value'].to_numpy())
    interpolate_missing(data, step, misses)
    return data
