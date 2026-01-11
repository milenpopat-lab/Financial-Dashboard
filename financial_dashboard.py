import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Financial Analytics Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">📈 Financial Analytics Dashboard</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Stock selection
    default_stocks = ["AAPL", "MSFT", "GOOGL"]
    stock_input = st.text_input(
        "Enter stock tickers (comma-separated)",
        value=", ".join(default_stocks)
    )
    selected_stocks = [s.strip().upper() for s in stock_input.split(",") if s.strip()]
    
    # Date range
    st.subheader("Date Range")
    time_period = st.selectbox(
        "Select Period",
        ["1M", "3M", "6M", "1Y", "2Y", "5Y"],
        index=3
    )
    
    # Map period to dates
    period_map = {
        "1M": 30,
        "3M": 90,
        "6M": 180,
        "1Y": 365,
        "2Y": 730,
        "5Y": 1825
    }
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=period_map[time_period])
    
    # Portfolio allocation
    st.subheader("Portfolio Allocation")
    st.info("Equal weight allocation is used by default")

# Function to fetch stock data
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker, start, end):
    try:
        # Use download method which is more reliable in cloud environments
        df = yf.download(
            ticker, 
            start=start, 
            end=end, 
            progress=False,
            auto_adjust=True
        )
        
        # Check if data is empty
        if df.empty:
            return None
        
        # Ensure we have the columns we need
        if 'Close' not in df.columns and 'close' in df.columns:
            df.rename(columns={'close': 'Close'}, inplace=True)
        
        # For multi-index columns (when ticker is in column name)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        return df
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None

