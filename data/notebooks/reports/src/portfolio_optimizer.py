''' The PortfolioOptimizer class contains methods to optimize portfolio performance
by optimizing Sharpe Ratio and minimize portfolio volatility.'''


import numpy as np


from data.notebooks.reports.src.analysis import PortfolioAnalyzer
from scipy.optimize import minimize


class PortfolioOptimizer:
    def __init__(self, analyzer: PortfolioAnalyzer):
        self.analyzer = analyzer
        self.returns = analyzer.returns # This is the daily returns
        self.annualized_returns = analyzer.calculate_annualized_return()
        self.annualized_cov = analyzer.calculate_covariance_matrix()
        self.risk_free_rate = analyzer.risk_free_rate

    # Create a function to calculate performance given a set of weights
    def portfolio_performance(self, weights: np.ndarray) -> tuple: # accept weights
        expected_returns = np.dot(weights, self.annualized_returns)
        volatility = np.sqrt(weights.T @ self.annualized_cov @ weights)
        # excess return divided by the volatility
        sharpe_ratio = (expected_returns - self.risk_free_rate) / volatility
        return expected_returns, volatility, sharpe_ratio

    # Allow user to input the weights
    def get_weights_input(self) -> np.ndarray:
        n_assets = len(self.returns.columns) # ask the user for porfolio weights, return a NumPy array
        tickers = self.returns.columns.tolist()
        # converts the assets list from pandas index object
        # into a plain Python list

        # Display tickers to the user
        print('\nYour Portfolio Assets: ')
        for idx, ticker in enumerate(tickers):
            print(f"{idx + 1}. {ticker}")

        print("\nAssigning equal weights to all assets.")
        weights = np.array([1 / n_assets] * n_assets)
        return weights


    # Create a function to optimize the Sharpe ratio
    def optimize_sharpe_ratio(self, weights):
        expected_returns = np.dot(weights, self.annualized_returns)
        cov_matrix = self.annualized_cov
        risk_free_rate = self.risk_free_rate

        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (expected_returns - self.risk_free_rate) / portfolio_volatility
        return  -sharpe_ratio

    # Create a function to run shape ration optimization (maximize)
    def run_optimization(self):
        num_assets = len(self.annualized_returns)

        # Start with equal weights for all assets
        initial_weights = np.ones(num_assets) / num_assets

        # Set bounds for each asset's weight: must be between 0 and 1
        bounds = tuple((0,1) for _ in range(num_assets))

        # Constraint: weights must sum to 1 to be a fully invested portfolio
        constraints = {'type': 'eq', 'fun': lambda  w:np.sum(w) - 1} # rewrite this!

        result = minimize(
            fun = self.optimize_sharpe_ratio,
            x0 = initial_weights,
            method= 'SLSQP',
            bounds = bounds,
            constraints = constraints
        )
        if result.success:
            return result.x # Optimized weight
        else:
            raise ValueError("Optimization failed" + result.message)

    # Crete a function to minimize volatility
    def optimize_volatility(self, weights):
        cov_matrix = self.annualized_cov
        portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
        volatility = np.sqrt(portfolio_variance)

        return volatility


    # Create a function to minimize volatility
    def min_volatility(self):
        num_assets = len(self.annualized_returns)
        # Start with equal weights for all assets
        initial_weights = np.ones(num_assets) / num_assets

        # Set bounds for each asset's weight: must be between 0 and 1
        bounds = tuple((0, 1) for _ in range(num_assets))

        # Constraint: weights must sum to 1 to be a fully invested portfolio
        constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}  # rewrite this!

        result = minimize(fun=self.optimize_volatility,
                 x0=initial_weights,
                 method='SLSQP',
                 bounds=bounds,
                 constraints=constraints
                 )
        if result.success:
            return result.x  # Optimized weight
        else:
            raise ValueError("Optimization failed" + result.message)










