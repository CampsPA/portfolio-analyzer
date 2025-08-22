# Here I will have the logic to create a database, connect to database

from sqlalchemy import create_engine


# Create a database connection with PostgreSQL
def get_engine():
    # Create connection to PostgreSQL
    username = 'postgres'
    password = 'Campospa'
    host = 'localhost'
    port = '5433'
    database = 'portfolio_db'  # Create database manually in postgres

    # Create database engine.
    engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")
    return engine
