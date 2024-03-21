import streamlit as st
from utils.utils import *
from widgets import *
import pages.login.login_page as login_page



# configure the page
st.set_page_config(page_title="IOT Dashboard", layout="wide",initial_sidebar_state='expanded')


#initialize the authentication status
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = get_authentication_status()

#verification of the authentication status
if st.session_state.authenticated == False:
    login_page.show()
elif st.session_state.authenticated == True:
    st.title("welcome to your IOT Dashboard")
    st.button('Logout', key='logout', on_click=logout)