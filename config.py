# config.py
"""
Configuration for Eco Data Analysis – Macroeconomic trends via Yahoo Finance.
This version uses only Yahoo Finance tickers as proxies for macro indicators,
no API keys or CSVs required.
"""

from pathlib import Path

# -------------------------
# PATHS
# -------------------------
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = BASE_DIR / "outputs"
PLOTS_DIR = OUTPUT_DIR / "plots"
REPORT_DIR = OUTPUT_DIR / "report"

# Create folders if missing
for p in [DATA_DIR, RAW_DIR, PROCESSED_DIR, OUTPUT_DIR, PLOTS_DIR, REPORT_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# -------------------------
# PROJECT SCOPE
# -------------------------
GEO_SCOPE = "US"
TIMEFRAME_START = "2013-01-01"
TIMEFRAME_END   = "2024-12-31"
FREQ = "M"
FORECAST_PERIODS = 12  # forecast next 12 months

# -------------------------
# INDICATORS — MACRO + MARKET (Yahoo)
# -------------------------
# This selection blends macroeconomic variables with market indices.
# All are available via Yahoo Finance. No API key needed.

INDICATORS = [
    # Market indices
    {"name": "SP500",       "type": "yahoo", "ticker": "^GSPC"},
    {"name": "NASDAQ100",   "type": "yahoo", "ticker": "^NDX"},
    {"name": "DOWJONES",    "type": "yahoo", "ticker": "^DJI"},

    # Macroeconomic proxies
    {"name": "INFLATION_TIP", "type": "yahoo", "ticker": "TIP"},         # inflation-protected bonds
    {"name": "USD_INDEX",     "type": "yahoo", "ticker": "DX-Y.NYB"},    # dollar strength
    {"name": "10YR_YIELD",    "type": "yahoo", "ticker": "^TNX"},        # 10-year Treasury yield
    {"name": "VIX",           "type": "yahoo", "ticker": "^VIX"},        # volatility index
    {"name": "CRUDE_OIL",     "type": "yahoo", "ticker": "CL=F"},        # crude oil futures
    {"name": "GOLD",          "type": "yahoo", "ticker": "GC=F"}         # gold futures
]

# -------------------------
# MODEL CONFIG
# -------------------------
SARIMA_DEFAULTS = {
    "order": (1, 1, 1),
    "seasonal_order": (1, 1, 1, 12),
    "enforce_stationarity": False
}

LAGS = 6
ML_MODEL = "rf"  # "rf" or "lr"

# Not used (no FRED)
FRED_API_ENVVAR = "FRED_API_KEY"
