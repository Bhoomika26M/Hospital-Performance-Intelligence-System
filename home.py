import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================
# 1. Page Configuration
# ==========================================

st.set_page_config(
    page_title="MedTrack | Hospital Analytics",
    page_icon="🏥",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent

# ==========================================
# 2. Load Datasets
# ==========================================

@st.cache_data
def load_data():
    patient_file = BASE_DIR / "hospital_cleaned.csv"
    kpi_file = BASE_DIR / "hospital_kpi_summary.csv"
    department_file = BASE_DIR / "hospital_department_analytics.csv"

    patients = pd.read_csv(patient_file)
    kpis = pd.read_csv(kpi_file)
    departments = pd.read_csv(department_file)

    return patients, kpis, departments


try:
    patients, kpis, departments = load_data()
except FileNotFoundError as error:
    st.error(f"Required file not found: {error.filename}")
    st.info(
        "Make sure hospital_cleaned.csv, hospital_kpi_summary.csv, "
        "and hospital_department_analytics.csv are in the same folder as app.py."
    )
    st.stop()

# ==========================================
# 3. Prepare Data
# ==========================================

patients.columns = patients.columns.str.strip().str.lower()
departments.columns = departments.columns.str.strip().str.lower()
kpis.columns = kpis.columns.str.strip().str.lower()

for column in ["date_of_admission", "discharge_date"]:
    if column in patients.columns:
        patients[column] = pd.to_datetime(
            patients[column], errors="coerce"
        )

if "department" not in patients.columns:
    if "medical_condition" in patients.columns:
        mapping = {
            "Cancer": "Oncology",
            "Obesity": "General Medicine",
            "Diabetes": "Endocrinology",
            "Asthma": "Pulmonology",
            "Hypertension": "Cardiology",
            "Arthritis": "Rheumatology",
        }
        patients["department"] = (
            patients["medical_condition"]
            .astype("string")
            .str.strip()
            .str.title()
            .map(mapping)
            .fillna("Other")
        )
    else:
        patients["department"] = "Unknown"

# ==========================================
# 4. Sidebar Filters
# ==========================================

st.sidebar.title("🏥 MedTrack")
st.sidebar.caption("Hospital Analytics Dashboard")
st.sidebar.divider()

st.sidebar.subheader("Filters")

filtered = patients.copy()

if "department" in filtered.columns:
    department_options = sorted(
        filtered["department"].dropna().unique().tolist()
    )
    selected_departments = st.sidebar.multiselect(
        "Department",
        department_options,
        default=department_options
    )
    filtered = filtered[
        filtered["department"].isin(selected_departments)
    ]

if "medical_condition" in filtered.columns:
    condition_options = sorted(
        filtered["medical_condition"].dropna().unique().tolist()
    )
    selected_conditions = st.sidebar.multiselect(
        "Medical Condition",
        condition_options,
        default=condition_options
    )
    filtered = filtered[
        filtered["medical_condition"].isin(selected_conditions)
    ]

if "admission_type" in filtered.columns:
    admission_options = sorted(
        filtered["admission_type"].dropna().unique().tolist()
    )
    selected_admissions = st.sidebar.multiselect(
        "Admission Type",
        admission_options,
        default=admission_options
    )
    filtered = filtered[
        filtered["admission_type"].isin(selected_admissions)
    ]

if "date_of_admission" in filtered.columns:
    valid_dates = filtered["date_of_admission"].dropna()

    if not valid_dates.empty:
        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()

        date_range = st.sidebar.date_input(
            "Admission Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
            start_date, end_date = date_range
            filtered = filtered[
                filtered["date_of_admission"].dt.date.between(
                    start_date, end_date
                )
            ]

# ==========================================
# 5. Dashboard Header
# ==========================================

st.title("🏥 MedTrack Hospital Analytics")
st.markdown(
    "### Monitor admissions, patient flow, and department performance"
)

st.caption(
    "Dashboard metrics are based on the available healthcare dataset. "
    "Some operational metrics require additional hospital records."
)

st.divider()

# ==========================================
# 6. Hospital Overview KPIs
# ==========================================

st.subheader("Hospital Overview")

total_admissions = len(filtered)

if "length_of_stay" in filtered.columns:
    average_stay = pd.to_numeric(
        filtered["length_of_stay"], errors="coerce"
    ).mean()
else:
    average_stay = float("nan")

if "billing_amount" in filtered.columns:
    average_billing = pd.to_numeric(
        filtered["billing_amount"], errors="coerce"
    ).mean()
else:
    average_billing = float("nan")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Admissions", f"{total_admissions:,}")
col2.metric(
    "Average Stay",
    f"{average_stay:.1f} days" if pd.notna(average_stay) else "N/A"
)
col3.metric(
    "Average Billing",
    f"₹{average_billing:,.2f}" if pd.notna(average_billing) else "N/A"
)
col4.metric("Departments", filtered["department"].nunique())

st.divider()

# ==========================================
# 7. Hospital Overview Charts
# ==========================================

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
            y="Admissions",
            color="#3B82F6"
        )
    else:
        st.info("No data available for the selected filters.")

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
                y="Admissions",
                color="#14B8A6"
            )
        else:
            st.info("No data available for the selected filters.")

