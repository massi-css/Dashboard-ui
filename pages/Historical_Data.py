import streamlit as st
from utils.utils import *
import pandas as pd
from widgets import sidebar

# configure the page
st.set_page_config(page_title="IOT Dashboard", layout="wide",initial_sidebar_state='expanded')

#initialize the authentication status
if 'authenticated' not in os.environ:
    os.environ['authenticated'] = 'False'

if os.environ['authenticated'] == 'False':
    st.switch_page("pages/login_page.py")
elif os.environ['authenticated'] == 'True':
    # the sidebar
    sidebar()
    devices = get_devices()

    st.title("Historical Data")
    st.markdown("<span style='height: 20px;'></span>", unsafe_allow_html=True)
    if(len(devices) == 0):
        st.write("No devices found")
        st.stop()
    for device in devices:
        with st.expander(f"Device: {device['deviceName']}"):
            deviceData = get_device_data(device['_id'])
            if len(deviceData) == 0:
                st.write("No data available")
                continue
            df= pd.DataFrame(deviceData)
            st.dataframe(df, width=1000, height=300)
        
