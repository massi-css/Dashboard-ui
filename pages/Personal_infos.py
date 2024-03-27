import streamlit as st

def showPage():
    st.title("Edit password and username")
    st.markdown("<hr/>", unsafe_allow_html=True)
    with st.form(key='my_form'):
        username = st.text_input('Username')
        oldPassword = st.text_input("Old password")
        password = st.text_input('New Password', type='password')
        submit_button = st.form_submit_button('Submit')
        if submit_button:
            st.write("clicked")