st.divider()

# ==========================================
# 8. Patient Flow
# ==========================================

st.header("Patient Flow Analytics")

flow_col1, flow_col2 = st.columns(2)

with flow_col1:
    st.subheader("Admissions Over Time")

    if "date_of_admission" in filtered.columns:
        monthly = filtered.dropna(
            subset=["date_of_admission"]
        ).copy()

        if not monthly.empty:
            monthly["Month"] = (
                monthly["date_of_admission"].dt.to_period("M").astype(str)
            )

            monthly_counts = (
                monthly.groupby("Month")
                .size()
                .reset_index(name="Admissions")
            )

            st.line_chart(
                monthly_counts,
                x="Month",
                y="Admissions",
                color="#8B5CF6"
            )
        else:
            st.info("No valid admission dates are available.")
    else:
        st.info("Admission dates are unavailable.")

with flow_col2:
    st.subheader("Admission Type Distribution")

    if "admission_type" in filtered.columns:
        admission_counts = (
            filtered["admission_type"]
            .value_counts()
            .rename_axis("Admission Type")
            .reset_index(name="Count")
        )

        if not admission_counts.empty:
            st.bar_chart(
                admission_counts,
                x="Admission Type",
                y="Count",
                color="#F59E0B"
            )
        else:
            st.info("No data available for the selected filters.")

st.divider()

# ==========================================
# 9. Department Analytics
# ==========================================

st.header("Department Analytics")

department_metrics = (
    filtered.groupby("department")
    .agg(
        total_admissions=("department", "size"),
        average_length_of_stay=("length_of_stay", "mean")
    )
    .reset_index()
)

if "billing_amount" in filtered.columns:
    billing = (
        filtered.groupby("department")["billing_amount"]
        .mean()
        .reset_index(name="average_billing_amount")
    )

    department_metrics = department_metrics.merge(
        billing, on="department", how="left"
    )

if not department_metrics.empty:
    st.dataframe(
        department_metrics.round(2),
        use_container_width=True,
        hide_index=True
    )

if "department_efficiency_score" in departments.columns:
    st.subheader("Provisional Department Efficiency Score")

    st.caption(
        "This score is an exploratory estimate based on admissions per "
        "listed doctor and length of stay. It is not a validated clinical "
        "or operational efficiency measure."
    )

    score_data = departments[
        ["department", "department_efficiency_score"]
    ].copy()

    score_data = score_data[
        score_data["department"].isin(
            filtered["department"].dropna().unique()
        )
    ]

    if not score_data.empty:
        st.bar_chart(
            score_data,
            x="department",
            y="department_efficiency_score",
            color="#6366F1"
        )

st.divider()

# ==========================================
# 10. Resource Utilization
# ==========================================

st.header("Resource Utilization")

st.warning(
    "Occupancy rate and bed utilization cannot be calculated from the "
    "current dataset because bed capacity and occupied-bed records "
    "are not available."
)

resource_col1, resource_col2 = st.columns(2)

with resource_col1:
    st.metric("Occupancy Rate", "Unavailable")

with resource_col2:
    st.metric("Bed Utilization Rate", "Unavailable")

st.info(
    "To calculate these metrics accurately, obtain hospital bed capacity, "
    "occupied-bed counts, and time-based bed availability records."
)

st.divider()

# ==========================================
# 11. Readmission Information
# ==========================================

st.header("Readmission Analytics")

st.warning(
    "Readmission rate is unavailable because this dataset does not provide "
    "reliable patient identifiers and longitudinal visit history."
)

st.divider()

# ==========================================
# 12. Patient Data Explorer
# ==========================================

st.header("Patient Data Explorer")

st.caption(
    "The table below reflects the filters selected in the sidebar."
)

st.write(f"Showing {len(filtered):,} records.")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Patient Data (CSV)",
    data=csv_data,
    file_name="hospital_filtered_data.csv",
    mime="text/csv"
)

# ==========================================
# 13. Footer
# ==========================================

st.divider()

st.caption(
    "MedTrack | Hospital Data Analytics Project | "
    "Exploratory analysis of the provided dataset"
)
