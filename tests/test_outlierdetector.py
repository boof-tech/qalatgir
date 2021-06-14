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
