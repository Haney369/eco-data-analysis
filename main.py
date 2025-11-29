# main.py
"""
Orchestrator for macro_analysis pipeline.
Runs: data collection -> prep -> eda -> stats -> modeling -> cognitive -> reporting
"""
import os
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

from config import RAW_DIR, OUTPUT_DIR, PLOTS_DIR, REPORT_DIR, TIMEFRAME_START, TIMEFRAME_END, FORECAST_PERIODS

# Local imports
from src.data_collection import collect_all_indicators
from src.data_prep import prepare_dataset
from src.eda import run_eda
from src.stats_analysis import run_stats
from src.modeling import run_modeling_pipeline
from src.cognitive_model import evaluate_signals
from src.reporting import generate_report

def ensure_outputs():
    for p in (OUTPUT_DIR, PLOTS_DIR, REPORT_DIR):
        Path(p).mkdir(parents=True, exist_ok=True)

def main():
    ensure_outputs()
    print("1) Collecting data...")
    raw = collect_all_indicators(RAW_DIR)
    print("Data collected. Columns:", raw.columns.tolist())

    print("2) Preparing dataset...")
    df = prepare_dataset(raw, start=TIMEFRAME_START, end=TIMEFRAME_END)
    print("Prepared dataset shape:", df.shape)

    print("3) Running EDA & visuals...")
    run_eda(df, out_dir=PLOTS_DIR)

    print("4) Running statistical analysis...")
    stats_res = run_stats(df, out_dir=OUTPUT_DIR)

    print("5) Modeling & forecasting...")
    model_res = run_modeling_pipeline(df, forecast_periods=FORECAST_PERIODS, out_dir=OUTPUT_DIR)

    print("6) Cognitive heuristics (hype vs structural)...")
    cognitive_flags = evaluate_signals(df)

    print("7) Generating report...")
    generate_report(df, stats_res, model_res, cognitive_flags, out_dir=REPORT_DIR)

    print("All done. Check outputs/ for visuals and report.")

if __name__ == "__main__":
    main()
