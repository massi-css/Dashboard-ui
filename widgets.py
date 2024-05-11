import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
from utils.utils import *
import altair as alt

# the sidebar
def sidebar():
    sidebar = st.sidebar
    with sidebar :
        st.title("IOT Dashboard")
        st.markdown("<span style='height: 20px;'></span>", unsafe_allow_html=True)
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.page_link("Home.py", label="Home", icon="🏠")
        st.page_link("pages/Devices.py", label="Devices", icon="📱")
        st.page_link("pages/AiChat.py", label="AI Chat", icon="💬")
        st.page_link("pages/Notifications.py", label="Notifications", icon="📧")
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
    padding = 0.001
    if gdf is not None:
        # trying to fit the map to the center of all markers
        mean_lat = gdf['latitude'].mean()
        mean_lon = gdf['longitude'].mean()
        location = [mean_lat, mean_lon]
        m = folium.Map(location=location, zoom_start=zoom, tiles=map_type)
        # trying to fit the zoom to all markers in the map
        sw = gdf[['latitude', 'longitude']].min().values.tolist()
        ne = gdf[['latitude', 'longitude']].max().values.tolist()
        sw[0] -= padding
        sw[1] -= padding
        ne[0] += padding
        ne[1] += padding
        m.fit_bounds([sw, ne])
        return m
    return folium.Map(location=location, zoom_start=zoom, tiles=map_type)

# function to plot a map with markers
def add_points_to_map(m, gdf):
    for i, row in gdf.iterrows():
        folium.Marker(location=[row['latitude'], row['longitude']], popup=row['deviceName']).add_to(m)
    return m

def line_chart(df, x, y_columns, title):
    # Reshape the DataFrame from wide format to long format
    df_long = df.melt(id_vars=x, value_vars=y_columns, var_name='column', value_name='value')

    chart = alt.Chart(df_long).mark_line().encode(
        alt.X(x),
        alt.Y('value:Q'),
        color='column:N'  # Use the 'column' column for the color encoding
    ).properties(
        title=title,
        # width=500
        height=500
    )

    st.altair_chart(chart, use_container_width=True)

def scatter_chart(df, x, y, title):
    chart = alt.Chart(df).mark_point().encode(
    x=x,
    y=y,
    color='Origin:N',
    tooltip=['Name:N']
).properties(
    title=title,
    width=500
)

    st.altair_chart(chart)

def area_chart(df, x, y, title, threshold=None):
    chart = alt.Chart(df).mark_area(
        line={'color':'darkgreen'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='white', offset=0),
                alt.GradientStop(color='darkgreen', offset=1)],
            x1=1,
            x2=1,
            y1=1,
            y2=0
        )
    ).encode(
        alt.X(x),
        alt.Y(y)
    ).properties(
        title=title,
        width=500
    )

    if threshold is not None:
        rule = alt.Chart(df).mark_rule(color='red').encode(
            y=alt.value(threshold)
        )
        chart = alt.layer(chart, rule).resolve_scale(y='shared')
        chart = chart + rule

    st.altair_chart(chart)

def bar_chart_with_threshold(source,x,y,threshold=None,label="danger"):
    

    bars = alt.Chart(source).mark_bar(color="#e45755").encode(
        x=f"{x}:O",
        y=f"{y}:Q",
    ).properties(
        width=500
    )

    if threshold is not None:
        highlight = bars.mark_bar(color="#00CC96").encode(
        y2=alt.Y2(datum=threshold)
        ).transform_filter(
        alt.datum[y] > threshold
        )

        rule = alt.Chart().mark_rule(color="#e45755").encode(
            y=alt.Y(datum=threshold)
        )

        label = rule.mark_text(
            x="width",
            dx=-2,
            align="right",
            baseline="bottom",
            text=label,
            color="#FFFFFF"
        )

        st.altair_chart(bars + highlight + rule + label)
    else:
        st.altair_chart(bars)

def horizontal_bars_chart(df, x, y):
    chart = alt.Chart(df).mark_bar().encode(
        alt.X(y),
        alt.Y(x)
    ).properties(
        height=320,
        width=500
    )
    st.altair_chart(chart)