import datetime as dt

import numpy as np

from qalatgir import fill_missing
from tests.datasynthesis import unit_function_pattern


def get_data():
    original_data = unit_function_pattern(dt.timedelta(minutes=5), days=365).iloc[15:].reset_index(drop=True)
    for i in np.random.randint(0, 300, 50):
        missed_period = slice(i * 24 * 12 + (10 + np.random.randint(30)) * 12,
                              i * 24 * 12 + (48 + np.random.randint(30)) * 12)
        original_data.loc[missed_period, 'value'] = np.nan
    return original_data


def setup_cython():
    return (get_data(), 5, 'cython'), {}


def setup_numba():
    return (get_data(), 5, 'numba'), {}


def setup_rust():
    return (get_data(), 5, 'rust'), {}


def test_benchmark_on_numba(benchmark):
    benchmark.pedantic(fill_missing, setup=setup_numba, rounds=30)


def test_benchmark_on_rust(benchmark):
    benchmark.pedantic(fill_missing, setup=setup_cython, rounds=30)


def test_benchmark_on_cython(benchmark):
    benchmark.pedantic(fill_missing, setup=setup_rust, rounds=30)
