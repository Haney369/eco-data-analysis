
"""
Cleaning, resampling, merging, handling missing values.
"""
import pandas as pd
import numpy as np
from src.utils import ensure_index_datetime
from config import FREQ

def prepare_dataset(df_raw, start=None, end=None):
    df = df_raw.copy()
    df = ensure_index_datetime(df)
    # Restrict timeframe
    if start:
        df = df[df.index >= pd.to_datetime(start)]
    if end:
        df = df[df.index <= pd.to_datetime(end)]
    # Resample to monthly (or FREQ)
    df = df.resample(FREQ).mean()
    # Forward fill then backward fill for small gaps
    df = df.ffill().bfill()
    # Drop columns with too many NaNs
    threshold = int(len(df) * 0.5)
    df = df.dropna(axis=1, thresh=threshold)
    # Standardize column names
    df.columns = [c.strip() for c in df.columns]
    return df
