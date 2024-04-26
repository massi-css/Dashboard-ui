import streamlit as st
import plotly.express as px
from widgets import *
from datetime import datetime
import time
import pandas as pd
from utils.utils import *



# Dasboard of each device
def deviceDashboard(deviceId):
    device = get_device_by_id(deviceId)
    if 'copy' not in st.session_state:
        st.session_state['copy'] = False
    title = f"{device['deviceName']} dashboard"
    deviceId  = device['_id']
    headcol1,headcol2,headcol3,headcol4 = st.columns([1,1,1,1])
    with headcol1: 
        if st.button("back"):
            st.session_state["device_num"] = -1
            st.rerun()
    with headcol4:
        if st.button("copy ID to clipboard"):
            copy_to_clipboard(deviceId)
            st.session_state["copy"] = True
    with headcol3:
        if st.session_state['copy']:
            st.success("id copied to clipboard !")
            time.sleep(1)
            st.session_state['copy'] = False
            st.rerun()
            
    st.markdown("<span style='height: 10px;'></span>", unsafe_allow_html=True)

    st.title(title)
    st.markdown("<hr/>", unsafe_allow_html=True)
    main_section = st.container()
    with main_section:
        # parameters indicators
        col1,col2= st.columns([2,1])
        with col1:
            st.subheader("collected data:")
            placeholder11 = col1.empty()
        with col2:
            st.subheader("status of water:")
            placeholder8 = col2.empty()
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.subheader("water quality index: ")
        waterqualityPlaceholder = st.empty()
        st.markdown("<hr/>", unsafe_allow_html=True)
        # parameters indicators
        st.subheader("water parameters:")
        st.markdown("<hr/>", unsafe_allow_html=True)
        col1,col2,col3,col4= st.columns(4)
        placeholder9 = col1.empty()
        placeholder4 = col2.empty()
        placeholder3 = col3.empty()
        placeholder5 = col4.empty()
        # parameters graphs
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.subheader("more details:")
        st.markdown("<hr/>", unsafe_allow_html=True)
        col1,col2= st.columns(2)
        placeholder10 = col1.empty()
        placeholder1 = col2.empty()
        placeholder6 = col1.empty()
        placeholder2 = col2.empty()

    while True:
        latest_data = get_latest_device_data(deviceId)
        df = pd.DataFrame(latest_data)
        # dataframe and circle plot
        with placeholder11:
            st.dataframe(df, height=360)
        with placeholder8:
            plot_circle(["ph","temperature","conductivity","turbidity"],[df['ph'].iloc[0],df['temperature'].iloc[0],df['conductivity'].iloc[0],df['turbidity'].iloc[0]])
        # water quality index
        with waterqualityPlaceholder:
            water_quality_index = calculate_wqi(df['ph'].iloc[0],df['turbidity'].iloc[0],df['conductivity'].iloc[0],df['temperature'].iloc[0])
            plot_gauge(water_quality_index,"white", "WQI","Water Quality Index", 100)
        # parameters indicators
        with placeholder3:
            plot_gauge(df['temperature'].iloc[0],"blue", "°C","Temperature", 45)
        with placeholder4:
            plot_gauge(df['conductivity'].iloc[0],"green", "µS/cm","Conductivity", 100)
        with placeholder5:
            plot_gauge(df['turbidity'].iloc[0],"red", "NTU","Turbidity", 5)
        with placeholder9:
            plot_gauge(df['ph'].iloc[0],"purple", "pH","pH", 14)
        # parameters graphs
        with placeholder10:
            # st.line_chart(df[['temperature','createdAt']].set_index('createdAt'),color="#0000FF")
            line_chart(df,'createdAt',["ph","temperature","turbidity"],'Parameters')
        with placeholder2:
            # st.line_chart(df[['conductivity','createdAt']].set_index('createdAt'),color="#008000")
            scatter_chart(df,'temperature','ph','ph')
        with placeholder6:
            # st.line_chart(df[['turbidity','createdAt']].set_index('createdAt'),color="#808080")
            area_chart(df,'createdAt','temperature','Temperature')
        with placeholder1:
            st.line_chart(df[['ph','createdAt']].set_index('createdAt'),color="#800080")
        time.sleep(10)
        