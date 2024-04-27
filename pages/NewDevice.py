import streamlit as st
from utils.utils import *
from widgets import sidebar

# configure the page
st.set_page_config(page_title="IOT Dashboard", layout="centered",initial_sidebar_state='expanded')

#initialize the authentication status
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = get_authentication_status()

if st.session_state.authenticated == False:
    st.switch_page("pages/login_page.py")
elif st.session_state.authenticated == True:
    # the sidebar
    sidebar()
    latitude, longitude = generate_random_lat_long(max_lat=36.605496,min_lat=36.464257,max_long=3.022199,min_long=2.767970)
    # back button 
    if st.button("Back"):
        st.switch_page("pages/Devices.py")
    with st.form(key='ad_device_form'):
        st.title("Add a new device")
        device_name = st.text_input("Device name")
        location = st.text_input("Location")
        status = st.selectbox("Status", ["Active", "Inactive"])
        # latitude = st.number_input("Latitude", value=latitude, format="%.8f")
        # longitude = st.number_input("Longitude", value=longitude, format="%.8f")
        submit = st.form_submit_button("Add device")
        if submit:
            data={
                'deviceName': device_name,
                'location': location,
                'status': status,
                'longitude': longitude,
                'latitude': latitude
            }
            device = create_device(data)
            if device:
                st.success("Device added successfully")
                st.switch_page("pages/Devices.py")
            else:
                st.error("Error adding the device")
            st.session_state["device_num"] = -1
            # st.rerun()