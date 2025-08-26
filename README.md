# 📊 Portfolio Analyzer

Portfolio Analyzer is a Python-based web application built with Streamlit that allows users to 
analyze and optimize stock portfolios. It provides performance metrics, visualizations,
and optimization using historical data fetched from Yahoo Finance.



## 🚀 Features

- Fetches historical **adjusted close** price data via `yfinance`
- Calculates key portfolio metrics:
  - Daily Returns
  - Cumulative Returns
  - Annualized Return
  - Volatility
  - Sharpe Ratio
  - Maximum Drawdown
- Generates Correlation and Covariance Matrices
- Portfolio Optimization using:
  - Maximum Sharpe Ratio
  - Minimum Volatility
- Interactive Streamlit Dashboard
- Saves metrics and portfolio data to a PostgreSQL database

---

## 🛠 Technologies Used

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [NumPy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [yfinance](https://pypi.org/project/yfinance/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [psycopg2](https://pypi.org/project/psycopg2/)
- PostgreSQL

---

## 📦 Installation

 **Clone the repository**
   ```bash
   git clone https://github.com/your-username/portfolio-analyzer.git
   cd portfolio-analyzer

## Create a virtual environment

  python -m venv venv
  source venv/bin/activate#

## Install dependencies

  pip install -r requirements.txt

## PostgreSQL Setup

  Make sure PostgreSQL is installed and running.
  
  Create a database named portfolio_db.
  
  Update your database credentials in database.py

## Run the Streamlit Dashboard:

  streamlit run app.py

## Project Structure
  data/
    notebooks/
      reports/
  src/
    .streamlit/
    analysis.py
    dashboard.py
    data_pipeline.py
    database.py
    db_setup.py
    portfolio_optimizer.py
    README.md
    run.py
    visualization.py
  requirements.txt


  
