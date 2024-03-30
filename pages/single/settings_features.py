import streamlit as st
import pages.single.Personal_infos as Personal_infos
import pages.single.DataUpadtes as DataUpadtes
import pages.single.Help as Help
import pages.single.Feedback_Reporting as Feedback_Reporting

def Feature_Page(feature):   
    if feature == 'password_username':
        Personal_infos.showPage()
    elif feature == "data_upadtes":
        DataUpadtes.showPage()
    elif feature == "help":
        Help.showPage()
    elif feature == "feedback_reporting":
        Feedback_Reporting.showPage()
        
    