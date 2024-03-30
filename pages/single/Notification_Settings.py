from time import sleep
import streamlit as st
from utils.utils import *

def showPage():
    st.subheader("Notification Settings")
    st.markdown("<hr/>", unsafe_allow_html=True)
    user = get_user_by_Id()
    if user['phoneNumber'] == None:
        phoneNumberfield = ""
    else:
        phoneNumberfield = user['phoneNumber']
    st.info("if you turn off the notifications you will no longer receive any alerts from the system")
    with st.form(key='my_form'):
        perEmail = st.toggle("recieve notification via email",value=user['recieveNotification']['perEmail'])
        perSMS = st.toggle("recieve notification via sms",value=user['recieveNotification']['perSMS'])
        email = st.text_input('email',value=user['email'])
        phoneNumber = st.text_input("phone number",value=phoneNumberfield)
        submit_button = st.form_submit_button('submit')
        if submit_button:
            data ={
                "email": email,
                "phoneNumber": phoneNumber,
                "recieveNotification": {
                    "perEmail": perEmail,
                    "perSMS": perSMS
                }
            }
            if email == "" or phoneNumber == "":
                st.error("Please fill all the fields")
            else:
                response = update_notification(data)
                if response['status'] == True:
                    st.success(response['message'])
                    sleep(2)
                    st.rerun()
                else:
                    st.error(response['message'])