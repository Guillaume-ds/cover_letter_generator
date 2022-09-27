import streamlit as st
import pdfkit

# ---------- General functions ------------
try:    
    selectedData = st.session_state.internshipData
except:
    selectedData = {
        "Company" : None,
        "Position" : None,
        "Skills" : None,
        "Description":None
    }

html = open(".\static\FinanceCoverLetterBasis.html").read().format(
                                                    position=selectedData['Position'],
                                                    companyName=selectedData['Company'],
                                                    skillsRequired=selectedData['Skills'],
                                                    description=selectedData['Description'] )

# -------------- Front -------------
st.markdown(f"""<h2 style='text-align: center; font-weight:bold; margin-bottom:10px; margin-top:0px'>
                    Internship Cover Letter </h2>""",unsafe_allow_html=True)
st.markdown(f"""<h3 style='text-align: center; font-weight:bold; margin-bottom:150px; margin-top:0px'>
                    As {selectedData['Position']} at {selectedData['Company']} </h3>""",unsafe_allow_html=True)

st.markdown(html, unsafe_allow_html=True)

st.markdown(f"""<h3 style='text-align: center; font-weight:bold; margin-bottom:50px; margin-top:0px'> </h3>""",unsafe_allow_html=True)

save = st.button('Sauvegarder la lettre')
if save:
    positionName = '_'.join(selectedData['Position'].split()[1:])
    pdfkit.from_string(html,"coverLetters/"+selectedData['Company']+"_"+positionName+".pdf")
