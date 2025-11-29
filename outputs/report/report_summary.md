# Macroeconomic Analysis Report

**Time range:** 2013-01-31 to 2024-12-31

**Indicators analyzed:** SP500, NASDAQ100, DOWJONES, INFLATION_TIP, USD_INDEX, 10YR_YIELD, VIX, CRUDE_OIL, GOLD


---

## Executive Macroeconomic Narrative

The following analysis provides an integrated assessment of macroeconomic conditions and their interaction with financial markets over the specified period. The insights are derived from historical data trends, correlation structures, statistical testing, and forward-looking forecasts.

### Key Market–Macro Relationships

The correlation analysis highlights the strongest statistical relationships between macroeconomic proxies and major equity indices.

**Most positively correlated pairs:**
- SP500 and NASDAQ100: correlation 0.99
- NASDAQ100 and SP500: correlation 0.99
- DOWJONES and SP500: correlation 0.99

**Most negatively correlated pairs:**
- USD_INDEX and CRUDE_OIL: correlation -0.28
- 10YR_YIELD and VIX: correlation -0.31
- VIX and 10YR_YIELD: correlation -0.31

### Forecasted Macro Trends

- SP500 appears rising over the forecast horizon.
- NASDAQ100 appears rising over the forecast horizon.
- DOWJONES appears rising over the forecast horizon.
- INFLATION_TIP appears rising over the forecast horizon.
- USD_INDEX appears rising over the forecast horizon.
- 10YR_YIELD appears rising over the forecast horizon.
- VIX appears declining over the forecast horizon.
- CRUDE_OIL appears declining over the forecast horizon.
- GOLD appears rising over the forecast horizon.

### Structural vs Short-Term Signals

Indicators classified as *structural* exhibit persistent, fundamental-driven movement, while *temporary* signals reflect short-term fluctuations or market noise.

**Structural indicators:**
- SP500
- NASDAQ100
- DOWJONES
- INFLATION_TIP
- USD_INDEX
- 10YR_YIELD
- VIX
- CRUDE_OIL
- GOLD

**Short-term or volatile indicators:**
- No indicators flagged as short-term or noise dominated.

---


## Technical Summary


### Stationarity Tests (ADF)

- SP500: ADF=1.019510664078886, p=0.9944676020278383
- NASDAQ100: ADF=1.0585930149956804, p=0.9948472667553364
- DOWJONES: ADF=0.37326981807265064, p=0.9804673342610739
- INFLATION_TIP: ADF=-0.8040672742752119, p=0.8179244160272952
- USD_INDEX: ADF=-1.6096630063820272, p=0.47873784987874823
- 10YR_YIELD: ADF=-0.6890697035667345, p=0.8495604530032017
- VIX: ADF=-4.1563646433861905, p=0.0007803817089033634
- CRUDE_OIL: ADF=-2.293736756055715, p=0.1739959501015091
- GOLD: ADF=0.8597030557880061, p=0.9925412488783999

### Correlation Matrix
(See correlation plot in output folder.)


### SARIMA Forecast Diagnostics

- SP500: AIC=1529.41
- NASDAQ100: AIC=1846.45
- DOWJONES: AIC=2018.98
- INFLATION_TIP: AIC=442.98
- USD_INDEX: AIC=516.28
- 10YR_YIELD: AIC=23.95
- VIX: AIC=744.91
- CRUDE_OIL: AIC=788.25
- GOLD: AIC=1324.04

### Machine Learning Baseline

- SP500: MSE=968765.3565
- NASDAQ100: MSE=12969518.1677
- DOWJONES: MSE=28205908.1528
- INFLATION_TIP: MSE=3.1604
- USD_INDEX: MSE=5.0266
- 10YR_YIELD: MSE=0.1019
- VIX: MSE=18.4473
- CRUDE_OIL: MSE=57.7421
- GOLD: MSE=239409.9299

### Structural vs Temporary Indicator Classification

- SP500: structural (score 0.4686642300172832)
- NASDAQ100: structural (score 0.4755317168105291)
- DOWJONES: structural (score 0.43792158105717593)
- INFLATION_TIP: structural (score 0.5085228371810562)
- USD_INDEX: structural (score 0.4925904898764353)
- 10YR_YIELD: structural (score 0.5893491950049596)
- VIX: structural (score 0.3657384123957651)
- CRUDE_OIL: structural (score 0.5372962220529199)
- GOLD: structural (score 0.4750955081630692)