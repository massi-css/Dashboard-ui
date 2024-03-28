import streamlit as st
from utils.utils import *
from widgets import *
import streamlit.components.v1 as components
import pandas as pd



# configure the page
st.set_page_config(page_title="IOT Dashboard", layout="wide",initial_sidebar_state='expanded')


#initialize the authentication status
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = get_authentication_status()

#verification of the authentication status
if st.session_state.authenticated == False:
    st.switch_page("pages/login_page.py")
elif st.session_state.authenticated == True:
    # the sidebar
    sidebar()
    with open("home.css") as f:
        st.markdown(
            f"""
            <style>
                {f.read()}
            </style>
            """,
            unsafe_allow_html=True
        ) 
    st.title("Welcome")
    st.markdown("<span style='height: 20px;'></span>", unsafe_allow_html=True)
    container = st.container()

    # notificationsData= ["notification1", "notification2", "notification3", "notification4"]
    notificationsData = get_notifications()

    # devicesData = [
    #         {'deviceName': 'Device 1', 'location': 'blida', 'status': 'Active','longitude': 36.531513, 'latitude': 2.967012},
    #         {'deviceName': 'Device 2', 'location': 'alger', 'status': 'Inactive','longitude': 36.752887, 'latitude': 3.042048},
    #         {'deviceName': 'Device 3', 'location': 'oran', 'status': 'Active','longitude': 35.691111, 'latitude': -0.641667},
    #         {'deviceName': 'Device 4', 'location': 'constantine', 'status': 'Active','longitude': 36.365, 'latitude': 6.614722},
    #         {'deviceName': 'Device 5', 'location': 'annaba', 'status': 'Inactive','longitude': 36.9, 'latitude': 7.767}
    #     ]
    devicesData = get_devices()
    gdf = pd.DataFrame(devicesData)

    with container:
        devices,notifications = st.columns([2,1])
        chat,Map = st.columns([1,2])
        with devices:
            st.subheader("Devices")
            st.markdown("<span style='height: 10px;'></span>", unsafe_allow_html=True)
            # Create 3 columns for maximum 3 devices
            cols = st.columns(min(3, gdf.shape[0]))
            # Loop through the data
            for i, item in gdf.head(3).iterrows():
                # Select the column
                col = cols[i % 3]
                # Create the card
                col.header(item['deviceName'])
                col.write(f"Status: {item['status']}")
                col.write(f"Location: {item['location']}")
            
        with notifications:
            st.subheader("Notifications")
            st.markdown("<span style='height: 10px;'></span>", unsafe_allow_html=True)
            notificationContainer = st.container()
            # st.write("List of notifications")
            with notificationContainer:
                for notification in notificationsData:
                    st.write(notification.get('message'))
        with chat:
            st.subheader("Chat")
            st.markdown("<span style='height: 10px;'></span>", unsafe_allow_html=True)
            st.markdown("<hr/>", unsafe_allow_html=True)
            st.write("Chat with ai")
            st.markdown("<hr/>", unsafe_allow_html=True)
        with Map:
            st.subheader("Map")
            st.markdown("<span style='height: 10px;'></span>", unsafe_allow_html=True)
            m = init_map(gdf=gdf)
            m = add_points_to_map(m, gdf)
            # Convert the map to an HTML string
            m_html = m._repr_html_()
            # Display the map
            components.html(m_html, height=420)