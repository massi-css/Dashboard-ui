import streamlit as st
from widgets import *
import time
import pandas as pd
from utils.utils import *



# Dasboard of each device
def deviceDashboard(deviceId):
    #CSS
    with open("single_device.css") as f:
        st.markdown(
            f"""
            <style>
                {f.read()}
            </style>
            """,
            unsafe_allow_html=True
        )
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
        if st.button("reset device"):
            reset_device_data(deviceId)
            # copy_to_clipboard(deviceId)
            # st.session_state["copy"] = True
    with headcol3:
        if st.session_state['copy']:
            st.success("id copied to clipboard !")
            time.sleep(1)
            st.session_state['copy'] = False
            st.rerun()
            
    st.markdown("<span style='height: 10px;'></span>", unsafe_allow_html=True)

    st.title(title)
    main_section = st.container()
    with main_section:
        # parameters indicators
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.subheader("water quality index: ")
        st.markdown("<hr/>", unsafe_allow_html=True)
        qualitycol1,qualitycol2 = st.columns(2)
        with qualitycol1 :
            chartwaterqualityPlaceholder = st.empty()
        with qualitycol2 :
            waterqualityPlaceholder = st.empty()
            mesagecol1,mesagecol2,messagecol3 = st.columns([1,2,1])
            with mesagecol2:
                messageQuality = st.empty()
        # parameters indicators
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.subheader("water parameters:")
        st.markdown("<hr/>", unsafe_allow_html=True)
        col1,col3,col4= st.columns(3)
        placeholder9 = col1.empty()
        placeholder3 = col3.empty()
        placeholder5 = col4.empty()
        # data analytics
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.subheader("Data analytics:")
        st.markdown("<hr/>", unsafe_allow_html=True)
        col1,col2= st.columns([2,1])
        with col1:
            st.markdown("#### collected data :")
            placeholder11 = col1.empty()
        with col2:
            st.markdown("#### the expect for next day :")
            st.markdown("<span style='height: 10px;'></span>", unsafe_allow_html=True)
            forcastph = st.empty()
            forcastturbidity = st.empty()
            forcasttemperature = st.empty()
        # parameters graphs
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.subheader("more details:")
        st.markdown("<hr/>", unsafe_allow_html=True)
        placeholder10 = st.empty()

        datatoforcast = get_latest_device_data(deviceId)
        datatoforcast = datatoforcast[0]
        datatoforcastformated  ={
            "pH": datatoforcast['ph'],
            "temperature": datatoforcast['temperature'],
            "turbidity": datatoforcast['turbidity'],
        }
        # forcast_next_day(deviceId=deviceId, data=datatoforcastformated)

    while True:
        latest_data = get_latest_device_data(deviceId)
        df = pd.DataFrame(latest_data)
        forcasteddata = get_last_forcasted_data(deviceId)
        if forcasteddata:
            forcasteddata = forcasteddata[0] 


        # dataframe and forcasted metrics
        with placeholder11:
            st.dataframe(df, height=360)
        with forcastturbidity:
            diff = forcasteddata['next_day_turb'] - df['turbidity'].iloc[0]
            diff = format(diff, '.2f')
            st.metric(label="Turbidity", value=f"{format(forcasteddata['next_day_turb'],'.2f')} NTU", delta=f"{diff} NTU")
        with forcastph:
            diff = forcasteddata['next_day_pH'] - df['ph'].iloc[0]
            diff = format(diff, '.2f')
            st.metric(label="pH", value=f"{format(forcasteddata['next_day_pH'],'.2f')} pH", delta=f"{diff} pH")
        with forcasttemperature:
            diff = forcasteddata['next_day_temp'] - df['temperature'].iloc[0]  
            diff = format(diff, '.2f') 
            st.metric(label="Temperature", value=f"{format(forcasteddata['next_day_temp'],'.2f')} °C", delta=f"{diff} °C")
        # water quality index
        with waterqualityPlaceholder:
            plot_gauge(df['qualityIndex'].iloc[0],"#00CC96", "WQI","Water Quality Index", 100)
        with chartwaterqualityPlaceholder:
            bar_chart_with_threshold(df[["qualityIndex","createdAt"]],'createdAt','qualityIndex',40,"be careful !")
        with messageQuality:
            message = water_quality_message(df['qualityIndex'].iloc[0])
            st.write(message)
        # parameters indicators
        with placeholder3:
            plot_gauge(df['temperature'].iloc[0],"blue", "°C","Temperature", 45)
        with placeholder5:
            plot_gauge(df['turbidity'].iloc[0],"red", "NTU","Turbidity", 50)
        with placeholder9:
            plot_gauge(df['ph'].iloc[0],"purple", "pH","pH", 14)
        # parameters graphs
        with placeholder10:
            line_chart(df,'createdAt',["ph","temperature","turbidity"],'Parameters')

        time.sleep(10)

        