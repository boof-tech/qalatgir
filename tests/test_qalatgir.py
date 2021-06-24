import datetime as dt

import numpy as np
import pandas as pd

from qalatgir import fill_missing


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


def test_one_missing_value_should_replace_with_average():
    corrected_data = fill_missing(data[:2], step=5)
    missed = {
        'time': dt.datetime(2021, 1, 1, 0, 5),
        'value': 1.5
    }
    data.append(missed)
    assert np.all(corrected_data == pd.DataFrame(data[:2] + [missed]).set_index('time').sort_index())
