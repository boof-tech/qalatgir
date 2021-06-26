import datetime as dt

import numpy as np

from qalatgir import fill_missing
from tests.datasynthesis import unit_function_pattern


def setup():
    original_data = unit_function_pattern(dt.timedelta(minutes=5), days=365).iloc[15:].reset_index(drop=True)
    missed_period = slice((10 + np.random.randint(30)) * 12, (48 + np.random.randint(30)) * 12)
    original_data.loc[missed_period, 'value'] = np.nan
    return (original_data, 5), {}


def test_pure_python(benchmark):
    benchmark.pedantic(fill_missing, setup=setup, rounds=300)
