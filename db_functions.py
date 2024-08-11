from sqlalchemy import create_engine
import pandas as pd

connection_string = 'sqlite:///database.db'

def insert_data(df):
    # Create a SQLAlchemy engine
    engine = create_engine(connection_string)

    # Insert the DataFrame into the SQLite database
    try:
        with engine.connect() as conn:
            df.to_sql(name='data', con=conn, if_exists='replace')
            # Query to get column names and types
            query = "PRAGMA table_info(data)"
            result_df = pd.read_sql(query, conn)
            # Select name and type
            result_df = result_df[['name', 'type']]

        return {'status': True, 'columns': result_df}
        
    except Exception as e:
        print("An error occurred while inserting data into the database.")
        print(str(e))
        return {'status': False}

def get_table_structure():
    
    # Create a SQLAlchemy engine
    engine = create_engine(connection_string)
    # Insert the DataFrame into the SQLite database
    try:
        with engine.connect() as conn:
            # Query to get column names and types
            query = "PRAGMA table_info(data)"
            result_df = pd.read_sql(query, conn)
            # Select name and type
            result_df = result_df[['name', 'type']]
            
        return result_df
        
    except Exception as e:
        print("An error occurred while inserting data into the database.")
        print(str(e))

def get_table_info():
    
    # Create a SQLAlchemy engine
    engine = create_engine(connection_string)
    # Insert the DataFrame into the SQLite database
    try:
        with engine.connect() as conn:
            # Query to get column names and types
            query = "SELECT * FROM data LIMIT 5"
            result_df = pd.read_sql(query, conn)

        return {'status': True, 'data': result_df}
        
    except Exception as e:
        print("An error occurred while inserting data into the database.")
        print(str(e))
        return {'status': False}


def execute_query(query):
    # Create a SQLAlchemy engine
    engine = create_engine(connection_string)
    try:
        with engine.connect() as conn:
            # Query to get column names and types
            result_df = pd.read_sql(query, conn)
        return result_df
        
    except Exception as e:
        print("An error occurred while inserting data into the database.")
        print(str(e))




