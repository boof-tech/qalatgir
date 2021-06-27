import datetime as dt

import numpy as np

from qalatgir import fill_missing, get_consecutive_missing_numba
from qalatgir.cy_qalatgir.qalatgir import get_consecutive_missing as get_consecutive_missing_cython
from rust_qalatgir import get_consecutive_missing as get_consecutive_missing_rust
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


# def test_benchmark_on_numba(benchmark):
#     benchmark.pedantic(fill_missing, setup=setup_numba, rounds=30)
#
#
# def test_benchmark_on_rust(benchmark):
#     benchmark.pedantic(fill_missing, setup=setup_cython, rounds=30)
#
#
# def test_benchmark_on_cython(benchmark):
#     benchmark.pedantic(fill_missing, setup=setup_rust, rounds=30)


def setup_get_consecutive_missing_cython():
    arr = np.arange(1_000_000, dtype=float)
    arr[np.random.randint(0, 1_000_000, 10_000)] = np.nan
    return (arr, len(arr)), {}


def setup_get_consecutive_missing():
    arr = np.arange(1_000_000, dtype=float)
    arr[np.random.randint(0, 1_000_000, 10_000)] = np.nan
    return (arr, ), {}


def test_get_consecutive_missing_cython(benchmark):
    benchmark.pedantic(get_consecutive_missing_cython, setup=setup_get_consecutive_missing_cython, rounds=30)


def test_get_consecutive_missing_rust(benchmark):
    benchmark.pedantic(get_consecutive_missing_rust, setup=setup_get_consecutive_missing, rounds=30)


def test_get_consecutive_missing_numba(benchmark):
    benchmark.pedantic(get_consecutive_missing_numba, setup=setup_get_consecutive_missing, rounds=30)
