import streamlit as st
import plotly.express as px
from widgets import *
from datetime import datetime
import time
import random
import pandas as pd
from utils.utils import *



# Dasboard of each device
def deviceDashboard(deviceId):
    device = get_device_by_id(deviceId)
    # df = pd.DataFrame(columns=['createdAt','ph', 'temperature','conductivity','oxigen','turbidity'])
    title = f"{device['deviceName']} dashboard"
    if st.button("back"):
        st.session_state["device_num"] = -1
        st.rerun()
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
        col1,col2,col3= st.columns(3)
        placeholder10 = col1.empty()
        placeholder1 = col2.empty()
        placeholder6 = col3.empty()
        placeholder2 = col1.empty()
        placeholder7 = col2.empty()

    while True:
        latest_data = get_latest_device_data(deviceId)
        # temperature_in_c = latest_data['temperature'][0]['temperature']
        # conductivity = latest_data['conductivity']
        # oxigen = latest_data['oxygen']
        # turbidity = latest_data['turbidity']
        # ph = latest_data['ph']
        # dateString= latest_data['createdAt']
        # date_string = dateString.replace('Z', '')
        # date_object = datetime.fromisoformat(date_string)
        # date = date_object.strftime("%H:%M:%S")
        # df = pd.concat([df, pd.DataFrame([[date,ph, temperature_in_c,conductivity,oxigen,turbidity]],columns=['createdAt','ph', 'temperature','conductivity','oxigen','turbidity'])], ignore_index=True)
        df = pd.DataFrame(latest_data)
        print(df)
        with placeholder1:
            st.line_chart(df[['temperature','createdAt']].set_index('createdAt'),color="#0000FF")
        with placeholder2:
            st.line_chart(df[['conductivity','createdAt']].set_index('createdAt'),color="#008000")
        with placeholder3:
            plot_gauge(df['temperature'].iloc[0],"blue", "°C","Temperature", 45)
        with placeholder4:
            plot_gauge(df['conductivity'].iloc[0],"green", "µS/cm","Conductivity", 100)
        with placeholder5:
            plot_gauge(df['oxygen'].iloc[0],"red", "mg/L","Oxigen", 100)
        with placeholder6:
            st.line_chart(df[['oxygen','createdAt']].set_index('createdAt'),color="#FF0000")
        with placeholder7:
            st.line_chart(df[['turbidity','createdAt']].set_index('createdAt'),color="#808080")
        # with placeholder8:
        #     plot_gauge(turbidity,"white", "NTU","Turbidity", 100)
        with placeholder9:
            plot_gauge(df['ph'].iloc[0],"purple", "pH","pH", 14)
        with placeholder10:
            st.line_chart(df[['ph','createdAt']].set_index('createdAt'),color="#800080")
        with placeholder11:
            st.dataframe(df, height=360)
        with placeholder8:
            plot_circle(["ph","temperature","conductivity","oxigen","turbidity"],[df['ph'].iloc[0],df['temperature'].iloc[0],df['conductivity'].iloc[0],df['oxygen'].iloc[0],df['turbidity'].iloc[0]])
        time.sleep(10)
        