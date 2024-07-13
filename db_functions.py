import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.types import String, Integer, Float, DateTime
import os

port = os.environ.get('PED_DB_PORT')
database = os.environ.get("PED_DB_DATABASE")
username = os.environ.get("PED_DB_USER_NAME")
password = os.environ.get("PED_DB_PASSWORD")
hostname = os.environ.get('PED_DB_HOST_NAME')

def get_sqlalchemy_types(df):
    dtype_map = {
        'object': String,
        'int64': Integer,
        'float64': Float,
        'datetime64[ns]': DateTime,
        # Add other pandas dtypes as needed
    }
    return {col: dtype_map[str(dtype)] for col, dtype in df.dtypes.items()}

def connect_to_db():
    # Create the database connection URL
    db_url = f'postgresql://{username}:{password}@{hostname}:{port}/{database}'
    # Create a SQLAlchemy engine
    engine = create_engine(db_url)
    return engine

def add_pandas_df_to_table(df=None, engine=None, table_name=None):
    """
    Append a pandas DataFrame to a PostgreSQL table.
    Args:
        df (pd.DataFrame): DataFrame to be added to the table.
        engine (sqlalchemy.engine.base.Engine): SQLAlchemy engine to connect to the database.
        table_name (str): Name of the table to add the DataFrame to.
    """
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print("DataFrame inserted successfully.")

def create_table_from_df(df=None, engine=None, table_name=None):
    """
    Create a table in a PostgreSQL database from a pandas DataFrame.
    Args:
        df (pd.DataFrame): DataFrame to be added to the table.
        engine (sqlalchemy.engine.base.Engine): SQLAlchemy engine to connect to the database.
        table_name (str): Name of the table to create.
    """
    # Get the SQLAlchemy types for the DataFrame columns
    dtype_map = get_sqlalchemy_types(df)
    # Create the table
    df.to_sql(table_name, engine, if_exists='replace', index=False, dtype=dtype_map)
    print("Table created successfully.")



if __name__ == '__main__':
    engine = connect_to_db()
