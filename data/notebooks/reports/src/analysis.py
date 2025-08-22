# The PortfolioAnalyzer class contains methods to calculate various financial metrics.

import pandas as pd
import numpy as np



class PortfolioAnalyzer:
    def __init__(self, price_data: pd.DataFrame, risk_free_rate: float = 0.03):
        self.prices = price_data
        self.risk_free_rate = risk_free_rate
        self.returns = self.calculate_daily_returns() # daily returns stored here for reuse.

    # Calculate daily returns.
    def calculate_daily_returns(self) -> pd.DataFrame:
        daily_returns = self.prices.pct_change().dropna()
        return daily_returns

    # Calculate cumulative returns
    def calculate_cumulative_returns(self) -> pd.DataFrame:
        cumulative_returns = (1 + self.returns).cumprod().dropna()
        return cumulative_returns

    # Calculate annualized volatility.
    def calculate_annualized_volatility(self) -> pd.Series:
        std_daily_returns = self.returns.std()
        annualized_volatility = std_daily_returns * np.sqrt(252)
        return annualized_volatility


    # Calculate annualized return.
    def calculate_annualized_return(self) -> pd.Series:
        average_daily_returns = self.returns.mean() # Take the average of daily returns.
        annualized_returns = average_daily_returns * 252
        return annualized_returns

    # Calculate Sharpe Ratio.
    def calculate_sharpe_ratio(self) -> pd.Series:
        annualized_returns = self.calculate_annualized_return()
        annualized_volatility = self.calculate_annualized_volatility()
        sharpe_ratio = (annualized_returns - self.risk_free_rate) / annualized_volatility
        return sharpe_ratio

    # calculate max drawdown.
    # Indicates the max pct drop from the previous high.
    def calculate_max_drawdown(self) -> pd.Series:
        cumulative_returns = self.calculate_cumulative_returns()
        running_max = cumulative_returns.cummax()
        drawdown = (running_max - cumulative_returns ) / running_max
        max_drawdown = drawdown.max()
        return max_drawdown

    # Create a function that calculates correlation between assets
    def calculate_correlation_matrix(self) -> pd.DataFrame:
        return self.returns.corr()


    # Create a function that calculates correlation between assets
    def calculate_covariance_matrix(self) -> pd.DataFrame:
        return self.returns.cov() * 252
