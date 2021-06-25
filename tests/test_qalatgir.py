import datetime as dt

import numpy as np
import pandas as pd

from qalatgir import fill_missing, numba_qalatgir
from datasynthesis import unit_function_pattern


data = [
    {
        'time': dt.datetime(2021, 1, 1),
        'value': 1.0
    },
    {
        'time': dt.datetime(2021, 1, 1, 0, 10),
        'value': 2.0
    },
    {
        'time': dt.datetime(2021, 1, 1, 0, 15),
        'value': 1.0
    }
]


def mae(ar1, ar2):
    return np.mean(np.abs(ar1-ar2))


def test_one_missing_value_should_replace_with_average():
    corrected_data = fill_missing(data[:2], step=5)
    missed = {
        'time': dt.datetime(2021, 1, 1, 0, 5),
        'value': 1.5
    }
    data.append(missed)
    assert np.all(corrected_data == pd.DataFrame(data[:2] + [missed]).set_index('time').sort_index())


def test_more_than_an_hour_missing_should_replace_with_other_days_average():
    original_data = unit_function_pattern(dt.timedelta(minutes=5))
    missed_period = slice(11 * 12, 13 * 12)
    deleted = original_data.iloc[missed_period]['value'].copy()
    original_data.loc[missed_period, 'value'] = np.nan
    corrected_data = fill_missing(original_data, 5)

    assert not any(corrected_data['value'].isna())

    recovered = corrected_data.iloc[missed_period]['value'].copy()
    assert mae(deleted.to_numpy(), recovered.to_numpy()) < 100


def test_lots_of_missing_works_in_different_days():
    original_data = unit_function_pattern(dt.timedelta(minutes=15))
    missed_period = slice(20 * 4, 27 * 4)
    deleted = original_data.iloc[missed_period]['value'].copy()
    original_data.loc[missed_period, 'value'] = np.nan
    corrected_data = fill_missing(original_data, 15)

    assert not any(corrected_data['value'].isna())

    recovered = corrected_data.iloc[missed_period]['value'].copy()
    assert mae(deleted.to_numpy(), recovered.to_numpy()) < 100


# def test_lots_of_missing_works_in_different_days_numba():
#     original_data = unit_function_pattern(dt.timedelta(minutes=5))
#     missed_period = slice(11 * 12, 13 * 12)
#     deleted = original_data.iloc[missed_period]['value'].copy()
#     original_data.loc[missed_period, 'value'] = np.nan
#     corrected_data = numba_qalatgir.numba_fill_missing(original_data, 5)
#
#     assert not any(corrected_data['value'].isna())
#
#     recovered = corrected_data.iloc[missed_period]['value'].copy()
#     assert mae(deleted.to_numpy(), recovered.to_numpy()) < 100
