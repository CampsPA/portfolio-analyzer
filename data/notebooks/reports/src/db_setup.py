# Here I will create the necessary database tables

from sqlalchemy import text
from database import get_engine
from analysis import PortfolioAnalyzer
from portfolio_optimizer import PortfolioOptimizer
import pandas as pd
from datetime import date as dt_date

# Connect to the database:
engine = get_engine()

# Define SQL statements.
create_tables_sql = """
CREATE TABLE IF NOT EXISTS portfolio_metrics (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR,
    date DATE,
    cumulative_return NUMERIC,
    annualized_return NUMERIC,
    annualized_volatility NUMERIC,
    sharpe_ratio NUMERIC,
    max_drawdown NUMERIC
);

CREATE TABLE IF NOT EXISTS portfolio_allocations (
    id SERIAL PRIMARY KEY,
    date DATE,
    ticker VARCHAR,
    weight NUMERIC,
    optimized_sharpe_ratio NUMERIC,
    optimized_volatility NUMERIC,
    minimum_volatility_portfolio NUMERIC
); 

CREATE TABLE IF NOT EXISTS adjusted_prices (
    id SERIAL,
    ticker VARCHAR,
    date DATE,
    adj_close NUMERIC
);
"""

# Create a function to create the tables.
def create_tables():
    try:
        with engine.begin() as conn:
            conn.execute(text(create_tables_sql))
            print("All tables created successfully.")
    except Exception as e:
        print("Failed to create tables:", e)
        exit()

# Create a function to save the relevant performance metrics
def save_performance_metrics(price_data):
    # Initialize analyzer.
    analyzer = PortfolioAnalyzer(price_data)
    today = pd.Timestamp.today().date()
    metrics_list = []
    for ticker in price_data.columns:
        metrics = {
            "date": today,
            "ticker": ticker,
            "cumulative_return": float(analyzer.calculate_cumulative_returns()[ticker].iloc[-1]),
            "annualized_volatility": float(analyzer.calculate_annualized_volatility()[ticker]),
            "annualized_return": float(analyzer.calculate_annualized_return()[ticker]),
            "sharpe_ratio": float(analyzer.calculate_sharpe_ratio()[ticker]),
            "max_drawdown": float(analyzer.calculate_max_drawdown()[ticker])
        }

        metrics_list.append(metrics)

     # Insert performance metrics data into the database
    # Use .begin() instead of .connect() to allow for automatic commit
    with engine.begin() as conn:
        for row in metrics_list:
            conn.execute(text("""
            INSERT INTO portfolio_metrics 
            (date, ticker, cumulative_return, annualized_return, annualized_volatility, 
            sharpe_ratio, max_drawdown)
            VALUES (:date, :ticker, :cumulative_return, :annualized_return, 
            :annualized_volatility, :sharpe_ratio, :max_drawdown)
            """), row)

    return metrics_list


# Create a function to save portfolio allocations (weights) and optimized metrics
def save_portfolio_allocations(weights, price_data, optimized_sharpe, optimized_volatility, min_volatility_weights):
    today = pd.Timestamp.today().date()
    optimized_weights_metrics = []
    for i, ticker, in enumerate(price_data.columns): # create a Tuple pairing tickers with weights
        optimized_weights_metrics.append({
            "date": today,
            "ticker": ticker,
            "weight": float(weights[i]),
            "optimized_sharpe_ratio": float(optimized_sharpe),
            "optimized_volatility": float(optimized_volatility),
            "minimum_volatility_portfolio": float(min_volatility_weights[i])
        })

    # Insert allocations data into the database
    with engine.begin() as conn:
        for row in optimized_weights_metrics:
            conn.execute(text("""
            INSERT INTO portfolio_allocations
            (date, ticker, weight, optimized_sharpe_ratio, 
            optimized_volatility, minimum_volatility_portfolio)
            VALUES (:date, :ticker, :weight, :optimized_sharpe_ratio, 
            :optimized_volatility, :minimum_volatility_portfolio)"""), row)


    return optimized_weights_metrics

# Create a function to insert adjusted close prices to the database
def insert_adjusted_prices(df: pd.DataFrame):
    df = df.copy()
    df.index = pd.to_datetime(df.index)

    with engine.begin() as conn:
        for date, row in df.iterrows():
            for ticker, price in row.items():
                if pd.notna(price):
                    conn.execute(
                        text("""
                        INSERT INTO adjusted_prices (date, ticker, adj_close)
                        VALUES (:date, :ticker, :adj_close)
                        """),
                        {
                            "date": date.date() if isinstance(date, pd.Timestamp) else date,
                            "ticker": str(ticker),
                            "adj_close": float(price)
                        }
                    )

# Commenting out this section since streamlit does not accept input()
# Keeping the logic for debugging purposes.
def clear_db_tables():
    #confirm = input("Do you want to clear all tables? (yes/no): ").strip().lower()
    #if confirm != 'yes':
        #print("Aborted clearing tables.")
        #return False

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM adjusted_prices"))
        conn.execute(text("DELETE FROM portfolio_allocations"))
        conn.execute(text("DELETE FROM portfolio_metrics"))
        print("Tables cleared")
    return  True



