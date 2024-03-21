import streamlit as st
from utils.utils import *


#initialize the collections
UsersCollection = connect_to_db(uri, database_name, "users")
def show():
    # CSS hiding the sidebar
    st.markdown("""
    <style>
    .st-emotion-cache-1cypcdb{
        display: none !important;
    }
    .main{
        padding-left: 300px;
        padding-right: 300px;
    }
    </style>
    """, unsafe_allow_html=True)

    # login form
    st.title('Login page')
    with st.form(key='my_form'):
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        submit_button = st.form_submit_button('Login')
        if submit_button:
            if authenticate_user(UsersCollection, username, password):
                st.success('You are now logged in!')
                st.session_state.authenticated = set_authentication_status(True)
                st.experimental_rerun()
            else:
                st.error('Invalid username or password')