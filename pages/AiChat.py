import matplotlib
import streamlit as st
from utils.utils import *
import pandas as pd
from widgets import sidebar
import os
from pandasai import SmartDataframe
from pandasai.responses.response_parser import ResponseParser
from PIL import Image
import io
# from pandasai.callbacks import BaseCallback

# class StreamlitCallback(BaseCallback):
#     def __init__(self, container) -> None:
#         """Initialize callback handler."""
#         self.container = container

#     def on_code(self, response: str):
#         self.container.code(response)


class StreamlitResponse(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)

    def format_dataframe(self, result):
        st.dataframe(result["value"])

    def format_plot(self, result):
        image = Image.open(result["value"])
        st.image(image)

    def format_other(self, result):
        st.write(result["value"])


# configure the page
st.set_page_config(page_title="IOT Dashboard", layout="wide",initial_sidebar_state='expanded')

# llm  = OpenAI(api_token=api_key)
os.environ["PANDASAI_API_KEY"] = api_key


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
    
    # the main content
    st.title("AI Chat")
    devices = get_devices()
    device_names = ['Select ...'] +[device['deviceName'] for device in devices]
    col1,col2 = st.columns(2)
    with col2:
        uploaded_file = st.file_uploader("Choose a file", type=['csv'])
        st.session_state.selected_option = 'Select ...'
        option = st.selectbox(
            'Select a device dataset:',
            device_names, index=device_names.index(st.session_state.selected_option))
        st.session_state.selected_option = option
        if option != 'Select ...':
            device = [device for device in devices if device['deviceName'] == option][0]
            data = get_device_data(device['_id'])
                
        with st.spinner('Loading data...'):
            if uploaded_file is not None:
                st.session_state.selected_option = 'Select ...'
                df = pd.read_csv(uploaded_file)
                st.write(df.tail(5))
                agent = SmartDataframe(df,config={
                    "response_parser": StreamlitResponse,
                })    
                st.success('Data loaded successfully')
            elif option != 'Select ...':
                df = pd.DataFrame(data)
                st.write(df.tail(5))
                agent = SmartDataframe(df,config={
                    "response_parser": StreamlitResponse,
                })  
                st.success('Data loaded successfully')  
            else:
                st.info('Please upload a file or choose a device dataset to start the chat ')
    with col1:
        # display the chat
        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.write(message['content'])
        # react to user input
        prompt = st.chat_input("Enter your message here")
        if prompt:
            # display the user input
            with st.chat_message("user"):
                st.write(prompt)
            # add the user input to the messages state
            st.session_state.messages.append({'role': 'user', 'content': prompt})
            # respond to the user input
            if df is not None:
                response = agent.chat(prompt)
            else:
                response = "Please upload a file to start the chat"
            with st.chat_message("assistant"):
                with st.spinner('Generating response...'):
                    st.write(response)
            # add the response to the messages state
            st.session_state.messages.append({'role': 'assistant', 'content': response})
    