
import streamlit as st
import pandas as pd
from pathlib import Path

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="Hospital Overview | MedTrack",
    page_icon="🏥",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================
# Load Dataset
# =====================================

@st.cache_data
def load_data():
    file_path = BASE_DIR / "hospital_cleaned.csv"
    df = pd.read_csv(file_path)

    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    if "date_of_admission" in df.columns:
        df["date_of_admission"] = pd.to_datetime(
            df["date_of_admission"], errors="coerce"
        )

    for col in ["billing_amount", "length_of_stay"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "department" not in df.columns:
        mapping = {
            "Cancer": "Oncology",
            "Obesity": "General Medicine",
            "Diabetes": "Endocrinology",
            "Asthma": "Pulmonology",
            "Hypertension": "Cardiology",
            "Arthritis": "Rheumatology",
        }

        df["department"] = (
            df["medical_condition"]
            .astype("string")
            .str.strip()
            .str.title()
            .map(mapping)
            .fillna("Other")
        )

    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error("hospital_cleaned.csv was not found in the project folder.")
    st.stop()

# =====================================
# Sidebar Filters
# =====================================

st.sidebar.title("🏥 MedTrack")
st.sidebar.caption("Hospital Analytics Platform")
st.sidebar.divider()

st.sidebar.subheader("Dashboard Filters")

departments = sorted(df["department"].dropna().unique())

selected_departments = st.sidebar.multiselect(
    "Select Department",
    departments,
    default=departments
)

filtered = df[df["department"].isin(selected_departments)].copy()

if "medical_condition" in filtered.columns:
    conditions = sorted(
        filtered["medical_condition"].dropna().unique()
    )

    selected_conditions = st.sidebar.multiselect(
        "Medical Condition",
        conditions,
        default=conditions
    )

    filtered = filtered[
        filtered["medical_condition"].isin(selected_conditions)
    ]

# =====================================
# Dashboard Header
# =====================================

st.title("🏥 Hospital Overview")
st.markdown(
    "A consolidated view of hospital admissions and patient statistics."
)

st.caption("MedTrack | Hospital Data Analytics")
st.divider()

# =====================================
# KPI Cards
# =====================================

total_admissions = len(filtered)

average_age = (
    filtered["age"].mean()
    if "age" in filtered.columns else float("nan")
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

c1.metric("Total Admissions", f"{total_admissions:,}")
c2.metric(
    "Average Patient Age",
    f"{average_age:.1f} years" if pd.notna(average_age) else "N/A"
)
c3.metric(
    "Average Length of Stay",
    f"{average_stay:.1f} days" if pd.notna(average_stay) else "N/A"
)
c4.metric(
    "Average Billing",
    f"₹{average_billing:,.2f}" if pd.notna(average_billing) else "N/A"
)

st.divider()

# =====================================
# Department and Condition Charts
# =====================================

left, right = st.columns(2)

with left:
    st.subheader("Admissions by Department")

    department_counts = (
        filtered["department"]
        .value_counts()
        .rename_axis("Department")
        .reset_index(name="Admissions")
    )

    if not department_counts.empty:
        st.bar_chart(
            department_counts,
            x="Department",
            y="Admissions"
        )
    else:
        st.info("No data for the selected filters.")

with right:
    st.subheader("Admissions by Medical Condition")

    if "medical_condition" in filtered.columns:
        condition_counts = (
            filtered["medical_condition"]
            .value_counts()
            .rename_axis("Medical Condition")
            .reset_index(name="Admissions")
        )

        if not condition_counts.empty:
            st.bar_chart(
                condition_counts,
                x="Medical Condition",
                y="Admissions"
            )
        else:
            st.info("No data for the selected filters.")

st.divider()

# =====================================
# Admission Trends
# =====================================

st.subheader("Admission Trends Over Time")

if "date_of_admission" in filtered.columns:
    trend_data = filtered.dropna(
        subset=["date_of_admission"]
    ).copy()

    if not trend_data.empty:
        trend_data["Month"] = (
            trend_data["date_of_admission"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_admissions = (
            trend_data.groupby("Month")
            .size()
            .reset_index(name="Admissions")
        )

        st.line_chart(
            monthly_admissions,
            x="Month",
            y="Admissions"
        )
    else:
        st.info("No valid admission dates are available.")

# =====================================
# Summary Table
# =====================================

st.subheader("Department Summary")

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
    "Download Overview Data",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="hospital_overview.csv",
    mime="text/csv"
)

st.divider()
st.caption("MedTrack | Hospital Analytics Project")


# Donut Chart: Admissions by Department
import plotly.express as px

st.subheader("Department-wise Admission Distribution")

donut_data = (
    df.groupby("department")
    .size()
    .reset_index(name="admissions")
)

fig = px.pie(
    donut_data,
    names="department",
    values="admissions",
    hole=0.55,
    title="Share of Admission Records by Department"
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig.update_layout(
    template="plotly_dark",
    legend_title_text="Department"
)

st.plotly_chart(fig, use_container_width=True)
