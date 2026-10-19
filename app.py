
import streamlit as st

st.set_page_config(
    page_title="MedTrack Hospital Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

home = st.Page(
    "home.py",
    title="App",
    icon="🏥",
    default=True
)

department = st.Page(
    "pages/Department_Analytics.py",
    title="Department Analytics",
    icon="📊"
)

overview = st.Page(
    "pages/Hospital_Overview.py",
    title="Hospital Overview",
    icon="🏥"
)

patient_flow = st.Page(
    "pages/Patient_Flow.py",
    title="Patient Flow",
    icon="🔄"
)

resources = st.Page(
    "pages/Resource_Utilization.py",
    title="Resource Utilization",
    icon="📈"
)

navigation = st.navigation(
    [home, department, overview, patient_flow, resources],
    position="top",
    expanded=True
)

navigation.run()
