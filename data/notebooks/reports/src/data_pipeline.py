''' This program allows the user to fetch stock data from Yahoo Finance,
saves the data into a CSV file, and load the data from the CSV file.'''

import yfinance as yf
import pandas as pd
from typing import List

class StockDataFetcher:
    def __init__(self, tickers: List[str],start_date: str, end_date: str):
        self.tickers = [t.upper() for t in tickers]
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def fetch_data(self) -> pd.DataFrame:
        try:
            df = yf.download(
                self.tickers,
                start=self.start_date,
                end=self.end_date,
                auto_adjust=False,
                progress=False
            )
            if isinstance(df.columns,pd.MultiIndex):
                # Select only the 'Adj Close' level
                adj_close = df['Adj Close']
            else:
                # Single ticker case.
                adj_close = df[['Adj Close']] if 'Adj Close' in df.columns else df[['Close']]

            self.data = adj_close.dropna(how='all') #drop missing values
            return self.data
        except Exception as e:
            print(f"Failed to fetch data {e}")
            return pd.DataFrame()

    # Create a function to save the data into csv.
    def save_to_csv(self, path):
        if self.data is not None:
            self.data.to_csv(path)
        else:
            print('No data to save.')

    # Create a function to load the data from the csv file.
    def load_from_csv(self, path):
        try:
            self.data = pd.read_csv(path, index_col=0, parse_dates=True)
            return self.data
        except FileNotFoundError:
            print(f'File not found: {path}')
            return pd.DataFrame()