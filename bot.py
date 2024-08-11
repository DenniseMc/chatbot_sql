#streamlit
import streamlit as st

#langchain
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

#aux
import pandas as pd
import ast

#API_KEY - OPEN AI
API_KEY = st.secrets.api_key 
#DB Connection variables
DB_NAME = st.secrets.db_credentials.db_name 
DB_USER = st.secrets.db_credentials.db_user 
DB_PASS = st.secrets.db_credentials.db_pass 
DB_HOST = st.secrets.db_credentials.db_host 
DB_PORT = st.secrets.db_credentials.db_port 

def start_bot():
    # app config
    st.title("Streaming bot")

    # session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am a bot. How can I help you?"),
        ]

        
    # conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                messages = message.content.split('/')
                if(messages[0] == 'query'):
                    st.code(messages[1], language="sql", line_numbers=False)
                    tuple_data = ast.literal_eval(messages[2])
                    st.write(pd.DataFrame(tuple_data))     
                else:        
                    st.write(message.content)

        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

    # user input
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "":
        st.session_state.chat_history.append(HumanMessage(content=user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            response = get_response(user_query, st.session_state.chat_history)            
            if response['type'] == 'query':
                st.code(response['query'], language="sql", line_numbers=False)
                data = []
                if response['data']:
                    try:
                        data = ast.literal_eval(response['data'])  
                        st.write(pd.DataFrame(data))        
                        st.session_state.chat_history.append(AIMessage(content=f"{response['type']}/{response['query']}/{data}"))         
                    except Exception as e:
                        data = 'Someting happened please try again.'
                        st.write(data)
                        st.session_state.chat_history.append(AIMessage(content=data))
                
            else:
                st.write("I'm sorry, but the question provided is not clear. Kindly provide a valid question.")
                st.session_state.chat_history.append(AIMessage(content=f"I'm sorry, but the question provided is not clear. Kindly provide a valid question."))
            
            
def get_response(user_query, chat_history):
        
        api_key = API_KEY

        try:

            # connection_string = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
            connection_string = 'sqlite:///database.db'
            
            llm = ChatOpenAI(openai_api_key=api_key)
            db = SQLDatabase.from_uri(connection_string)

            chain = create_sql_query_chain(llm, db)        
            response = chain.invoke({"question": user_query, "chat_history": chat_history})   
        
            data = db.run(response)
            return {'type': 'query', 'query': response, 'data': data}            
        except Exception as e:
            print(e)
            return {'type': 'error', 'query': '', 'data': ''}
