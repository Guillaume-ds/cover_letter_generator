import streamlit as st 
import pandas as pd 

from st_aggrid import GridOptionsBuilder, AgGrid

# ---------- General functions ------------
try:
    stages = pd.read_csv('./static/stages.csv')
except:
    stages = pd.DataFrame({'Company':["Great Company"],
                        'Position':["Quantitative Analyst"],
                        'Link':["https://www.youtube.com/watch?v=dQw4w9WgXcQ"],
                        'Description':["using python to develop applications, trading"],
                        'Applied':["not yet applied"],
                        'Skills':["Python, analytical mind"]})

def addValues(stages,Company,Position,Link,Description,Applied,skills):
    df2 = pd.DataFrame({'Company':[Company],
                        'Position':[Position],
                        'Link':[Link],
                        'Description':[Description],
                        'Applied':[Applied],
                        'Skills':[skills]})
    newValues = pd.concat([stages,df2],ignore_index=True)
    stages = newValues
    stages.to_csv('./static/stages.csv',index=False)
    st.experimental_rerun()
    
def deleteValues(stages,selectedDf):
    newValues = pd.concat([stages, selectedDf],ignore_index=True).drop_duplicates(keep=False)
    stages = newValues
    stages.to_csv('./static/stages.csv',index=False)
    st.experimental_rerun()

# -------------- Front --------------

st.markdown(f"""<h2 style='text-align: center; font-weight:bold; margin-bottom:50px; margin-top:0px'>
                    Internship Positions</h2>""",unsafe_allow_html=True)


    #---------- Grid Table ------------
gb = GridOptionsBuilder.from_dataframe(stages)
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children")
gridOptions = gb.build()

grid_response = AgGrid(
    stages,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=True,
    #theme='ALPINE', #Add theme color to the table
    enable_enterprise_modules=True, 
    #reload_data=True
)
data = grid_response['data']
selectedValues = grid_response['selected_rows'] 
selectedDf = pd.DataFrame(selectedValues) #Pass the selected rows to a new dataframe df that is displayed in delete


    #---------- Selected DF ------------
    
if len(selectedDf)>0:
    st.session_state.internshipData=selectedDf.iloc[-1]
    selectedInternship = selectedDf.iloc[-1]
    action = "Modify internship"
else:
    selectedInternship= stages.iloc[-1]
    st.session_state.internshipData=selectedInternship
    action = "Add an internship"

    #---------- Expenders ------------
    
with st.expander(action):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        Company = st.text_input("Company",selectedInternship['Company'])
        Position = st.text_input("Position",selectedInternship['Position'])

    with col2:
        Link = st.text_input("Link",selectedInternship['Link'])
        Skills = st.text_input("Skills",selectedInternship['Skills'])
        update = st.button('Ajouter un stage')

    with col3:
        Description = st.text_input("Description",selectedInternship['Description'])
        Applied = st.selectbox("Application",("Not yet Applied","Applied","In process", "Offer"))

    if update:
        if len(selectedDf)==0:
            addValues(stages,Company,Position,Link,Description,Applied,Skills)
        else:
            index=selectedValues[-1]["_selectedRowNodeInfo"]["nodeRowIndex"]
            stages.iloc[index]=[Company,Position,Link,Description,Applied,Skills]
            stages.to_csv('./static/stages.csv',index=False)
            st.experimental_rerun()
     
with st.expander("Delete internship"):
    if len(selectedDf)>0:
        selectedDf=selectedDf.drop('_selectedRowNodeInfo',axis=1)
        st.table(selectedDf)
        delete = st.button('Supprimer les formations')
        if delete:
            deleteValues(stages,selectedDf)


