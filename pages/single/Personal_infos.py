from time import sleep
import streamlit as st
from utils.utils import *

def showPage():
    st.subheader("Edit password and username")
    user = get_user_by_Id()
    st.info("duplicate the old password if you don't want to change it")
    with st.form(key='my_form'):
        username = st.text_input('Username',value=user['username'])
        oldPassword = st.text_input("Old password")
        password = st.text_input('New Password', type='password')
        submit_button = st.form_submit_button('update')
        if submit_button:
            data ={
                "username": username,
                "oldPassword": oldPassword,
                "password": password
            }
            if username == "" or oldPassword == "" or password == "":
                st.error("Please fill all the fields")
            else:
                response = update_user(data)
                if response['status'] == True:
                    st.success(response['message'])
                    sleep(2)
                    st.rerun()
                else:
                    st.error(response['message'])