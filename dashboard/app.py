
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="MedTrack - Hospital Analytics",
    page_icon="🏥",
    layout="wide"
)

# Dashboard title
st.title("🏥 MedTrack")
st.subheader("Hospital Operations & Patient Analytics Dashboard")

st.markdown("---")

# Sidebar
st.sidebar.title("MedTrack Navigation")
page = st.sidebar.radio(
    "Select Dashboard",
    [
        "Hospital Overview",
        "Patient Flow",
        "Department Analytics",
        "Resource Utilization"
    ]
)

# Load datasets
healthcare = pd.read_csv("cleaned_data/healthcare_cleaned.csv")
hdhi = pd.read_csv("cleaned_data/hdhi_cleaned.csv")

# Hospital Overview
if page == "Hospital Overview":

    st.header("Hospital Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Admissions", f"{len(healthcare):,}")
    col2.metric(
        "Average Stay",
        f"{healthcare['Length of Stay'].mean():.2f} days"
    )
    col3.metric(
        "Medical Conditions",
        healthcare["Medical Condition"].nunique()
    )
    col4.metric(
        "Unique Hospital Names",
        healthcare["Hospital"].nunique()
    )

    st.markdown("---")

    st.subheader("Admissions by Medical Condition")

    condition_data = healthcare["Medical Condition"].value_counts().reset_index()
    condition_data.columns = ["Medical Condition", "Admissions"]

    fig = px.bar(
        condition_data,
        x="Medical Condition",
        y="Admissions",
        color="Medical Condition",
        title="Admissions by Medical Condition"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Admission Type Distribution")

    admission_data = healthcare["Admission Type"].value_counts().reset_index()
    admission_data.columns = ["Admission Type", "Admissions"]

    fig2 = px.pie(
        admission_data,
        names="Admission Type",
        values="Admissions",
        title="Admission Types"
    )

    st.plotly_chart(fig2, use_container_width=True)

# Other dashboard pages - to be developed next

elif page == "Patient Flow":

    st.header("Patient Flow Analysis")
    st.write("Analysis of patient admissions, stay duration and outcomes.")

    # Prepare numerical columns
    hdhi["DURATION OF STAY"] = pd.to_numeric(
        hdhi["DURATION OF STAY"], errors="coerce"
    )
    hdhi["duration of intensive unit stay"] = pd.to_numeric(
        hdhi["duration of intensive unit stay"], errors="coerce"
    )

    # KPI calculations
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Admissions", f"{len(hdhi):,}")

    avg_stay = hdhi["DURATION OF STAY"].mean()
    col2.metric(
        "Average Stay",
        f"{avg_stay:.2f} days" if pd.notna(avg_stay) else "N/A"
    )

    avg_icu = hdhi["duration of intensive unit stay"].mean()
    col3.metric(
        "Average ICU Stay",
        f"{avg_icu:.2f} days" if pd.notna(avg_icu) else "N/A"
    )

    st.markdown("---")

    # Monthly admission trends
    st.subheader("Monthly Admission Trends")

    healthcare["Date of Admission"] = pd.to_datetime(
        healthcare["Date of Admission"], errors="coerce"
    )

    monthly = (
        healthcare.dropna(subset=["Date of Admission"])
        .groupby(
            healthcare.dropna(subset=["Date of Admission"])
            ["Date of Admission"].dt.to_period("M")
        )
        .size()
        .reset_index(name="Admissions")
    )

    monthly["Month"] = monthly["Date of Admission"].astype(str)

    fig = px.line(
        monthly,
        x="Month",
        y="Admissions",
        markers=True,
        title="Monthly Patient Admissions"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Patient outcomes
    st.subheader("Patient Outcome Analysis")

    outcome_data = (
        hdhi["OUTCOME"]
        .fillna("Not Recorded")
        .value_counts()
        .reset_index()
    )

    outcome_data.columns = ["Outcome", "Patients"]

    fig2 = px.bar(
        outcome_data,
        x="Outcome",
        y="Patients",
        color="Outcome",
        title="Patient Outcomes"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Admission type
    st.subheader("Emergency vs OPD Admissions")

    admission_data = (
        hdhi["TYPE OF ADMISSION-EMERGENCY/OPD"]
        .fillna("Not Recorded")
        .value_counts()
        .reset_index()
    )

    admission_data.columns = ["Admission Type", "Patients"]

    fig3 = px.pie(
        admission_data,
        names="Admission Type",
        values="Patients",
        title="Admission Type Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)



elif page == "Department Analytics":

    st.header("Department & Clinical Analytics")

    st.write(
        "Analysis of medical conditions, doctor workload "
        "and average patient stay."
    )

    # KPI cards
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Medical Conditions",
        healthcare["Medical Condition"].nunique()
    )

    col2.metric(
        "Unique Doctors",
        healthcare["Doctor"].nunique()
    )

    col3.metric(
        "Total Admissions",
        f"{len(healthcare):,}"
    )

    st.markdown("---")

    # Admissions by medical condition
    st.subheader("Admissions by Medical Condition")

    condition_data = (
        healthcare.groupby("Medical Condition")
        .size()
        .reset_index(name="Admissions")
        .sort_values("Admissions", ascending=False)
    )

    fig1 = px.bar(
        condition_data,
        x="Medical Condition",
        y="Admissions",
        color="Medical Condition",
        title="Clinical Workload by Medical Condition"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # Doctor workload
    st.subheader("Top 10 Doctors by Patient Admissions")

    doctor_data = (
        healthcare.groupby("Doctor")
        .size()
        .reset_index(name="Admissions")
        .sort_values("Admissions", ascending=False)
        .head(10)
    )

    fig2 = px.bar(
        doctor_data,
        x="Doctor",
        y="Admissions",
        title="Top 10 Doctors by Admissions"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # Average stay by medical condition
    st.subheader("Average Length of Stay by Medical Condition")

    stay_data = (
        healthcare.groupby("Medical Condition")["Length of Stay"]
        .mean()
        .reset_index()
    )

    stay_data.columns = ["Medical Condition", "Average Stay"]

    fig3 = px.bar(
        stay_data,
        x="Medical Condition",
        y="Average Stay",
        color="Medical Condition",
        title="Average Patient Stay by Medical Condition"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.info(
        "Note: Department-wise performance cannot be calculated "
        "because the dataset does not contain a Department column. "
        "Clinical condition and doctor-wise analysis are shown instead."
    )



elif page == "Resource Utilization":

    st.header("Resource Utilization Analysis")

    st.write(
        "Analysis of recorded room assignments, "
        "hospital stay and intensive care usage."
    )

    # Convert ICU stay into numeric format
    hdhi["duration of intensive unit stay"] = pd.to_numeric(
        hdhi["duration of intensive unit stay"],
        errors="coerce"
    )

    icu_data = hdhi[
        hdhi["duration of intensive unit stay"] > 0
    ]

    # KPI calculations
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Admissions",
        f"{len(hdhi):,}"
    )

    col2.metric(
        "Records With ICU Stay",
        f"{len(icu_data):,}"
    )

    avg_icu = icu_data["duration of intensive unit stay"].mean()

    col3.metric(
        "Average ICU Stay",
        f"{avg_icu:.2f} days" if pd.notna(avg_icu) else "N/A"
    )

    col4.metric(
        "Recorded Room Numbers",
        healthcare["Room Number"].nunique()
    )

    st.markdown("---")

    # Room assignment frequency
    st.subheader("Room Assignment Frequency")

    room_data = (
        healthcare["Room Number"]
        .fillna("Not Recorded")
        .astype(str)
        .value_counts()
        .head(10)
        .reset_index()
    )

    room_data.columns = ["Room Number", "Admission Records"]

    fig1 = px.bar(
        room_data,
        x="Room Number",
        y="Admission Records",
        title="Top 10 Most Frequently Recorded Room Numbers"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # ICU stay distribution
    st.subheader("ICU Stay Distribution")

    fig2 = px.histogram(
        icu_data,
        x="duration of intensive unit stay",
        nbins=20,
        title="Distribution of Recorded ICU Stay Duration"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # Hospital stay distribution
    st.subheader("Hospital Stay Distribution")

    stay_data = pd.to_numeric(
        hdhi["DURATION OF STAY"],
        errors="coerce"
    ).dropna()

    fig3 = px.histogram(
        x=stay_data,
        nbins=20,
        title="Distribution of Hospital Stay Duration",
        labels={"x": "Duration of Stay (Days)", "y": "Admissions"}
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.info(
        "Note: Room assignment frequency is not bed occupancy. "
        "Actual bed utilization requires bed capacity and occupancy "
        "period data, which are not available in the supplied datasets."
    )

