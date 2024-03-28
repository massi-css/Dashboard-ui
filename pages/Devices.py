import streamlit as st
import pages.single.single_device as single_device 
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
    # Initialize device_num
    if "device_num" not in st.session_state:
        st.session_state["device_num"] = -1
    # No device selected show main page else show the dasboard of each device
    if st.session_state.get("device_num") == -1:  
        #CSS
        with open("devices_page_Style.css") as f:
            st.markdown(
                f"""
                <style>
                    {f.read()}
                </style>
                """,
                unsafe_allow_html=True
            )
        st.title("Devices")
        # Columns
        num_columns = 3
        columns = st.columns(num_columns)
        # Data
        # devices = [
        #     {'Name': 'Device 1', 'Location': 'blida', 'Status': 'Active','Longitude': 36.531513, 'Latitude': 2.967012},
        #     {'Name': 'Device 2', 'Location': 'alger', 'Status': 'Inactive','Longitude': 36.752887, 'Latitude': 3.042048},
        #     {'Name': 'Device 3', 'Location': 'oran', 'Status': 'Active','Longitude': 35.691111, 'Latitude': -0.641667},
        #     {'Name': 'Device 4', 'Location': 'constantine', 'Status': 'Active','Longitude': 36.365, 'Latitude': 6.614722},
        #     {'Name': 'Device 5', 'Location': 'annaba', 'Status': 'Inactive','Longitude': 36.9, 'Latitude': 7.767}
        # ]
        devices = get_devices()
        i = -1
        if len(devices) > 0:
            # Iterate over devices
            for i, device in enumerate(devices):
                col_index = i % num_columns
                container = columns[col_index].container()
                # Write device information to the container
                container.title(device['deviceName'])
                container.write(f"Location: {device['location']}")
                buttonContainer = container.container()
                
                # Button to show dashboard
                #giving it a speacial key to identify it
                button_key = device["_id"]
                # add new device card
                if buttonContainer.button("See dashboard", key=button_key):
                    st.session_state["device_num"] = device["_id"]
                    st.rerun()
                # Button to delete device
                if buttonContainer.button("remove device", key=f"delete_{button_key}"):
                    message = delete_device(device["_id"])
                    st.success(message)
                    st.rerun()
        # Add new device card
        add_col_index = (i + 1) % num_columns  
        add_container = columns[add_col_index].container()
        st.markdown("<div id='add_device'>", unsafe_allow_html=True)
        add_container.title("add new device")
        if add_container.button("add"):
            st.switch_page("pages/NewDevice.py")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        single_device.deviceDashboard(st.session_state["device_num"])





