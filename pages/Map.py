import streamlit as st
import pages.login.login_page as login_page
from utils.utils import *

# configure the page
st.set_page_config(page_title="IOT Dashboard", layout="wide",initial_sidebar_state='expanded')

#initialize the authentication status
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = get_authentication_status()

if st.session_state.authenticated == False:
    login_page.show()
elif st.session_state.authenticated == True:
    st.title("this is the Map page")