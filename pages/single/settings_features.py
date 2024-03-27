import streamlit as st
import pages.Personal_infos as Personal_infos
import pages.DataUpadtes as DataUpadtes
import pages.Help as Help
import pages.Feedback_Reporting as Feedback_Reporting

def Feature_Page(feature):
    if st.button("back"):
        st.session_state["selected_Feature"] = "Settings"
        st.rerun()
        
        
    if feature == 'password_username':
        Personal_infos.showPage()
    elif feature == "data_upadtes":
        DataUpadtes.showPage()
    elif feature == "help":
        Help.showPage()
    elif feature == "feedback_reporting":
        Feedback_Reporting.showPage()
        
    