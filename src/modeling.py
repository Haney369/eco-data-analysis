
"""
Modeling: SARIMA (univariate per series), VAR (placeholder), and ML lag-based baseline (RF or LR).
Saves forecasts and some diagnostics.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from src.utils import savefig_obj
from config import SARIMA_DEFAULTS, LAGS, ML_MODEL

def sarima_fit_forecast(series, periods, order=None, seasonal_order=None, enforce_stationarity=False):
    series = series.dropna()
    if order is None:
        order = SARIMA_DEFAULTS['order']
    if seasonal_order is None:
        seasonal_order = SARIMA_DEFAULTS['seasonal_order']
    model = SARIMAX(series, order=order, seasonal_order=seasonal_order,
                    enforce_stationarity=enforce_stationarity, enforce_invertibility=False)
    fit = model.fit(disp=False)
    pred = fit.get_forecast(steps=periods)
    forecast = pred.predicted_mean
    conf = pred.conf_int()
    return fit, forecast, conf

def build_lag_features(df, lags=LAGS):
    X = pd.DataFrame(index=df.index)
    for col in df.columns:
        for lag in range(1, lags+1):
            X[f"{col}_lag_{lag}"] = df[col].shift(lag)
    return X

def ml_lag_forecast(df, target_col, periods, lags=LAGS, model_type=ML_MODEL):
    X = build_lag_features(df, lags=lags)
    y = df[[target_col]]
    data = X.join(y).dropna()
    if len(data) <= periods:
        raise RuntimeError("Not enough data for ML forecast.")
    train = data.iloc[:-periods]
    test = data.iloc[-periods:]
    X_train = train.drop(columns=[target_col])
    y_train = train[target_col]
    X_test = test.drop(columns=[target_col])
    y_test = test[target_col]
    if model_type == "rf":
        model = RandomForestRegressor(n_estimators=200, random_state=42)
    else:
        model = LinearRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    # place preds into a series with proper dates
    preds_s = pd.Series(preds, index=y_test.index, name=f"{target_col}_ml_pred")
    return model, preds_s, y_test, mse

def run_modeling_pipeline(df, forecast_periods=12, out_dir="outputs"):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    sarima_results = {}
    ml_results = {}
    for col in df.columns:
        try:
            fit, forecast, conf = sarima_fit_forecast(df[col], periods=forecast_periods)
            # make forecast index
            start = df.index[-1] + pd.offsets.MonthBegin()
            forecast.index = pd.date_range(start=start, periods=forecast_periods, freq='M')
            conf.index = forecast.index
            sarima_results[col] = {"fit": fit, "forecast": forecast, "conf": conf}
            # plot
            fig, ax = plt.subplots(figsize=(10,4))
            df[col].plot(ax=ax, label="history")
            forecast.plot(ax=ax, label="sarima_forecast")
            ax.fill_between(forecast.index, conf.iloc[:,0], conf.iloc[:,1], alpha=0.2)
            ax.set_title(f"SARIMA forecast: {col}")
            ax.legend()
            savefig_obj(fig, out_dir, f"sarima_{col}.png")
        except Exception as e:
            print("SARIMA failed:", col, e)

        # ML baseline (try)
        try:
            model, preds, y_test, mse = ml_lag_forecast(df, col, periods=min(forecast_periods, max(3, len(df)//6)))
            ml_results[col] = {"model": model, "preds": preds, "y_test": y_test, "mse": mse}
            # plot ml preds vs actual
            fig, ax = plt.subplots(figsize=(10,4))
            combined = pd.concat([y_test, preds], axis=1)
            combined.plot(ax=ax)
            ax.set_title(f"ML lag baseline: {col} (MSE={mse:.3f})")
            savefig_obj(fig, out_dir, f"ml_{col}.png")
        except Exception as e:
            print("ML baseline failed for", col, e)

    # Optionally VAR modeling could be added here
    return {"sarima": sarima_results, "ml": ml_results}
