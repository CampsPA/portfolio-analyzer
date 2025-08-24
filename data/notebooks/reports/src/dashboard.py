import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from visualization import Visualizer
# Import the relevant modules
from data_pipeline import StockDataFetcher
from analysis import PortfolioAnalyzer
from portfolio_optimizer import PortfolioOptimizer

# --- Page config --- st.set_page_config(page_title="Portfolio Analyzer", layout="wide")

# --- Sidebar menu ---
menu = ["Home", "Portfolio Metrics", "Portfolio Optimization"]
page = st.sidebar.selectbox("Select Page", menu)

# --- Sidebar inputs (shared for metrics and optimization) ---

st.sidebar.header("User Inputs")
tickers_input = st.sidebar.text_input("Enter tickers (comma separated)")
tickers = [ticker.strip().upper() for ticker in tickers_input.split(',') if ticker.strip()]
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
fetch_data_btn = st.sidebar.button("Fetch Data")

# --- Fetch data ---
if fetch_data_btn:
    fetcher = StockDataFetcher(tickers, start_date, end_date)
    price_data = fetcher.fetch_data()
    if price_data.empty:
        st.error("No data fetched. Check tickers or date range.")
    else:
        st.session_state["price_data"] = price_data

# --- Check if price data exists ---
price_data = st.session_state.get("price_data", None)

# --- Home Page ---
if page == "Home":
    st.markdown(
        '<h1 style="text-align: center;color:#FF0000;">Portfolio Analyzer Dashboard</h1>',
        unsafe_allow_html=True
        )
    image = Image.open(r"C:\Users\campo\OneDrive\Desktop\Data Analysis\premium_photo-1663931932687-c4c2366a5c61.avif")
    st.image(image, use_container_width=True)
    st.write("Welcome! Use the sidebar to navigate between pages.")

# --- Portfolio Metrics Page ---
elif page == "Portfolio Metrics":
    if price_data is not None:
        analyzer = PortfolioAnalyzer(price_data)
        st.subheader("Portfolio Metrics")
        st.write("Daily Returns:")
        st.line_chart(analyzer.calculate_daily_returns())

        st.write("Cumulative Returns:")
        st.line_chart(analyzer.calculate_cumulative_returns())

        st.write("Annualized Returns:")
        st.bar_chart(analyzer.calculate_annualized_return().to_frame())

        st.write("Annualized Volatility:")
        st.bar_chart(analyzer.calculate_annualized_volatility().to_frame())

        st.write("Sharpe Ratios:")
        st.bar_chart(analyzer.calculate_sharpe_ratio().to_frame())

        st.write("Max Drawdown:")
        st.dataframe(analyzer.calculate_max_drawdown().to_frame())

        # Correlation Heatmap
        visualizer = Visualizer(analyzer)
        fig = visualizer.correlation_heatmap()
        st.pyplot(fig)
    else:
        st.warning("Please fetch price data first from the sidebar.")

# --- Portfolio Optimization Page ---
elif page == "Portfolio Optimization":
    if price_data is not None:
        analyzer = PortfolioAnalyzer(price_data)
        optimizer = PortfolioOptimizer(analyzer)
        best_weights = optimizer.run_optimization()
        expected_return, volatility, sharpe_ratio = optimizer.portfolio_performance(best_weights)
        st.subheader("Optimized Portfolio Weights")
        weights_df = pd.DataFrame({
            "Ticker": tickers,
            "Weight (%)": np.round(best_weights * 100, 2)
        })
        st.dataframe(weights_df)

        st.write(f"Expected Return: {expected_return:.4f}")
        st.write(f"Volatility: {volatility:.4f}")
        st.write(f"Sharpe Ratio: {sharpe_ratio:.4f}")
    else:
        st.warning("Please fetch price data first from the sidebar.")