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
    # settings_features.Feature_Page(st.session_state["selected_Feature"])
    # Initialize selected_Feature
    if "selected_Feature" not in st.session_state:
        st.session_state["selected_Feature"] = "password_username"
    # the main page
    maincontainer = st.container()
    features, displayfeature = maincontainer.columns([2, 4])
    displayContainer = displayfeature.container()
    with features:
        st.title("Settings")
        st.markdown("<span style='height: 20px;'></span>", unsafe_allow_html=True)
        with open("settings.css") as f:
            st.markdown(
                f"""
                <style>
                    {f.read()}
                </style>
                """,
                unsafe_allow_html=True
            )
        if st.button("Edit Password and username", key="Editpass"):
            st.session_state["selected_Feature"] = "password_username"
            st.rerun()
        if st.button("data updates frequency", key="Editfrequency"):
            st.session_state["selected_Feature"] = "data_upadtes"
            st.rerun()
        if st.button("help", key="help"):
            st.session_state["selected_Feature"] = "help"
            st.rerun()
        if st.button("feedback && reporting", key="feedback"):
            st.session_state["selected_Feature"] = "feedback_reporting"
            st.rerun()
    with displayContainer:
        settings_features.Feature_Page(st.session_state["selected_Feature"])