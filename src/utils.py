# src/utils.py
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def savefig_obj(fig, out_dir, name):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / name
    fig.savefig(path, bbox_inches='tight', dpi=150)
    plt.close(fig)
    print("Saved:", path)
    return path

def ensure_index_datetime(df):
    df = df.copy()
    if not isinstance(df.index, pd.DatetimeIndex):
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.set_index('Date')
        else:
            raise ValueError("DataFrame must have a DatetimeIndex or a 'Date' column")
    return df

def rolling_snr(series, window=6):
    # signal-to-noise ratio: mean change magnitude / std of changes
    diffs = series.diff().dropna()
    if len(diffs) < 2:
        return np.nan
    sig = np.abs(diffs.rolling(window).mean()).iloc[-1]
    noise = diffs.rolling(window).std().iloc[-1]
    return float(sig / (noise + 1e-9))
