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

    notificationsData = get_notifications()
    devicesData = get_devices()
    gdf = pd.DataFrame(devicesData)
    # Create a DataFrame contains eech device name with its qualityIndex data
    if gdf.shape[0] > 0 :
        for i, item in gdf.iterrows():
            data = get_latest_device_data(item['_id'])
            gdf.loc[i, 'qualityIndex'] = data[0].get('qualityIndex')
    
    gdf = gdf.drop(columns=["datas","forcasts"], axis=1)
    st.write(gdf)
    with container:
        devices,notifications = st.columns([2,1])
        generalGraph,Map = st.columns([1,1])
        with devices:
            st.subheader("Devices")
            st.markdown("<span style='height: 10px;'></span>", unsafe_allow_html=True)
            # Create 3 columns for maximum 3 devices
            if(gdf.shape[0] > 0):
                cols = st.columns(min(3, gdf.shape[0]))
            else:
                cols = st.columns(1)
                cols[0].subheader("No devices found")
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
                if(isinstance(notificationsData, list)):
                    for notification in notificationsData:
                        st.write(notification.get('message'))
                else:
                    st.write(notificationsData.get('message'))
        with generalGraph:
            st.subheader("all devices status")
            st.markdown("<span style='height: 30px;'></span>", unsafe_allow_html=True)
            horizontal_bars_chart(gdf, 'deviceName', 'qualityIndex')
      
        with Map:
            st.subheader("Map")
            st.markdown("<span style='height: 10px;'></span>", unsafe_allow_html=True)
            if gdf.shape[0] > 0:
                m = init_map(gdf=gdf)
                m = add_points_to_map(m, gdf)
                # Convert the map to an HTML string
                m_html = m._repr_html_()
                # Display the map
                components.html(m_html, height=310)
            else:
                cols = st.columns(1)
                cols[0].subheader("add at least one device to see the map")