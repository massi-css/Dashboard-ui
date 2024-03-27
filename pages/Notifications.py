import streamlit as st
from utils.utils import *
from widgets import sidebar

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
    with open("notifications.css") as f:
        st.markdown(
            f"""
            <style>
                {f.read()}
            </style>
            """,
            unsafe_allow_html=True
        ) 
    st.title("Notifications")
    
    notificationsData= ["Notification1", "Notification2", "Notification3", "Notification4"]
      
    notificationContainer = st.container()
    # st.write("List of notifications")
    with notificationContainer:
        for notification in notificationsData:
            st.write(notification)
        