# src/reporting.py
"""
Generate markdown report with automatic formal macroeconomic narrative.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import json

def generate_macro_narrative(df, stats_res, model_res, cognitive_flags):
    """
    Creates a formal, professional macroeconomic commentary.
    """

    corr = stats_res.get("corr")
    sarima = model_res.get("sarima", {})
    ml = model_res.get("ml", {})

    # ---------------------------
    # 1. Identify key positive & negative correlations
    # ---------------------------
    corr_un = corr.unstack()
    corr_un = corr_un.dropna()
    corr_un = corr_un[corr_un.index.get_level_values(0) != corr_un.index.get_level_values(1)]
    corr_sorted = corr_un.sort_values(ascending=False)

    top_pos = corr_sorted.head(3)
    top_neg = corr_sorted.tail(3)

    # ---------------------------
    # 2. Identify strongest SARIMA trends
    # ---------------------------
    trend_lines = []
    for ind, res in sarima.items():
        fc = res["forecast"]
        if fc is not None and len(fc) > 1:
            direction = "rising" if fc.iloc[-1] > df[ind].iloc[-1] else "declining"
            trend_lines.append(f"{ind} appears {direction} over the forecast horizon.")
    
    # ---------------------------
    # 3. Identify structural vs hype indicators
    # ---------------------------
    structural = [k for k,v in cognitive_flags.items() if v.get("label")=="structural"]
    hype = [k for k,v in cognitive_flags.items() if v.get("label")=="temporary/hype"]

    # ---------------------------
    # Build narrative text
    # ---------------------------
    narrative = []

    narrative.append("## Executive Macroeconomic Narrative\n")
    narrative.append(
        "The following analysis provides an integrated assessment of macroeconomic conditions and "
        "their interaction with financial markets over the specified period. "
        "The insights are derived from historical data trends, correlation structures, statistical testing, "
        "and forward-looking forecasts."
    )

    # Correlation insights
    narrative.append("\n### Key Market–Macro Relationships\n")
    narrative.append(
        "The correlation analysis highlights the strongest statistical relationships between macroeconomic proxies "
        "and major equity indices."
    )
    narrative.append("\n**Most positively correlated pairs:**")
    for (a,b),v in top_pos.items():
        narrative.append(f"- {a} and {b}: correlation {v:.2f}")

    narrative.append("\n**Most negatively correlated pairs:**")
    for (a,b),v in top_neg.items():
        narrative.append(f"- {a} and {b}: correlation {v:.2f}")

    # SARIMA trend summary
    narrative.append("\n### Forecasted Macro Trends\n")
    if trend_lines:
        for t in trend_lines:
            narrative.append(f"- {t}")
    else:
        narrative.append("- No significant trend shifts detected in the forecasting window.")

    # Structural vs hype
    narrative.append("\n### Structural vs Short-Term Signals\n")
    narrative.append(
        "Indicators classified as *structural* exhibit persistent, fundamental-driven movement, "
        "while *temporary* signals reflect short-term fluctuations or market noise."
    )

    narrative.append("\n**Structural indicators:**")
    if structural:
        for s in structural:
            narrative.append(f"- {s}")
    else:
        narrative.append("- None identified as structurally dominant.")

    narrative.append("\n**Short-term or volatile indicators:**")
    if hype:
        for h in hype:
            narrative.append(f"- {h}")
    else:
        narrative.append("- No indicators flagged as short-term or noise dominated.")

    narrative.append("\n---\n")
    return "\n".join(narrative)


def generate_report(df, stats_res, model_res, cognitive_flags, out_dir="outputs/report"):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    md = []
    md.append("# Macroeconomic Analysis Report\n")
    md.append(f"**Time range:** {df.index.min().date()} to {df.index.max().date()}\n")
    md.append("**Indicators analyzed:** " + ", ".join(df.columns) + "\n")
    md.append("\n---\n")

    # Add formal macro narrative
    md.append(generate_macro_narrative(df, stats_res, model_res, cognitive_flags))

    # Technical sections
    md.append("\n## Technical Summary\n")

    # ADF
    md.append("\n### Stationarity Tests (ADF)\n")
    for k,v in stats_res.get("adf", {}).items():
        md.append(f"- {k}: ADF={v.get('adf_stat')}, p={v.get('pvalue')}")

    # Correlations
    md.append("\n### Correlation Matrix\n(See correlation plot in output folder.)\n")

    # SARIMA summary
    md.append("\n### SARIMA Forecast Diagnostics\n")
    for k, v in model_res.get("sarima", {}).items():
        if v.get("fit") is not None:
            md.append(f"- {k}: AIC={v['fit'].aic:.2f}")

    # ML
    md.append("\n### Machine Learning Baseline\n")
    for k,v in model_res.get("ml", {}).items():
        md.append(f"- {k}: MSE={v.get('mse'):.4f}")

    # Cognitive flags
    md.append("\n### Structural vs Temporary Indicator Classification\n")
    for k,v in cognitive_flags.items():
        md.append(f"- {k}: {v.get('label')} (score {v.get('score')})")

    # Write markdown + JSON
    md_path = out_dir / "report_summary.md"
    md_path.write_text("\n".join(md))

    (out_dir / "analysis_summary.json").write_text(
        json.dumps({
            "adf": stats_res.get("adf"),
            "cognitive": cognitive_flags
        }, default=str, indent=2)
    )

    print("Report written to:", md_path)
    return md_path
