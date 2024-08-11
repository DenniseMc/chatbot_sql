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
from io import StringIO

#db functions
from db_functions import get_table_structure,get_table_info, execute_query

#API_KEY - OPEN AI
API_KEY = st.secrets.api_key 
connection_string = 'sqlite:///database.db'

def start_bot():
    # app config
    st.title(":right_anger_bubble: SQL bot")
    info = get_table_info()
    if (info['status']):
        with st.expander(":grey_question: Help"):
            st.write(":card_index_dividers: Table structure:")
            st.write(get_table_structure())    
            st.write(":mag_right: Data preview")
            st.write(info['data']) 
        # session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                AIMessage(content="Hello, I’m a SQL bot. Feel free to ask me any questions about the uploaded dataset."),
            ]
            
        # conversation
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI"):
                    try:
                        messages = message.content.split('/')
                        if(messages[0] == 'query'):
                            st.code(messages[1], language="sql", line_numbers=False)
                            # Convert the string to a DataFrame
                            df = pd.read_csv(StringIO(messages[2]))
                            st.write(df)     
                        else:        
                            st.write(message.content)
                    except Exception as e:
                        print(e)
                        st.write('Something went wrong please try again')

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
                    data = response['data']
                    try:
                        st.write(data)
                        # Convert dataframe to string
                        csv_string = data.to_csv(index=False)
                        # Append history       
                        st.session_state.chat_history.append(AIMessage(content=f"{response['type']}/{response['query']}/{csv_string}"))         
                    except Exception as e:
                        data = 'Something went wrong please try again.'
                        st.write(data)
                        # Append history       
                        st.session_state.chat_history.append(AIMessage(content=data))
                    
                else:
                    st.write("I'm sorry, but the question provided is not clear. Kindly provide a valid question.")
                    st.session_state.chat_history.append(AIMessage(content=f"I'm sorry, but the question provided is not clear. Kindly provide a valid question."))
    else:
        st.error('Please upload a file', icon="🚨")

    
            
            
def get_response(user_query, chat_history):
        
        api_key = API_KEY

        try:

            llm = ChatOpenAI(openai_api_key=api_key)
            db = SQLDatabase.from_uri(connection_string)
            chain = create_sql_query_chain(llm, db)        
            response = chain.invoke({"question": user_query, "chat_history": chat_history})   
            data = execute_query(response)
            if data is not None:
                return {'type': 'query', 'query': response, 'data': data}  
            else:
                return {'type': 'error', 'query': '', 'data': ''}
        except Exception as e:
            print(e)
            return {'type': 'error', 'query': '', 'data': ''}
