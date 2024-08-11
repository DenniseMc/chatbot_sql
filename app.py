import streamlit as st 
import streamlit.components.v1 as stc 
import pandas as pd
from bot import start_bot
from upload_file import upload_file

html_temp = """
    <div style="background-color:#ed8e1a;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Streamlit Chatbot with SQL Integration</h1>
    </div>
    """

def main():
    st.set_page_config(page_title="Streaming bot", page_icon="🤖")    
    stc.html(html_temp)

    # Sidebar navigation
    st.sidebar.title("Navigation")
    menu = [":file_folder: Upload file", ":robot_face: Bot"]
    
    choice = st.sidebar.radio(
        "Select an option",
        menu,
        captions=[
            "Add data",
            "Ask questions",
        ],
    )

    
    if choice == ":file_folder: Upload file":
        upload_file()
    
    elif choice == ":robot_face: Bot":
        start_bot()
            
if __name__ == '__main__':
    main()
