import streamlit as st
from utils.utils import *
from widgets import *
import streamlit.components.v1 as components
import pandas as pd
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
    devices = [
            {'Name': 'Device 1', 'Location': 'blida', 'Status': 'Active','Longitude': 36.531513, 'Latitude': 2.967012},
            {'Name': 'Device 2', 'Location': 'alger', 'Status': 'Inactive','Longitude': 36.752887, 'Latitude': 3.042048},
            {'Name': 'Device 3', 'Location': 'oran', 'Status': 'Active','Longitude': 35.691111, 'Latitude': -0.641667},
            {'Name': 'Device 4', 'Location': 'constantine', 'Status': 'Active','Longitude': 36.365, 'Latitude': 6.614722},
            {'Name': 'Device 5', 'Location': 'annaba', 'Status': 'Inactive','Longitude': 36.9, 'Latitude': 7.767}
        ]
    gdf = pd.DataFrame(devices)
    st.title("Map Page")
    st.markdown("<span style='height: 20px;'></span>", unsafe_allow_html=True)
    container = st.container()
    with container:
        m = init_map(gdf=gdf)
        m = add_points_to_map(m, gdf)
        # Convert the map to an HTML string
        m_html = m._repr_html_()
        # Display the map
        components.html(m_html, height=550)
        
