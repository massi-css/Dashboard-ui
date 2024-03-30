import streamlit as st
from time import sleep
from utils.utils import *

def showPage():
    st.subheader("Data updates frequency ")
    st.markdown("<hr/>", unsafe_allow_html=True)
    user = get_user_by_Id()
    st.info("Note the minimum update frequency is 10 seconds")
    with st.form(key='my_form'):
        updatefrequency = st.number_input("update frequency per sec",min_value=10,step=10,format="%d",value=user['updatefrequency'])
        submit_button = st.form_submit_button('submit')
        if submit_button:
            data ={
                "updatefrequency": updatefrequency
            }
            if updatefrequency == "":
                st.error("Please fill the field")
            else:
                response = update_notification(data)
                if response['status'] == True:
                    st.success(response['message'])
                    sleep(2)
                    st.rerun()
                else:
                    st.error(response['message'])