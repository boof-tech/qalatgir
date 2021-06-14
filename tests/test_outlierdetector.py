import datetime as dt
import math

import pandas as pd
import numpy as np

from outlierdetector import detect

data = [
    {
        'time': dt.datetime(2021, 1, 1),
        'value': 1.0
    },
    {
        'time': dt.datetime(2021, 1, 1, 0, 10),
        'value': np.nan
    },
    {
        'time': dt.datetime(2021, 1, 1, 0, 15),
        'value': math.inf
    },
    {
        'time': dt.datetime(2021, 1, 1, 0, 15),
        'value': 8_000_001
    },
    {
        'time': dt.datetime(2021, 1, 1, 0, 15),
        'value': 50_001
    },
    {
        'time': dt.datetime(2021, 1, 1, 0, 15),
        'value': 2
    },
    {
        'time': dt.datetime(2021, 1, 1, 0, 15),
        'value': 40_000
    },
    {
        'time': dt.datetime(2021, 1, 1, 0, 15),
        'value': 3
    }
]

df = pd.DataFrame(data)
detect(df)


def test_outlier_detector_adds_outlier_column():
    df = pd.DataFrame(data[:1])
    assert 'outlier' in detect(df).columns


def test_nan_values_are_outlier():
    assert df.loc[1, 'outlier']
    assert not df.loc[0, 'outlier']


def test_infinite_values_are_outlier():
    assert df.loc[2, 'outlier']


def test_value_bigger_than_eight_millions_is_outlier_by_default():
    assert df.loc[3, 'outlier']


def test_maximum_for_value_can_be_set():
    detect(df, max_value=50_000)
    assert df.loc[3, 'outlier']


def test_single_spikes_with_max_diff_are_outlier():
    assert df.loc[5, 'outlier']
