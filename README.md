# Financial Analytics Dashboard

A comprehensive Streamlit web application for financial data analysis and portfolio management. This interactive dashboard provides real-time stock market data, performance analytics, risk metrics, and portfolio insights.

##  Features

### Market Overview
- Real-time stock price data from Yahoo Finance
- Key metrics: Current Price, Total Return, Volatility, Sharpe Ratio
- Normalized price comparison across multiple stocks
- Customizable stock selection and date ranges

### Performance Analysis
- Interactive candlestick charts
- Trading volume visualization
- Daily returns distribution
- Historical price trends

###  Portfolio Analysis
- Equal-weighted portfolio tracking
- Cumulative returns comparison
- Correlation matrix heatmap
- Portfolio-level risk metrics

###  Risk Metrics
- Comprehensive risk metrics table
- Risk-Return scatter plot
- Value at Risk (VaR) calculations
- Maximum drawdown analysis
- Sharpe ratio for risk-adjusted returns

##  Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this project**

2. **Install required packages:**
```bash
pip install -r requirements.txt
```

### Running the Dashboard

```bash
streamlit run financial_dashboard.py
```

The dashboard will open automatically in your default web browser at `http://localhost:8501`

## 📖 How to Use

### Configuration (Sidebar)
1. **Stock Selection**: Enter stock tickers separated by commas (e.g., AAPL, MSFT, GOOGL)
2. **Time Period**: Choose from 1M, 3M, 6M, 1Y, 2Y, 5Y, or Max
3. The dashboard will automatically fetch and analyze the data

### Navigation
- **Overview Tab**: Quick snapshot of all selected stocks with normalized performance
- **Performance Tab**: Detailed analysis of individual stocks with candlestick charts
- **Portfolio Analysis Tab**: Portfolio-level metrics and correlation analysis
- **Risk Metrics Tab**: Comprehensive risk analysis and VaR calculations

##  Key Metrics Explained

- **Total Return**: Percentage change from start date to current
- **Volatility**: Annualized standard deviation of returns (higher = more volatile)
- **Sharpe Ratio**: Risk-adjusted return metric (higher = better risk-adjusted performance)
- **Max Drawdown**: Largest peak-to-trough decline (shows worst-case scenario)
- **VaR (95%)**: Maximum expected loss in a single day, 95% of the time

##  Technical Stack

- **Streamlit**: Interactive web framework
- **yfinance**: Real-time financial data API
- **Plotly**: Interactive data visualizations
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations

##  Use Cases

- **Portfolio Management**: Track and analyze investment portfolios
- **Financial Research**: Compare stocks and analyze market trends
- **Risk Assessment**: Evaluate investment risk profiles
- **Educational**: Learn about financial metrics and portfolio analysis
- **Interview/Portfolio**: Demonstrate finance and data analytics skills

##  Skills Demonstrated

- Financial data analysis and modeling
- Interactive dashboard development
- Data visualization and storytelling
- API integration (Yahoo Finance)
- Python programming (Pandas, NumPy)
- Statistical analysis and risk metrics
- Web application development (Streamlit)

## Disclaimer

This dashboard is for educational and analytical purposes only. The information provided should not be considered as financial advice. Always conduct your own research and consult with financial professionals before making investment decisions.

## Future Enhancements

Potential features to add:
- [ ] Custom portfolio weights
- [ ] Technical indicators (RSI, MACD, Moving Averages)
- [ ] News sentiment analysis
- [ ] Export reports to PDF
- [ ] Machine learning price predictions
- [ ] Cryptocurrency support
- [ ] Economic indicators integration
- [ ] Backtesting functionality

## License

This project is open source and available for educational purposes.

## Contributing

Feel free to fork this project and customize it for your needs. Suggestions and improvements are welcome!

---


