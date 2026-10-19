
import streamlit as st
import pandas as pd
from pathlib import Path

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="Patient Flow | MedTrack",
    page_icon="📈",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================
# Load Dataset
# =====================================

@st.cache_data
def load_data():
    df = pd.read_csv(BASE_DIR / "hospital_cleaned.csv")

    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    for col in ["date_of_admission", "discharge_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col], errors="coerce"
            )

    if "length_of_stay" in df.columns:
        df["length_of_stay"] = pd.to_numeric(
            df["length_of_stay"], errors="coerce"
        )

    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error("hospital_cleaned.csv was not found in the project folder.")
    st.stop()

# =====================================
# Sidebar
# =====================================

st.sidebar.title("🏥 MedTrack")
st.sidebar.caption("Patient Flow Analytics")
st.sidebar.divider()

filtered = df.copy()

if "admission_type" in filtered.columns:
    options = sorted(
        filtered["admission_type"].dropna().unique().tolist()
    )

    selected_types = st.sidebar.multiselect(
        "Admission Type",
        options,
        default=options
    )

    filtered = filtered[
        filtered["admission_type"].isin(selected_types)
    ]

if "medical_condition" in filtered.columns:
    conditions = sorted(
        filtered["medical_condition"].dropna().unique().tolist()
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
# Header
# =====================================

st.title("📈 Patient Flow Analytics")
st.markdown(
    "Understand admission patterns, discharge trends, and length of stay."
)

st.divider()

# =====================================
# KPI Cards
# =====================================

total_admissions = len(filtered)

average_stay = (
    filtered["length_of_stay"].mean()
    if "length_of_stay" in filtered.columns
    else float("nan")
)

valid_admissions = (
    filtered["date_of_admission"].notna().sum()
    if "date_of_admission" in filtered.columns
    else 0
)

valid_discharges = (
    filtered["discharge_date"].notna().sum()
    if "discharge_date" in filtered.columns
    else 0
)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Admission Records", f"{total_admissions:,}")
c2.metric(
    "Average Stay",
    f"{average_stay:.1f} days"
    if pd.notna(average_stay) else "N/A"
)
c3.metric("Valid Admission Dates", f"{valid_admissions:,}")
c4.metric("Valid Discharge Dates", f"{valid_discharges:,}")

st.divider()

# =====================================
# Admissions Over Time
# =====================================

left, right = st.columns(2)

with left:
    st.subheader("Monthly Admissions")

    if "date_of_admission" in filtered.columns:
        data = filtered.dropna(
            subset=["date_of_admission"]
        ).copy()

        if not data.empty:
            data["Month"] = (
                data["date_of_admission"]
                .dt.to_period("M")
                .astype(str)
            )

            monthly = (
                data.groupby("Month")
                .size()
                .reset_index(name="Admissions")
            )

            st.line_chart(
                monthly,
                x="Month",
                y="Admissions"
            )
        else:
            st.info("No valid admission dates found.")

with right:
    st.subheader("Admissions by Type")

    if "admission_type" in filtered.columns:
        admission_counts = (
            filtered["admission_type"]
            .value_counts()
            .rename_axis("Admission Type")
            .reset_index(name="Admissions")
        )

        st.bar_chart(
            admission_counts,
            x="Admission Type",
            y="Admissions"
        )

st.divider()

# =====================================
# Discharges Over Time
# =====================================

st.subheader("Monthly Discharges")

if "discharge_date" in filtered.columns:
    data = filtered.dropna(
        subset=["discharge_date"]
    ).copy()

    if not data.empty:
        data["Month"] = (
            data["discharge_date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_discharges = (
            data.groupby("Month")
            .size()
            .reset_index(name="Discharges")
        )

        st.bar_chart(
            monthly_discharges,
            x="Month",
            y="Discharges"
        )
    else:
        st.info("No valid discharge dates found.")

st.divider()

# =====================================
# Length of Stay Analysis
# =====================================

st.subheader("Length of Stay Distribution")

if "length_of_stay" in filtered.columns:
    stay_data = filtered[
        filtered["length_of_stay"].notna()
    ][["length_of_stay"]]

    if not stay_data.empty:
        st.histogram if False else None

        st.bar_chart(
            stay_data["length_of_stay"]
            .value_counts()
            .sort_index()
            .rename_axis("Length of Stay (Days)")
            .reset_index(name="Number of Records")
            .head(60),
            x="Length of Stay (Days)",
            y="Number of Records"
        )
    else:
        st.info("Length-of-stay information is unavailable.")

st.divider()

# =====================================
# Data Table
# =====================================

st.subheader("Patient Flow Records")

columns_to_show = [
    col for col in [
        "name",
        "medical_condition",
        "admission_type",
        "date_of_admission",
        "discharge_date",
        "length_of_stay"
    ]
    if col in filtered.columns
]

st.dataframe(
    filtered[columns_to_show],
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "Download Patient Flow Data",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="patient_flow_data.csv",
    mime="text/csv"
)

st.divider()
st.caption("MedTrack | Patient Flow Analytics")


# Histogram: Distribution of Length of Stay
import plotly.express as px

st.subheader("Length of Stay Distribution")

fig = px.histogram(
    df,
    x="length_of_stay",
    nbins=20,
    title="Distribution of Length of Stay",
    labels={
        "length_of_stay": "Length of Stay (Days)"
    }
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Length of Stay (Days)",
    yaxis_title="Number of Admission Records"
)

st.plotly_chart(fig, use_container_width=True)



# =====================================
# Box Plot: Length of Stay by Department
# =====================================

import plotly.express as px

st.subheader("Length of Stay by Department")

# Use the existing dataframe from your page
plot_data = df[
    ["length_of_stay", "department"]
].dropna().copy()

fig = px.box(
    plot_data,
    x="department",
    y="length_of_stay",
    color="department",
    title="Variation in Length of Stay Across Departments",
    labels={
        "department": "Department",
        "length_of_stay": "Length of Stay (Days)"
    },
    points=False
)

fig.update_layout(
    template="plotly_dark",
    height=450,
    showlegend=False,
    xaxis_title="Department",
    yaxis_title="Length of Stay (Days)"
)

st.plotly_chart(fig, use_container_width=True)