# Function to calculate metrics
def calculate_metrics(df):
    if df is None or df.empty:
        return None
    
    try:
        current_price = df['Close'].iloc[-1]
        start_price = df['Close'].iloc[0]
        
        # Returns
        total_return = ((current_price - start_price) / start_price) * 100
        daily_returns = df['Close'].pct_change().dropna()
        
        # Volatility (annualized)
        volatility = daily_returns.std() * np.sqrt(252) * 100
        
        # Sharpe Ratio (assuming 2% risk-free rate)
        risk_free_rate = 0.02
        excess_returns = daily_returns - (risk_free_rate / 252)
        sharpe_ratio = (excess_returns.mean() / daily_returns.std()) * np.sqrt(252) if daily_returns.std() != 0 else 0
        
        # Max Drawdown
        cumulative = (1 + daily_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min() * 100
        
        return {
            "current_price": current_price,
            "total_return": total_return,
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown
        }
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        return None

# Main content
tabs = st.tabs(["📊 Overview", "📈 Performance", "🎯 Portfolio Analysis", "📉 Risk Metrics"])

# Fetch data for all stocks with progress indicator
if not selected_stocks:
    st.warning("Please enter at least one stock ticker.")
    st.stop()

stock_data = {}
progress_bar = st.progress(0)
status_text = st.empty()

for idx, ticker in enumerate(selected_stocks):
    status_text.text(f"Fetching data for {ticker}... ({idx + 1}/{len(selected_stocks)})")
    data = fetch_stock_data(ticker, start_date, end_date)
    if data is not None and not data.empty:
        stock_data[ticker] = data
    progress_bar.progress((idx + 1) / len(selected_stocks))

progress_bar.empty()
status_text.empty()

# Tab 1: Overview
with tabs[0]:
    st.header("Market Overview")
    
    if not stock_data:
        st.warning("⚠️ No valid stock data available. Please check your ticker symbols and try again.")
    else:
        # Display metrics for each stock
        cols = st.columns(min(len(stock_data), 3))
        
        for idx, (ticker, df) in enumerate(stock_data.items()):
            col_idx = idx % 3
            with cols[col_idx]:
                metrics = calculate_metrics(df)
                if metrics:
                    st.subheader(ticker)
                    st.metric(
                        "Current Price",
                        f"${metrics['current_price']:.2f}",
                        f"{metrics['total_return']:.2f}%"
                    )
                    st.metric("Volatility", f"{metrics['volatility']:.2f}%")
                    st.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
        
        st.markdown("---")
        
        # Price comparison chart
        st.subheader("Price Comparison (Normalized)")
        fig = go.Figure()
        
        for ticker, df in stock_data.items():
            normalized = (df['Close'] / df['Close'].iloc[0]) * 100
            fig.add_trace(go.Scatter(
                x=df.index,
                y=normalized,
                mode='lines',
                name=ticker,
                line=dict(width=2)
            ))
        
        fig.update_layout(
            title="Normalized Price Performance (Base = 100)",
            xaxis_title="Date",
            yaxis_title="Normalized Price",
            hovermode='x unified',
            height=500,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Tab 2: Performance
with tabs[1]:
    st.header("Individual Stock Performance")
    
    if stock_data:
        selected_stock = st.selectbox("Select Stock", list(stock_data.keys()))
        df = stock_data[selected_stock]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Price chart
            fig_price = go.Figure()
            fig_price.add_trace(go.Scatter(
                x=df.index,
                y=df['Close'],
                mode='lines',
                name='Close Price',
                line=dict(color='#2563eb', width=2)
            ))
            
            fig_price.update_layout(
                title=f"{selected_stock} - Price Chart",
                xaxis_title="Date",
                yaxis_title="Price ($)",
                height=400,
                template="plotly_white"
            )
            
            st.plotly_chart(fig_price, use_container_width=True)
        
        with col2:
            # Volume chart (if available)
            if 'Volume' in df.columns:
                fig_volume = go.Figure()
                fig_volume.add_trace(go.Bar(
                    x=df.index,
                    y=df['Volume'],
                    name='Volume',
                    marker_color='lightblue'
                ))
                
                fig_volume.update_layout(
                    title=f"{selected_stock} - Trading Volume",
                    xaxis_title="Date",
                    yaxis_title="Volume",
                    height=400,
                    template="plotly_white"
                )
                
                st.plotly_chart(fig_volume, use_container_width=True)
        
        # Daily returns distribution
        st.subheader("Daily Returns Distribution")
        daily_returns = df['Close'].pct_change().dropna() * 100
        
        fig_dist = px.histogram(
            daily_returns,
            nbins=50,
            title=f"{selected_stock} - Daily Returns Distribution",
            labels={'value': 'Daily Return (%)', 'count': 'Frequency'}
        )
        
        fig_dist.update_layout(
            showlegend=False,
            height=400,
            template="plotly_white"
        )
        
        st.plotly_chart(fig_dist, use_container_width=True)

# Tab 3: Portfolio Analysis
with tabs[2]:
    st.header("Portfolio Analysis")
    
    if stock_data and len(stock_data) > 1:
        # Calculate portfolio performance (equal weight)
        portfolio_returns = pd.DataFrame()
        
        for ticker, df in stock_data.items():
            portfolio_returns[ticker] = df['Close'].pct_change()
        
        # Equal weight portfolio
        portfolio_returns['Portfolio'] = portfolio_returns.mean(axis=1)
        cumulative_returns = (1 + portfolio_returns).cumprod()
        
        # Portfolio value chart
        fig_portfolio = go.Figure()
        
        for col in cumulative_returns.columns:
            fig_portfolio.add_trace(go.Scatter(
                x=cumulative_returns.index,
                y=cumulative_returns[col] * 100,
                mode='lines',
                name=col,
                line=dict(width=3 if col == 'Portfolio' else 1.5)
            ))
        
        fig_portfolio.update_layout(
            title="Portfolio Cumulative Returns (Equal Weight)",
            xaxis_title="Date",
            yaxis_title="Cumulative Return (%)",
            hovermode='x unified',
            height=500,
            template="plotly_white"
        )
        
        st.plotly_chart(fig_portfolio, use_container_width=True)
        
        # Portfolio metrics
        st.subheader("Portfolio Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        portfolio_daily = portfolio_returns['Portfolio'].dropna()
        portfolio_total_return = (cumulative_returns['Portfolio'].iloc[-1] - 1) * 100
        portfolio_volatility = portfolio_daily.std() * np.sqrt(252) * 100
        
        risk_free_rate = 0.02
        excess_returns = portfolio_daily - (risk_free_rate / 252)
        portfolio_sharpe = (excess_returns.mean() / portfolio_daily.std()) * np.sqrt(252) if portfolio_daily.std() != 0 else 0
        
        cumulative = (1 + portfolio_daily).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        portfolio_max_dd = drawdown.min() * 100
        
        col1.metric("Total Return", f"{portfolio_total_return:.2f}%")
        col2.metric("Annualized Volatility", f"{portfolio_volatility:.2f}%")
        col3.metric("Sharpe Ratio", f"{portfolio_sharpe:.2f}")
        col4.metric("Max Drawdown", f"{portfolio_max_dd:.2f}%")
        
        # Correlation matrix
        st.subheader("Correlation Matrix")
        correlation = portfolio_returns.drop('Portfolio', axis=1).corr()
        
        fig_corr = px.imshow(
            correlation,
            text_auto='.2f',
            aspect="auto",
            color_continuous_scale='RdBu_r',
            title="Stock Correlation Matrix"
        )
        
        fig_corr.update_layout(height=500)
        st.plotly_chart(fig_corr, use_container_width=True)
    elif stock_data and len(stock_data) == 1:
        st.info("📊 Add at least 2 stocks to see portfolio analysis and correlation.")
    else:
        st.warning("⚠️ No stock data available for portfolio analysis.")

# Tab 4: Risk Metrics
with tabs[3]:
    st.header("Risk Analysis")
    
    if stock_data:
        # Risk metrics table
        risk_data = []
        
        for ticker, df in stock_data.items():
            metrics = calculate_metrics(df)
            if metrics:
                risk_data.append({
                    "Ticker": ticker,
                    "Current Price": f"${metrics['current_price']:.2f}",
                    "Total Return": f"{metrics['total_return']:.2f}%",
                    "Volatility": f"{metrics['volatility']:.2f}%",
                    "Sharpe Ratio": f"{metrics['sharpe_ratio']:.2f}",
                    "Max Drawdown": f"{metrics['max_drawdown']:.2f}%"
                })
        
        if risk_data:
            risk_df = pd.DataFrame(risk_data)
            st.dataframe(risk_df, use_container_width=True, hide_index=True)
            
            # Risk-Return scatter plot
            st.subheader("Risk-Return Profile")
            
            scatter_data = []
            for ticker, df in stock_data.items():
                metrics = calculate_metrics(df)
                if metrics:
                    scatter_data.append({
                        "Ticker": ticker,
                        "Return": metrics['total_return'],
                        "Volatility": metrics['volatility']
                    })
            
            scatter_df = pd.DataFrame(scatter_data)
            
            fig_scatter = px.scatter(
                scatter_df,
                x='Volatility',
                y='Return',
                text='Ticker',
                title="Risk-Return Profile",
                labels={'Volatility': 'Volatility (%)', 'Return': 'Total Return (%)'}
            )
            
            fig_scatter.update_traces(
                textposition='top center',
                marker=dict(size=15, line=dict(width=2, color='DarkSlateGrey'))
            )
            
            fig_scatter.update_layout(
                height=500,
                template="plotly_white"
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Value at Risk (VaR)
            st.subheader("Value at Risk (VaR) - 95% Confidence")
            
            var_data = []
            for ticker, df in stock_data.items():
                daily_returns = df['Close'].pct_change().dropna()
                var_95 = np.percentile(daily_returns, 5) * 100
                var_data.append({
                    "Ticker": ticker,
                    "1-Day VaR (95%)": f"{var_95:.2f}%",
                    "Interpretation": f"5% chance of losing more than {abs(var_95):.2f}% in a day"
                })
            
            var_df = pd.DataFrame(var_data)
            st.dataframe(var_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>💡 Built with Streamlit | Data source: Yahoo Finance (yfinance)</p>
        <p>⚠️ This dashboard is for educational and analytical purposes only. Not financial advice.</p>
    </div>
""", unsafe_allow_html=True)
