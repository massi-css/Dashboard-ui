import streamlit as st

def showPage():
    st.title("Feedback & Reporting")
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    with st.form(key='my_form'):
        col1, col2 = st.columns(2)
        with col1:
            st.text_area("Write your feedback here")

        with col2:
            st.text_area("Write your report here")
            
        submit_button = st.form_submit_button('Submit')
        if submit_button:
            st.write("clicked")
        
    