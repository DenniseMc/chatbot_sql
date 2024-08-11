import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv('.env')

#DB Connection variables
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def insert_data(df):
    # Create the connection string
    connection_string = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    # Create a SQLAlchemy engine
    engine = create_engine(connection_string)

    # Insert the DataFrame into the PostgreSQL database
    try:
        with engine.begin() as connection:
            df.to_sql(name='fraud_data', con=connection, if_exists='replace')

    except Exception as e:
        print("An error occurred while inserting data into the database.")
        print(str(e))


