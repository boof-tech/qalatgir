import math

import numpy as np


def detect(df):
    df['outlier'] = False
    for i in range(len(df)):
        value = df.loc[i, 'value']
        if np.isnan(value) or not math.isfinite(value):
            df.loc[i, 'outlier'] = True
    return df
