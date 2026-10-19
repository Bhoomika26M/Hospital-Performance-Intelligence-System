
import streamlit as st
import pandas as pd
from pathlib import Path

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="Resource Utilization | MedTrack",
    page_icon="🏥",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================
# Load Dataset
# =====================================

@st.cache_data
def load_data():
    patients = pd.read_csv(BASE_DIR / "hospital_cleaned.csv")
    departments = pd.read_csv(
        BASE_DIR / "hospital_department_analytics.csv"
    )

    for df in [patients, departments]:
        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

    for col in ["length_of_stay", "billing_amount"]:
        if col in patients.columns:
            patients[col] = pd.to_numeric(
                patients[col], errors="coerce"
            )

    return patients, departments


try:
    patients, departments = load_data()
except FileNotFoundError as error:
    st.error(f"Required dataset not found: {error.filename}")
    st.stop()


# =====================================
# Department Preparation
# =====================================

if "department" not in patients.columns:
    mapping = {
        "Cancer": "Oncology",
        "Obesity": "General Medicine",
        "Diabetes": "Endocrinology",
        "Asthma": "Pulmonology",
        "Hypertension": "Cardiology",
        "Arthritis": "Rheumatology"
    }

    patients["department"] = (
        patients["medical_condition"]
        .astype("string")
        .str.strip()
        .str.title()
        .map(mapping)
        .fillna("Other")
    )


# =====================================
# Sidebar Filters
# =====================================

st.sidebar.title("🏥 MedTrack")
st.sidebar.caption("Resource Utilization")
st.sidebar.divider()

department_options = sorted(
    patients["department"].dropna().unique().tolist()
)

selected_departments = st.sidebar.multiselect(
    "Select Departments",
    department_options,
    default=department_options
)

filtered = patients[
    patients["department"].isin(selected_departments)
].copy()


# =====================================
# Header
# =====================================

st.title("🏥 Resource Utilization")
st.markdown(
    "Explore available indicators of hospital workload and resource demand."
)



st.divider()


# =====================================
# Available Indicators
# =====================================

total_admissions = len(filtered)

unique_doctors = (
    filtered["doctor"].nunique()
    if "doctor" in filtered.columns else None
)

average_stay = (
    filtered["length_of_stay"].mean()
    if "length_of_stay" in filtered.columns
    else float("nan")
)

average_billing = (
    filtered["billing_amount"].mean()
    if "billing_amount" in filtered.columns
    else float("nan")
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Admission Records", f"{total_admissions:,}")

c2.metric(
    "Unique Listed Doctors",
    f"{unique_doctors:,}" if unique_doctors is not None else "N/A"
)

c3.metric(
    "Average Length of Stay",
    f"{average_stay:.1f} days"
    if pd.notna(average_stay) else "N/A"
)

c4.metric(
    "Average Billing",
    f"₹{average_billing:,.2f}"
    if pd.notna(average_billing) else "N/A"
)

st.divider()


# =====================================
# Workload by Department
# =====================================

st.subheader("Admission Workload by Department")

workload = (
    filtered.groupby("department")
    .size()
    .reset_index(name="Admission Records")
    .sort_values("Admission Records", ascending=False)
)

if not workload.empty:
    st.bar_chart(
        workload,
        x="department",
        y="Admission Records"
    )
else:
    st.info("No records match the selected filters.")

st.divider()


# =====================================
# Listed Doctor Workload
# =====================================

st.subheader("Admissions per Listed Doctor")

if "doctor" in filtered.columns:
    doctor_workload = (
        filtered.groupby("department")
        .agg(
            Admission_Records=("department", "size"),
            Unique_Doctors=("doctor", "nunique")
        )
        .reset_index()
    )

    doctor_workload["Admissions_per_Listed_Doctor"] = (
        doctor_workload["Admission_Records"]
        / doctor_workload["Unique_Doctors"].replace(0, pd.NA)
    )

    st.bar_chart(
        doctor_workload,
        x="department",
        y="Admissions_per_Listed_Doctor"
    )

    st.dataframe(
        doctor_workload.round(2),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "This is a descriptive ratio based on the doctor names in the "
        "dataset. It does not measure actual working hours, patient "
        "assignments, or clinical workload."
    )
else:
    st.warning("Doctor data is unavailable.")

st.divider()


# =====================================
# Length of Stay by Department
# =====================================

st.subheader("Average Length of Stay by Department")

if "length_of_stay" in filtered.columns:
    stay_summary = (
        filtered.groupby("department")["length_of_stay"]
        .mean()
        .reset_index(name="Average Length of Stay")
        .round(2)
    )

    st.bar_chart(
        stay_summary,
        x="department",
        y="Average Length of Stay"
    )

st.divider()


# =====================================
# Bed Utilization Data Requirements
# =====================================

st.subheader("Bed Occupancy and Utilization")

col1, col2 = st.columns(2)

with col1:
    st.metric("Bed Occupancy Rate", "Unavailable")
    st.write(
        "Requires occupied beds and total available beds measured "
        "at the same time."
    )

with col2:
    st.metric("Bed Utilization Rate", "Unavailable")
    st.write(
        "Requires bed capacity and bed-use records over a defined "
        "time period."
    )

with st.expander("What additional data is needed?"):
    st.markdown(
        """
        - Hospital or department identifier
        - Total operational bed capacity
        - Number of occupied beds
        - Date and time of each occupancy measurement
        - Beds temporarily unavailable, if applicable
        """
    )

    st.code(
        "Bed Occupancy Rate = "
        "(Occupied Beds / Available Beds) * 100",
        language="text"
    )

st.divider()


# =====================================
# Department Resource Summary
# =====================================

st.subheader("Resource Summary by Department")

summary = (
    filtered.groupby("department")
    .agg(
        Admission_Records=("department", "size"),
        Average_Length_of_Stay=("length_of_stay", "mean"),
        Average_Billing=("billing_amount", "mean")
    )
    .reset_index()
    .round(2)
)

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "Download Resource Summary",
    data=summary.to_csv(index=False).encode("utf-8"),
    file_name="hospital_resource_summary.csv",
    mime="text/csv"
)

st.divider()
st.caption("MedTrack | Hospital Analytics Project")
