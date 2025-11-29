
"""
Simple heuristics to flag temporary hype vs structural trends.
Uses persistence (autocorrelation), rolling volatility, and SNR.
"""
import numpy as np
from src.utils import rolling_snr

def hype_vs_structural(series, window=6):
    s = series.dropna()
    if len(s) < window + 2:
        return None
    # persistence: lag-1 autocorr
    persistence = s.autocorr(lag=1)
    # short-term volatility
    recent_vol = s.diff().rolling(window).std().iloc[-1]
    # signal-to-noise
    snr = rolling_snr(s, window=window)
    # combine: give persistence positive weight, vol negative
    # normalize roughly (-1..1)
    p = 0 if np.isnan(persistence) else np.tanh(persistence)
    v = 0 if np.isnan(recent_vol) else np.tanh(1/(1+recent_vol))
    s_score = 0.5 * p + 0.3 * v + 0.2 * np.tanh(snr if snr is not None else 0)
    return float(s_score)

def evaluate_signals(df):
    flags = {}
    for col in df.columns:
        try:
            score = hype_vs_structural(df[col])
            label = "structural" if score is not None and score > 0.2 else "temporary/hype"
            flags[col] = {"score": score, "label": label}
        except Exception as e:
            flags[col] = {"score": None, "label": "unknown", "error": str(e)}
    return flags
