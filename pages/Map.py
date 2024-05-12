import streamlit as st
from utils.utils import *
from widgets import *
import streamlit.components.v1 as components
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
    gdf = pd.DataFrame(devices)
    st.title("Map")
    st.markdown("<span style='height: 20px;'></span>", unsafe_allow_html=True)
    container = st.container()
    with container:
        if gdf.shape[0] > 0:
            m = init_map(gdf=gdf)
            m = add_points_to_map(m, gdf)
            # Convert the map to an HTML string
            m_html = m._repr_html_()
            # Display the map
            components.html(m_html, height=550)
        else:
            st.write("No devices found")
        
