
import streamlit as st
import pandas as pd
from pathlib import Path

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="Department Analytics | MedTrack",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================
# Load Data
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
st.sidebar.caption("Department Analytics")
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

st.title("📊 Department Analytics")
st.markdown(
    "Compare admissions, patient stays, billing, and departmental workload."
)

st.divider()


# =====================================
# KPI Cards
# =====================================

total_admissions = len(filtered)

department_count = filtered["department"].nunique()

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

c1.metric("Admissions", f"{total_admissions:,}")
c2.metric("Departments Selected", department_count)
c3.metric(
    "Average Stay",
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
# Admissions by Department
# =====================================

left, right = st.columns(2)

with left:
    st.subheader("Admissions by Department")

    admission_summary = (
        filtered.groupby("department")
        .size()
        .reset_index(name="Admissions")
        .sort_values("Admissions", ascending=False)
    )

    st.bar_chart(
        admission_summary,
        x="department",
        y="Admissions"
    )

with right:
    st.subheader("Average Length of Stay")

    if "length_of_stay" in filtered.columns:
        stay_summary = (
            filtered.groupby("department")["length_of_stay"]
            .mean()
            .reset_index(name="Average Days")
            .round(2)
        )

        st.bar_chart(
            stay_summary,
            x="department",
            y="Average Days"
        )

st.divider()


# =====================================
# Billing Analysis
# =====================================

st.subheader("Average Billing by Department")

if "billing_amount" in filtered.columns:
    billing_summary = (
        filtered.groupby("department")["billing_amount"]
        .mean()
        .reset_index(name="Average Billing")
        .round(2)
    )

    st.bar_chart(
        billing_summary,
        x="department",
        y="Average Billing"
    )

st.divider()


# =====================================
# Doctor and Workload Analysis
# =====================================

st.subheader("Department Workload")

if "doctor" in filtered.columns:
    doctor_summary = (
        filtered.groupby("department")
        .agg(
            Admissions=("department", "size"),
            Unique_Doctors=("doctor", "nunique")
        )
        .reset_index()
    )

    doctor_summary["Admissions per Listed Doctor"] = (
        doctor_summary["Admissions"]
        / doctor_summary["Unique_Doctors"].replace(0, pd.NA)
    )

    st.dataframe(
        doctor_summary.round(2),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Doctor information is unavailable.")


# =====================================
# Efficiency Score
# =====================================

st.subheader("Provisional Department Efficiency Score")

st.caption(
    "This exploratory score combines admissions per listed doctor "
    "and average length of stay. It is not a validated clinical "
    "or operational efficiency measure."
)

if "department_efficiency_score" in departments.columns:
    score_data = departments[
        ["department", "department_efficiency_score"]
    ].copy()

    score_data = score_data[
        score_data["department"].isin(selected_departments)
    ]

    if not score_data.empty:
        st.bar_chart(
            score_data,
            x="department",
            y="department_efficiency_score"
        )

        st.dataframe(
            score_data.round(2),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No efficiency scores are available for these departments.")
else:
    st.info("The department efficiency score has not been calculated.")


# =====================================
# Department Summary Table
# =====================================

st.subheader("Detailed Department Summary")

summary = (
    filtered.groupby("department")
    .agg(
        Total_Admissions=("department", "size"),
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
    "Download Department Analytics",
    data=summary.to_csv(index=False).encode("utf-8"),
    file_name="department_analytics.csv",
    mime="text/csv"
)

st.divider()
st.caption("MedTrack | Department Analytics")



# =====================================
# Scatter Plot: Length of Stay vs Billing
# =====================================

import plotly.express as px

st.subheader("Length of Stay vs Billing Amount")

# Use the filtered dataset so sidebar selections are respected
plot_data = filtered[
    ["length_of_stay", "billing_amount", "department"]
].dropna().copy()

# Sample records to reduce overcrowding
if len(plot_data) > 1500:
    plot_data = plot_data.sample(n=1500, random_state=42)

if not plot_data.empty:
    fig = px.scatter(
        plot_data,
        x="length_of_stay",
        y="billing_amount",
        color="department",
        title="Length of Stay vs Billing Amount",
        labels={
            "length_of_stay": "Length of Stay (Days)",
            "billing_amount": "Billing Amount",
            "department": "Department"
        },
        opacity=0.5,
        render_mode="webgl"
    )

    fig.update_traces(
        marker={"size": 5}
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title_text="Department"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No valid records available for the scatter plot.")
