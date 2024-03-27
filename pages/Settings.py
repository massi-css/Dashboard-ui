import streamlit as st
from utils.utils import *
from widgets import sidebar
import pages.single.settings_features as settings_features 
# configure the page
st.set_page_config(page_title="IOT Dashboard", layout="wide",initial_sidebar_state='expanded')

#initialize the authentication status
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = get_authentication_status()

if st.session_state.authenticated == False:
    st.switch_page("pages/login_page.py")
elif st.session_state.authenticated == True:
    # the sidebar
    sidebar()
    
    # Initialize selected_Feature
    if "selected_Feature" not in st.session_state:
        st.session_state["selected_Feature"] = "Settings"

    # No button selected show main page else show the page of each feature
    if st.session_state.get("selected_Feature") == "Settings":  
        #CSS
        with open("settings.css") as f:
            st.markdown(
                f"""
                <style>
                    {f.read()}
                </style>
                """,
                unsafe_allow_html=True
            )
        st.title("Settings")

        num_columns = 3
        columns = st.columns(num_columns)


        if st.button("Edit password and username"):
            st.session_state["selected_Feature"] = "password_username"
            st.rerun()
            
        if st.button("Data upadtes frequency"):
            st.session_state["selected_Feature"] = "data_upadtes"
            st.rerun()
            
        if st.button("Help"):
            st.session_state["selected_Feature"] = "help"
            st.rerun()
            
        if st.button("Feedback & Reporting"):
            st.session_state["selected_Feature"] = "feedback_reporting"
            st.rerun()        
    else:
        settings_features.Feature_Page(st.session_state["selected_Feature"])



        
        