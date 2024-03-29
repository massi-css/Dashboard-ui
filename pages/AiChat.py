import streamlit as st
from utils.utils import *
import pandas as pd
from widgets import sidebar
import os
from pandasai import SmartDataframe

# configure the page
st.set_page_config(page_title="IOT Dashboard", layout="wide",initial_sidebar_state='expanded')

#initialize the authentication status
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = get_authentication_status()

if st.session_state.authenticated == False:
    st.switch_page("pages/login_page.py")
elif st.session_state.authenticated == True:
    # initialize the messages state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    # the sidebar
    sidebar()
    os.environ["PANDASAI_API_KEY"] = api_key
    # the main content
    st.title("AI Chat")
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])
    with st.spinner('Loading data...'):
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write(df.tail(5))
            agent = SmartDataframe(df)
            st.success('Data loaded successfully')
        else:
            st.info('Please upload a file to start the chat')
    # display the chat
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])
    # react to user input
    prompt = st.chat_input("Enter your message here")
    if prompt:
        # display the user input
        with st.chat_message("user"):
            st.markdown(prompt)
        # add the user input to the messages state
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        # respond to the user input
        response = agent.chat(prompt)
        with st.chat_message("assistant"):
            with st.spinner('Generating response...'):
                st.write(response)
        # add the response to the messages state
        st.session_state.messages.append({'role': 'assistant', 'content': response})
    