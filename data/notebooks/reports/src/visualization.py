# Create visualizations for the metrics

from data_pipeline import StockDataFetcher
from analysis import PortfolioAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class Visualizer:
    def __init__(self, analyzer: PortfolioAnalyzer):
        self.analyzer = analyzer
        self.prices = analyzer.prices # Historical prices Dataframe
        self.returns = analyzer.returns # Daily returns

    # Create a line plot to plot daily returns.
    def plot_daily_returns(self):
        self.returns.plot() # I'm accessing this form __init__
        plt.title("Daily Returns")
        plt.xlabel("Date")
        plt.ylabel("Return")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # Create a line plot to plot cumulative returns.
    def plot_cumulative_returns(self):
        cum_returns = (1 + self.returns).cumprod() - 1
        cum_returns.plot() # I'm calculating this inside this method, therefore no self is used
        plt.title("Cumulative Returns")
        plt.xlabel("Date")
        plt.ylabel("Returns")
        plt.grid(True)
        plt.tight_layout()
        plt.show()



    # Create a bar chart to plot annualized volatility.
    def plot_annualized_volatility(self):
        std_daily_returns = self.returns.std()
        vol = std_daily_returns * np.sqrt(252)
        plt.bar(vol.index, vol.values)
        plt.title("Annualized Volatility")
        plt.xlabel("Tickers")
        plt.ylabel("Volatility")
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()


    # Create a bar chart to plot annualized return
    def plot_annualized_return(self):
        average_daily_returns = self.returns.mean()  # Take the average of daily returns.
        ann_returns = average_daily_returns * 252
        plt.bar(ann_returns.index, ann_returns.values)
        plt.title("Annualized Returns")
        plt.xlabel("Tickers")
        plt.ylabel("Return")
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()


    # Create a bar chart to plot the Sharpe Ratio.
    def plot_sharpe_ratio(self):
        annualized_returns = self.analyzer.calculate_annualized_return()
        annualized_volatility = self.analyzer.calculate_annualized_volatility()
        risk_free_rate = self.analyzer.risk_free_rate
        sharpe_ratio = (annualized_returns - risk_free_rate) / annualized_volatility
        plt.bar(sharpe_ratio.index, sharpe_ratio.values)
        plt.title("Sharpe Ratio")
        plt.xlabel("Tickers")
        plt.ylabel("Sharpe Ratio")
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()


    # Create a line plot to plot the max drawdown.
    def plot_max_drawdown(self):
        cumulative_returns = self.analyzer.calculate_cumulative_returns()
        running_max = cumulative_returns.cummax()
        drawdown = (running_max - cumulative_returns) / running_max
        max_drawdown = drawdown.max()
        max_drawdown.plot()
        plt.title("Maximun Drawdown")
        plt.xlabel("Tickers")
        plt.ylabel("Max. Drawdown")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # Create a heatmap to display the correlation matrix
    def correlation_heatmap(self):
        corr_matrix = self.analyzer.calculate_correlation_matrix()
        corr_matrix = sns.heatmap(corr_matrix, annot= True, cmap='coolwarm', fmt='.2f')
        plt.title('Correlation Matrix Heatmap')
        plt.show()

    # Create a heatmap to display the covariance matrix
    def covariance_heatmap(self):
        cov_matrix = self.analyzer.calculate_covariance_matrix()
        cov_matrix = sns.heatmap(cov_matrix, annot= True, cmap='coolwarm', fmt='.2f')
        plt.title('Covariance Matrix')
        plt.show()


