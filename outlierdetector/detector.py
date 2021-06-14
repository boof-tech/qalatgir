import math

import numpy as np
import pandas as pd


def detect(df: pd.DataFrame, max_value=8_000_000, max_spike=35_000) -> pd.DataFrame:
    """Adds outlier column to the `df` which is a boolean series indicating `df["value"]` is an outlier.
    This function is inplace!"""
    df['outlier'] = False
    for i in range(len(df)):
        value = df.loc[i, 'value']
        if np.isnan(value) or not math.isfinite(value) or value > max_value:
            df.loc[i, 'outlier'] = True
    for i in range(1, len(df) - 1):
        value = df.loc[i, 'value']
        if abs((df.loc[i-1, 'value'] + df.loc[i+1, 'value']) / 2 - value) > max_spike:
            df.loc[i, 'outlier'] = True
    return df
