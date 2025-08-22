import sys
import os
import numpy as np

from data.notebooks.reports.src.db_setup import insert_adjusted_prices, clear_db_tables

# Add the parent directory of src to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_pipeline import StockDataFetcher
from analysis import PortfolioAnalyzer
from portfolio_optimizer import PortfolioOptimizer
from visualization import Visualizer
from db_setup import save_performance_metrics, save_portfolio_allocations
from database import get_engine
from db_setup import create_tables

import sys
from db_setup import clear_db_tables
# Clear tables if data exists prior to running the program
if clear_db_tables():
    sys.exit()

# Ask the user if he wants to procedd with the analysis.
proceed = input('Would you like to proceed with the Analysis? (yes/no): ').strip().lower()
if proceed != 'yes':
    print('Exiting program.')
    sys.exit()



def main():

    # Connect to the database:
    engine = get_engine()

    # Create database tables here:
    create_tables()

    tickers_input = input("Enter tickers separated by commas: ")
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(',') if ticker.strip()]

    start = input('Enter start date (YYYY-MM-DD): ').strip()
    end = input('Enter end date (YYYY-MM-DD): ').strip()

    fetcher = StockDataFetcher(tickers, start, end)
    price_data = fetcher.fetch_data()

    print("\n📈 Price Data: ")
    print(price_data)

    # Run PortfolioAnalyzer.
    if price_data.empty:
        print('No data fetched.')


    # Initialize analyzer.
    analyzer = PortfolioAnalyzer(price_data)

    # Run your methods and print the results
    print("\n📈 Daily Returns:")
    print(analyzer.calculate_daily_returns())

    print("\n📈 Cumulative Returns:")
    print(analyzer.calculate_cumulative_returns())

    print("\n📈 Annualized Return:")
    print(analyzer.calculate_annualized_return())

    print("\n📉 Annualized Volatility:")
    print(analyzer.calculate_annualized_volatility())

    print("\n⚖️ Sharpe Ratio:")
    print(analyzer.calculate_sharpe_ratio())

    # Risk Metrics
    print("\n📉 Max Drawdown:")
    print(analyzer.calculate_max_drawdown())

    print("\n Correlation Matrix:")
    print(analyzer.calculate_correlation_matrix())

    print("\n Covariance Matrix:")
    print(analyzer.calculate_covariance_matrix())

    # Portfolio Performance
    optimizer = PortfolioOptimizer(analyzer)
    weights = optimizer.get_weights_input()
    expected_return, volatility, sharpe_ratio = optimizer.portfolio_performance(weights)
    print(f"Expected Return: {expected_return:.4f}")
    print(f"Volatility: {volatility:.4f}")
    print(f"Sharpe Ratio: {sharpe_ratio:.4f}")

    # Optimize Sharpe Ratio
    print("\n🔍 Optimizing portfolio for maximum Sharpe Ratio...")
    try:
        best_weights = optimizer.run_optimization()
        expected_return, volatility, sharpe_ratio = optimizer.portfolio_performance(best_weights)


        # Clean small weights for better readability
        clean_weights = np.round(best_weights, 4)
        percent_weights = clean_weights * 100
        formatted_percent_weights = [f"{weight:.2f}%" for weight in percent_weights] # updated from w to weight

        print("🧹 Optimized Sharpe Ratio Portfolio Weights:", formatted_percent_weights)
        for ticker, weight in zip(tickers, percent_weights):
            print(f"{ticker}: {weight:.2f}%")

        print(f"📈 Optimized Expected Return: {expected_return:.4f}")
        print(f"📉 Optimized Volatility: {volatility:.4f}")
        print(f"⚖️ Optimized Sharpe Ratio: {sharpe_ratio:.4f}")
    except ValueError as e:
        print(f"❌ Optimization failed: {e}")

    # Minimize volatility
    print("\n🔍 Minimize portfolio volatility...")
    try:
        min_vol_weights = optimizer.min_volatility()
        expected_return, volatility, sharpe_ratio = optimizer.portfolio_performance(min_vol_weights)


        # Clean small weights for better readability
        clean_vol_weights = np.round(min_vol_weights, 4)
        percent_min_vol_weights = clean_vol_weights * 100
        formatted_percent_min_vol_weights = [f"{weight:.2f}%" for weight in percent_min_vol_weights] # updated from w to weight
        print("🧹 Minimal Volatility Portfolio Weights:", formatted_percent_min_vol_weights)
        for ticker, weight in zip(tickers, percent_min_vol_weights):
            print(f"{ticker}: {weight:.2f}%")


        print(f"📈 Expected Return: {expected_return:.4f}")
        print(f"📉 Volatility: {volatility:.4f}")
        print(f"⚖️ Sharpe Ratio: {sharpe_ratio:.4f}")

    except ValueError as e:
        print(f"❌ Optimization failed: {e}")


    # Save metrics to the database
    metrics_list = save_performance_metrics(price_data)


    # Save optimized portfolio allocations
    optimized_weights_data = save_portfolio_allocations(
        weights=clean_weights,
        price_data=price_data,
        optimized_sharpe=sharpe_ratio,
        optimized_volatility=volatility,
        min_volatility_weights=clean_vol_weights
    )

    # Save adjusted close prices into the database
    insert_adjusted_prices(price_data)



    '''
    # Visualizations
    viz = Visualizer(analyzer)
    viz.plot_daily_returns()
    viz.plot_cumulative_returns()
    viz.plot_annualized_volatility()
    viz.plot_annualized_return()
    viz.plot_sharpe_ratio()
    viz.plot_max_drawdown()
    viz.correlation_heatmap()
    '''



if __name__ == '__main__':
    price_data = main()