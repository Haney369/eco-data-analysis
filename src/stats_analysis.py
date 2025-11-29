
"""
Statistical analysis: stationarity tests (ADF), Granger causality, pairwise stats.
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller, grangercausalitytests

def run_adf(series):
    s = series.dropna()
    if len(s) < 10:
        return {"adf_stat": None, "pvalue": None}
    res = adfuller(s, autolag='AIC')
    return {"adf_stat": res[0], "pvalue": res[1]}

def run_granger(df, maxlag=4):
    results = {}
    cols = df.columns
    for y in cols:
        for x in cols:
            if x == y:
                continue
            try:
                test = grangercausalitytests(df[[y, x]].dropna(), maxlag=maxlag, verbose=False)
                pvals = [test[l+1][0]['ssr_chi2test'][1] for l in range(maxlag)]
                results[(x, y)] = min(pvals)
            except Exception:
                results[(x, y)] = None
    return results

def run_stats(df, out_dir=None):
    # ADF per series
    adf_res = {col: run_adf(df[col]) for col in df.columns}
    # Correlation matrix
    corr = df.corr()
    # Granger causality (brief)
    try:
        granger = run_granger(df.dropna(), maxlag=4)
    except Exception as e:
        granger = {}
        print("Granger causality failed:", e)
    # Save short summaries
    if out_dir:
        with open(f"{out_dir}/adf_summary.txt", "w") as f:
            for k, v in adf_res.items():
                f.write(f"{k}: adf_stat={v['adf_stat']}, p={v['pvalue']}\n")
        with open(f"{out_dir}/granger_summary.txt", "w") as f:
            for (x,y), p in granger.items():
                f.write(f"{x} -> {y}: p={p}\n")
    return {"adf": adf_res, "corr": corr, "granger": granger}
