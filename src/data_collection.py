
"""
Data collectors: Yahoo, FRED, CSV local.
Returns a wide DataFrame with Date index and columns per indicator name.
"""
import os
from pathlib import Path
import pandas as pd
import yfinance as yf
import numpy as np
from dotenv import load_dotenv
from config import INDICATORS, TIMEFRAME_START, TIMEFRAME_END, FRED_API_ENVVAR
from fredapi import Fred

load_dotenv()

def fetch_yahoo(ticker, start, end):
    """
    Fetch monthly time-series data from Yahoo Finance.
    Handles MultiIndex columns and missing 'Adj Close'.
    """
    df = yf.download(ticker, start=start, end=end, progress=False)

    if df is None or df.empty:
        print(f"[Yahoo] No data returned for {ticker}. Skipping.")
        return None

    # Handle multi-index columns (some tickers like DX-Y.NYB, ^TNX, CL=F)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    # Choose the best available column for pricing/value
    price_col = None
    for candidate in ["Adj Close", "Close", "Value"]:
        if candidate in df.columns:
            price_col = candidate
            break

    if not price_col:
        print(f"[Yahoo] No valid price column found for {ticker}. Columns: {df.columns.tolist()}")
        return None

    # Clean and resample to monthly frequency
    df = df[[price_col]].rename(columns={price_col: ticker})
    df.index = pd.to_datetime(df.index)
    df = df.resample("M").last()

    return df

def fetch_fred(series_id, api_key=None, start=None, end=None):
    api_key = api_key or os.getenv(FRED_API_ENVVAR)
    if not api_key:
        print(f"[FRED] No API key. Skipping {series_id}.")
        return None

    try:
        fred = Fred(api_key=api_key)
        series = fred.get_series(series_id, observation_start=start, observation_end=end)
    except Exception as e:
        print(f"[FRED] Failed for {series_id}: {e}")
        return None

    df = series.to_frame(series_id)
    df.index = pd.to_datetime(df.index)
    df = df.resample("M").last()
    return df

def load_local_csv(filename, raw_dir):
    p = Path(raw_dir) / filename
    if not p.exists():
        print("Local CSV not found:", p)
        return None

    df = pd.read_csv(p)

    # 1. If any column contains 'date' (case-insensitive)
    for c in df.columns:
        if "date" in c.lower():
            df = df.rename(columns={c: "Date"})
            break

    # 2. If no Date column but has Year & Month
    if "Date" not in df.columns:
        if {"Year", "Month"}.issubset(df.columns):
            df["Date"] = pd.to_datetime(
                df["Year"].astype(str) + "-" + df["Month"].astype(str) + "-01"
            )
        else:
            # 3. Last fallback — use index as date if numeric
            if df.index.dtype != "datetime64[ns]":
                print(f"[CSV] No Date, Year, Month columns found in {filename}. Skipping file.")
                return None

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date")

    # Find first numeric column
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        print("[CSV] No numeric columns found. Skipping.")
        return None

    col = numeric_cols[0]

    # Convert to monthly
    monthly = df[[col]].resample("M").mean().rename(columns={col: filename.replace(".csv","")})
    return monthly

def collect_all_indicators(raw_dir):
    raw_dir = Path(raw_dir)
    frames = []
    for ind in INDICATORS:
        try:
            if ind['type'] == 'yahoo':
                df = fetch_yahoo(
                    ticker=ind['ticker'],
                    start=TIMEFRAME_START,
                    end=TIMEFRAME_END
                )
                df = df.rename(columns={ind['ticker']: ind['name']})
                frames.append(df)
            elif ind['type'] == 'fred':
                try:
                    df = fetch_fred(ind['fred_id'])
                    df = df.rename(columns={ind['fred_id']: ind['name']})
                    frames.append(df)
                except Exception as e:
                    print("FRED fetch failed for", ind['fred_id'], e)
            elif ind['type'] == 'csv':
                df = load_local_csv(ind['filename'], raw_dir)
                if df is not None:
                    df = df.rename(columns={df.columns[0]: ind['name']})
                    frames.append(df)
        except Exception as e:
            print("Failed to load indicator", ind, e)

    if not frames:
        raise RuntimeError("No data collected. Provide CSVs or FRED/Yahoo access.")
    # merge
    df_all = pd.concat(frames, axis=1)
    return df_all
