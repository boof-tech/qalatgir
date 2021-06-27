import cProfile
import datetime as dt

import numpy as np

from tests.datasynthesis import unit_function_pattern
from qalatgir import fill_missing


original_data = unit_function_pattern(dt.timedelta(minutes=5))
missed_period = slice(11 * 12, 13 * 12)
deleted = original_data.iloc[missed_period]['value'].copy()
original_data.loc[missed_period, 'value'] = np.nan
fill_missing(original_data, 5)

original_data = unit_function_pattern(dt.timedelta(minutes=5))
missed_period = slice(11 * 12, 13 * 12)
deleted = original_data.iloc[missed_period]['value'].copy()
original_data.loc[missed_period, 'value'] = np.nan
print(cProfile.run('fill_missing(original_data, 5)', sort='cumtime'))
