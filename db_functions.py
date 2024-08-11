#streamlit
import sqlite3
import streamlit as st
from sqlalchemy import create_engine


#DB Connection variables
DB_NAME = st.secrets.db_credentials.db_name 
DB_USER = st.secrets.db_credentials.db_user 
DB_PASS = st.secrets.db_credentials.db_pass 
DB_HOST = st.secrets.db_credentials.db_host 
DB_PORT = st.secrets.db_credentials.db_port 

def insert_data(df):
    # Create the connection string
    # connection_string = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    connection_string = 'sqlite:///database.db'
    
    # Create a SQLAlchemy engine
    engine = create_engine(connection_string)

    # Insert the DataFrame into the PostgreSQL database
    try:
        with engine.connect() as conn:
            df.to_sql(name='fraud_data', con=conn, if_exists='replace')
        
        # with engine.begin() as connection:
        #     df.to_sql(name='fraud_data', con=connection, if_exists='replace')

    except Exception as e:
        print("An error occurred while inserting data into the database.")
        print(str(e))


