# Financial Analytics Dashboard

Interactive stock market analysis and portfolio management platform built with Python and Streamlit.

## Features

**Market Analysis**
- Real-time stock data via yfinance API
- Normalized price comparison across multiple tickers
- Candlestick charts with volume analysis
- Daily returns distribution

**Portfolio Management**
- Equal-weight portfolio tracking
- Cumulative returns visualization
- Correlation matrix analysis
- Multi-stock comparison

**Risk Metrics**
- Sharpe ratio calculations
- Value at Risk (VaR) at 95% confidence
- Maximum drawdown analysis
- Volatility measurements (annualized)
- Risk-return scatter plots

**Financial Ratios**
- Return on Assets (ROA)
- Return on Equity (ROE)
- Net profit margins
- Asset turnover ratios

## Tech Stack

- Python 3.8+
- Streamlit - Web framework
- yfinance - Financial data API
- Plotly - Interactive visualizations
- Pandas - Data manipulation
- NumPy - Numerical computations

## Installation

```bash
pip install -r requirements.txt
streamlit run financial_dashboard.py
```

## Usage

1. Enter stock tickers (comma-separated)
2. Select analysis period (1M to 5Y)
3. Navigate through tabs:
   - Overview: Quick metrics and price comparison
   - Performance: Individual stock analysis
   - Portfolio: Multi-stock performance
   - Risk Metrics: Comprehensive risk analysis

## Default Stocks

- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Google)

Can analyze any publicly traded company via ticker symbol.

## Key Calculations

**Sharpe Ratio**
- Formula: (Portfolio Return - Risk-Free Rate) / Standard Deviation
- Assumes 2% risk-free rate
- Annualized calculation

**Value at Risk (VaR)**
- 95% confidence level
- Historical method
- Daily timeframe

**Maximum Drawdown**
- Peak-to-trough decline
- Percentage basis
- Rolling calculation

## File Structure

```
financial-analytics-dashboard/
├── financial_dashboard.py    # Main application
├── requirements.txt           # Dependencies
└── README.md                 # Documentation
```

## Live Demo

https://financial-dashboard-m1926.streamlit.app/

## Data Source

Yahoo Finance via yfinance library. Data refreshes on page load with 1-hour cache.

## Requirements

```
streamlit>=1.28.0
yfinance>=0.2.28
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
```

## Deployment

Deploy to Streamlit Cloud:
1. Push code to GitHub
2. Connect repository at share.streamlit.io
3. Select financial_dashboard.py as main file
4. Deploy

## Notes

- Annual data only (not quarterly)
- Cache TTL: 3600 seconds (1 hour)
- Supports up to 5 years historical data
- Optimized for desktop viewing
