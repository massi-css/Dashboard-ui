import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
from utils.utils import *

# the sidebar
def sidebar():
    sidebar = st.sidebar
    with sidebar :
        st.title("IOT Dashboard")
        st.markdown("<span style='height: 20px;'></span>", unsafe_allow_html=True)
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.page_link("Home.py", label="Home", icon="🏠")
        st.page_link("pages/Devices.py", label="Devices", icon="📱")
        st.page_link("pages/Alerts.py", label="Alerts", icon="📧")
        st.page_link("pages/Historical_Data.py", label="Historical Data", icon="📊")
        st.page_link("pages/Map.py", label="Map", icon="🗺️")
        st.page_link("pages/Settings.py", label="Settings", icon="⚙️")
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.button('Logout', key='logout', on_click=logout)

# Function to plot a gauge chart for water parameters
def plot_gauge(
    indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 26,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 28}
            },
        )
    )
    fig.update_layout(
        height=190,
        margin=dict(l=10, r=10, t=70, b=20, pad=8),
    )
    st.plotly_chart(fig, use_container_width=True)

# Function to plot a percentsge of water parameters
def plot_circle(names, values):
    fig = px.pie(values=values, names=names,template="plotly_dark")
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    st.plotly_chart(fig, use_container_width=True)

# function to plot a map support auto zoom and center if there is markers
# @st.cache_resource
def init_map(location = (36.531513, 2.967012), zoom=15, map_type='OpenStreetMap', gdf=None):
    if gdf is not None:
        # trying to fit the map to the center of all markers
        mean_lat = gdf['Latitude'].mean()
        mean_lon = gdf['Longitude'].mean()
        location = [mean_lat, mean_lon]
        m = folium.Map(location=location, zoom_start=zoom, tiles=map_type)
        # trying to fit the zoom to all markers in the map
        sw = gdf[['Latitude', 'Longitude']].min().values.tolist()
        ne = gdf[['Latitude', 'Longitude']].max().values.tolist()
        m.fit_bounds([sw, ne])
        return m
    return folium.Map(location=location, zoom_start=zoom, tiles=map_type)

# function to plot a map with markers
def add_points_to_map(m, gdf):
    for i, row in gdf.iterrows():
        folium.Marker(location=[row['Latitude'], row['Longitude']], popup=row['Location']).add_to(m)
    return m