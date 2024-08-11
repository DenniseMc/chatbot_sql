import streamlit as st
import pandas as pd
from db_functions import insert_data

def upload_file():
    st.subheader("Upload your .csv file")
    
    uploaded_file = st.file_uploader("Choose a file", type="csv")

    if st.button("Upload"):
        if uploaded_file is not None:
            st.write("Uploading...")
            try:
                df = pd.read_csv(uploaded_file)                
                # Print the content of the file
                st.write("Here is the content of your file:")
                st.write(df.head(5)) 
                insert_data(df)
            except Exception as e:
                st.write("An error occurred while uploading your file.")
                st.write(str(e))
        else:
            st.write("Please upload a csv file.")

