import streamlit as st
from utils.utils import *
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu




# initialize the button_clicked state
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

# Rerun the app after logout
if st.session_state.button_clicked:
    st.session_state.button_clicked = False
    st.experimental_rerun()

#initialize a user account 
UsersCollection = connect_to_db(uri, database_name, "users")
create_user(UsersCollection, "admin", "admin","swordartonline39@gmail.com","massi")

#initialize the authentication status
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = get_authentication_status()

#login form
if st.session_state.authenticated == False:
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
elif st.session_state.authenticated == True:
    #navigation menu in the sidebar
    with st.sidebar:
        page = option_menu("Main menu", options=["Home","Devices" , "Alerts","Map","Historical Data", "Settings","Feedback & Reporting"])
    # Page contents
    if page == "Home":
        st.title(f"Welcome to the {page} page")
        st.write(f"authenticated: {st.session_state.authenticated}")
        st.button('Logout', key='logout', on_click=logout)
    elif page == "Feedback & Reporting":
        st.title(f"this is the {page} page")
    elif page == "Settings":
        st.title(f"this is the {page} page")
    elif page == "Alerts":
        st.title(f"this is the {page} page")
    elif page == "Map":
        st.title(f"this is the {page} page")
    elif page == "Historical Data":
        st.title(f"this is the {page} page")
    elif page == "Devices":
        st.title(f"this is the {page} page")

   


