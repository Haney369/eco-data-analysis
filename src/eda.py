
"""
Exploratory Data Analysis and visualizations.
Saves plots to out_dir.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from src.utils import savefig_obj

def run_eda(df, out_dir):
    # 1) time series overview
    fig, axes = plt.subplots(len(df.columns), 1, figsize=(12, 3*len(df.columns)), sharex=True)
    if len(df.columns) == 1:
        axes = [axes]
    for ax, col in zip(axes, df.columns):
        df[col].plot(ax=ax, title=col)
        ax.set_ylabel(col)
    plt.tight_layout()
    savefig_obj(fig, out_dir, "time_series_overview.png")

    # 2) correlation heatmap
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Correlation matrix")
    savefig_obj(fig, out_dir, "correlation_matrix.png")

    # 3) seasonal decomposition for each series
    for col in df.columns:
        try:
            comp = seasonal_decompose(df[col].dropna(), period=12, model='additive', extrapolate_trend='freq')
            fig = comp.plot()
            fig.set_size_inches(10,8)
            savefig_obj(fig, out_dir, f"decompose_{col}.png")
        except Exception as e:
            print("Decompose failed for", col, e)
