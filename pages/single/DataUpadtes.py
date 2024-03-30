import streamlit as st

def showPage():
    st.title("Data updates frequency ")
    st.markdown("<hr/>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input("Data updates",step=1,format="%d")

    with col2:
        st.selectbox("per",["Minutes","Hours","Weeks"])