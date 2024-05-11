import streamlit as st
from utils.utils import *
from widgets import sidebar

# configure the page
st.set_page_config(page_title="IOT Dashboard", layout="wide",initial_sidebar_state='expanded')

#initialize the authentication status
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

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
    st.markdown("<span style='height: 20px;'></span>", unsafe_allow_html=True)
    notificationsData = get_notifications()
      
    notificationContainer = st.container()
    if isinstance(notificationsData,list):
        with notificationContainer:
            for notification in notificationsData:
                notif = f"{notification['message']} \n Time : {notification['createdAt']}"
                st.write(notif)
    else:
        st.write("No notifications available")
        