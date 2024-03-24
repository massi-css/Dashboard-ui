import streamlit as st
from utils.utils import *
import pandas as pd
import numpy as np
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
    num_rows = 30
    df = pd.DataFrame({
                'temperature': 'test',  # temperatures between -20 and 50
                'conductivity': 'test',  # conductivity values between 0 and 100
                'turbidity': 'test',  # turbidity values between 0 and 100
                'oxygen': 'test',  # oxygen values between 0 and 100
                'time': 'test',  # hourly data
                'location': 'location1'
            }, index=np.arange(num_rows))
    data =[
        {
            "device_id": "device1",
            "device_data": df
        },
        {
            "device_id": "device2",
            "device_data": df
        },
        {
            "device_id": "device3",
            "device_data": df,
        },
        {
            "device_id": "device4",
            "device_data": df
        },
        {
            "device_id": "device5",
            "device_data": df
        },
        {
            "device_id": "device6",
            "device_data": df
        },
        {
            "device_id": "device7",
            "device_data": df
        },
        {
            "device_id": "device8",
            "device_data": df
        }
    ]
    st.title("Historical Data")
    st.markdown("<span style='height: 20px;'></span>", unsafe_allow_html=True)
    for device in data:
        with st.expander(f"Device: {device['device_id']}"):
            st.dataframe(device['device_data'], width=1000, height=300)
        
