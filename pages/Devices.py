import streamlit as st
import pages.single.single_device as single_device 
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
        st.markdown("<span style='height: 20px;'></span>", unsafe_allow_html=True)
        # Columns
        num_columns = 3
        columns = st.columns(num_columns)
        # Data
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
                
                # Button to show dashboard
                #giving it a speacial key to identify it
                button_key = device["_id"]
                with container:
                    col1,col2 = st.columns([1,1])
                with col1:
                    # add new device card
                    if st.button("See Dashboard", key=button_key):
                        st.session_state["device_num"] = device["_id"]
                        st.rerun()
                with col2:
                    # Button to delete device
                    if st.button("Remove Device", key=f"delete_{button_key}"):
                        message = delete_device(device["_id"])
                        st.success(message)
                        st.rerun()
        # Add new device card
        add_col_index = (i + 1) % num_columns  
        add_container = columns[add_col_index].container()
        st.markdown("<div id='add_device'>", unsafe_allow_html=True)
        add_container.title("Add New Device")
        if add_container.button("Add"):
            st.switch_page("pages/NewDevice.py")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        single_device.deviceDashboard(st.session_state["device_num"])





