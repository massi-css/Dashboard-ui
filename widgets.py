import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


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

def plot_circle(names, values):

    fig = px.pie(values=values, names=names,template="plotly_dark")
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    st.plotly_chart(fig, use_container_width=True)

