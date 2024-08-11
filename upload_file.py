import streamlit as st
import pandas as pd
from db_functions import insert_data

def upload_file():
    st.subheader("Upload your .csv file")
    st.warning('The new file will overwrite the current file.', icon="⚠️")
    uploaded_file = st.file_uploader("Select a csv file", type="csv")

    if st.button("Upload", type="primary"):
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)  
                new_df = cast_date(df)
                result = insert_data(new_df) 
                if (result['status']): 
                    st.success('File Uploaded Successfully', icon="✅")
                    with st.expander(":card_index_dividers: Table structure:"):
                        st.write(result['columns'])    
                    with st.expander(":mag_right: Data preview"):
                        st.write(new_df.head(5))    
                else:
                    st.error('Something went wrong, please try again', icon="🚨")
                
            except Exception as e:
                st.write("An error occurred while uploading your file.")
                st.write(str(e))
        else:
            st.write("Please upload a csv file.")


def cast_date(df):
   
    for column in df.columns:
        try:
            if df[column].dtype == 'object':
                # Try to convert column to datetime
                df[column] = pd.to_datetime(df[column],format='mixed', errors='raise')
        except Exception as e:
            print(e)
    return df

