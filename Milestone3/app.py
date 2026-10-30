import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Hospital Performance Intelligence",
    layout="wide",
    initial_sidebar_state="locked"
)

# ============================================================
# CUSTOM STYLE
# ============================================================
st.markdown("""
<style>

/* =========================
   MAIN APP
   ========================= */

[data-testid="stAppViewContainer"] {
    background-color: #ffffff;
}
/* FORCE SIDEBAR TOGGLE TO BE VISIBLE */

[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    color: #12355b !important;
}

[data-testid="stHeader"] {
    background-color: #ffffff;
}

.main {
    background-color: #ffffff;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}


/* =========================
   MAIN TEXT
   ========================= */

h1 {
    color: #12355b !important;
    font-weight: 700;
}

h2 {
    color: #174a7c !important;
}

h3 {
    color: #245b89 !important;
}

p {
    color: #333333;
}


/* =========================
   SIDEBAR
   ========================= */

[data-testid="stSidebar"] {
    background-color: #eef4fa !important;
}

[data-testid="stSidebar"] * {
    color: #12355b !important;
}

[data-testid="stSidebar"] label {
    color: #12355b !important;
    font-weight: 500;
}


/* Sidebar navigation text */

[data-testid="stSidebar"] [role="radiogroup"] label {
    color: #12355b !important;
    font-size: 15px;
}

[data-testid="stSidebar"] [role="radiogroup"] label p {
    color: #12355b !important;
}


/* =========================
   KPI CARDS
   ========================= */

[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border-radius: 12px;
    padding: 18px;
    border: 1px solid #d9e2ec;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

[data-testid="stMetricLabel"] {
    color: #4b6075 !important;
}

[data-testid="stMetricLabel"] p {
    color: #4b6075 !important;
}

[data-testid="stMetricValue"] {
    color: #12355b !important;
}

[data-testid="stMetricValue"] div {
    color: #12355b !important;
}


/* =========================
   SELECTBOX / MULTISELECT
   ========================= */

[data-testid="stMultiSelect"] label {
    color: #12355b !important;
}

[data-testid="stMultiSelect"] input {
    color: #12355b !important;
}


/* =========================
   INFO / CAPTION
   ========================= */

[data-testid="stCaptionContainer"] {
    color: #5f6b76 !important;
}


/* =========================
   DIVIDERS
   ========================= */

hr {
    border-color: #d9e2ec !important;
}


/* =========================
   TABLE
   ========================= */

[data-testid="stDataFrame"] {
    border-radius: 10px;
}


/* =========================
   BUTTONS
   ========================= */

.stButton button {
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

weekly_path = DATA_DIR / "hospital_cleaned.csv"
admission_path = DATA_DIR / "hospital_admissions_cleaned.csv"

weekly_df = pd.read_csv(weekly_path)
admission_df = pd.read_csv(admission_path)

# Convert dates
admission_df["admission_date"] = pd.to_datetime(
    admission_df["admission_date"],
    errors="coerce"
)

# Convert readmission column safely
def convert_bool(value):
    if pd.isna(value):
        return pd.NA

    if isinstance(value, bool):
        return value

    value = str(value).strip().lower()

    if value in ["true", "1", "yes", "y"]:
        return True

    if value in ["false", "0", "no", "n"]:
        return False

    return pd.NA


admission_df["is_readmission_30d"] = (
    admission_df["is_readmission_30d"]
    .apply(convert_bool)
)

weekly_df["month"] = weekly_df["month"].astype(str)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏥 Hospital Analytics")

st.sidebar.markdown(
    "### Dashboard Navigation"
)

page = st.sidebar.radio(
    "Select Dashboard",
    [
        "Hospital Overview",
        "Patient Flow",
        "Department Analytics",
        "Resource Utilization"
    ]
)

st.sidebar.markdown("---")

# Department filter
departments = sorted(
    admission_df["department"]
    .dropna()
    .unique()
    .tolist()
)

selected_departments = st.sidebar.multiselect(
    "Filter Departments",
    departments,
    default=departments
)

filtered_admissions = admission_df[
    admission_df["department"].isin(selected_departments)
].copy()

st.sidebar.markdown("---")

st.sidebar.info(
    "Department filters affect admission-level KPIs and analyses. "
    "Operational resource charts use the weekly hospital dataset."
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Hospital Performance Intelligence System\n"
    "Milestone 3"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def empty_message(message):
    st.warning(message)


def format_percent(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:.1f}%"


# ============================================================
# PAGE 1 — HOSPITAL OVERVIEW
# ============================================================

if page == "Hospital Overview":

    st.title("🏥 Hospital Performance Intelligence")

    st.markdown(
        "### Hospital Overview Dashboard"
    )

    st.write(
        "An interactive view of hospital admissions, patient outcomes, "
        "operational activity, and departmental performance."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    total_admissions = weekly_df["patients_admitted"].sum()

    avg_los = filtered_admissions["length_of_stay_days"].mean()

    readmission_rate = (
        filtered_admissions["is_readmission_30d"]
        .dropna()
        .astype(bool)
        .mean() * 100
        if filtered_admissions["is_readmission_30d"].notna().any()
        else 0
    )

    satisfaction = filtered_admissions[
        "patient_satisfaction"
    ].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Admissions",
        f"{total_admissions:,.0f}"
    )

    col2.metric(
        "Average Length of Stay",
        f"{avg_los:.2f} days"
        if not pd.isna(avg_los)
        else "N/A"
    )

    col3.metric(
        "30-Day Readmission",
        format_percent(readmission_rate)
    )

    col4.metric(
        "Patient Satisfaction",
        f"{satisfaction:.2f}"
        if not pd.isna(satisfaction)
        else "N/A"
    )

    st.caption(
        "Total admissions are based on weekly operational admission records. "
        "LOS, readmission and satisfaction are calculated from admission-level data."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # MONTHLY OPERATIONAL TREND
    # --------------------------------------------------------

    st.subheader("📈 Monthly Operational Admissions")

    monthly_operations = (
        weekly_df
        .groupby("month")["patients_admitted"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        monthly_operations,
        x="month",
        y="patients_admitted",
        markers=True,
        title="Monthly Admissions Trend"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Patients Admitted",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # DEPARTMENT VOLUME
    # --------------------------------------------------------

    st.subheader("🏨 Patient Volume by Department")

    department_volume = (
        filtered_admissions
        .groupby("department")
        .size()
        .reset_index(name="Patient Records")
    )

    if not department_volume.empty:

        fig = px.bar(
            department_volume,
            x="department",
            y="Patient Records",
            color="Patient Records",
            color_continuous_scale="Blues",
            title="Admission Records by Department"
        )

        fig.update_layout(
            xaxis_title="Department",
            yaxis_title="Patient Records"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        empty_message(
            "No departments selected."
        )


# ============================================================
# PAGE 2 — PATIENT FLOW
# ============================================================

elif page == "Patient Flow":

    st.title("👥 Patient Flow Analytics")

    st.write(
        "Monitor admission trends, discharge outcomes, patient movement, "
        "and length of stay."
    )

    st.markdown("---")

    if filtered_admissions.empty:

        empty_message(
            "Please select at least one department."
        )

    else:

        # ----------------------------------------------------
        # ADMISSION TREND
        # ----------------------------------------------------

        st.subheader("📈 Admission Trend")

        admission_trend = (
            filtered_admissions
            .dropna(subset=["admission_date"])
            .groupby(
                filtered_admissions["admission_date"]
                .dt.to_period("M")
                .astype(str)
            )
            .size()
            .reset_index(name="Admissions")
        )

        admission_trend.columns = [
            "Month",
            "Admissions"
        ]

        fig = px.line(
            admission_trend,
            x="Month",
            y="Admissions",
            markers=True,
            title="Monthly Patient Admissions"
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Admissions",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # TWO COLUMN SECTION
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("🚪 Discharge Outcomes")

            discharge = (
                filtered_admissions[
                    "discharge_status"
                ]
                .value_counts()
                .reset_index()
            )

            discharge.columns = [
                "Discharge Status",
                "Patients"
            ]

            fig = px.pie(
                discharge,
                names="Discharge Status",
                values="Patients",
                title="Patient Discharge Outcomes"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            st.subheader("🛏️ Average Length of Stay")

            los_department = (
                filtered_admissions
                .groupby("department")[
                    "length_of_stay_days"
                ]
                .mean()
                .reset_index()
            )

            fig = px.bar(
                los_department,
                x="department",
                y="length_of_stay_days",
                color="length_of_stay_days",
                color_continuous_scale="Blues",
                title="Average LOS by Department"
            )

            fig.update_layout(
                xaxis_title="Department",
                yaxis_title="Average LOS (Days)"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # PATIENT LOAD
        # ----------------------------------------------------

        st.subheader("👥 Weekly Patient Load")

        patient_load = (
            weekly_df
            .groupby("week")["patient_count"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            patient_load,
            x="week",
            y="patient_count",
            markers=True,
            title="Weekly Patient Load"
        )

        fig.update_layout(
            xaxis_title="Week",
            yaxis_title="Patient Count"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PAGE 3 — DEPARTMENT ANALYTICS
# ============================================================

elif page == "Department Analytics":

    st.title("🏨 Department Analytics")

    st.write(
        "Compare patient volume, readmission, satisfaction, "
        "and length of stay across departments."
    )

    st.markdown("---")

    if filtered_admissions.empty:

        empty_message(
            "Please select at least one department."
        )

    else:

        # ----------------------------------------------------
        # DEPARTMENT SUMMARY
        # ----------------------------------------------------

        dept_summary = (
            filtered_admissions
            .groupby("department")
            .agg(
                Patient_Volume=(
                    "admission_id",
                    "count"
                ),
                Average_LOS=(
                    "length_of_stay_days",
                    "mean"
                ),
                Average_Satisfaction=(
                    "patient_satisfaction",
                    "mean"
                ),
                Readmissions=(
                    "is_readmission_30d",
                    lambda x: x.dropna().astype(bool).sum()
                )
            )
            .reset_index()
        )

        # ----------------------------------------------------
        # PATIENT VOLUME
        # ----------------------------------------------------

        st.subheader("👥 Patient Volume by Department")

        fig = px.bar(
            dept_summary,
            x="department",
            y="Patient_Volume",
            color="Patient_Volume",
            color_continuous_scale="Blues",
            title="Patient Volume"
        )

        fig.update_layout(
            xaxis_title="Department",
            yaxis_title="Patient Volume"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # READMISSION RATE
        # ----------------------------------------------------

        st.subheader("🔄 Readmission Rate by Department")

        readmission_dept = (
            filtered_admissions
            .groupby("department")[
                "is_readmission_30d"
            ]
            .apply(
                lambda x:
                x.dropna().astype(bool).mean() * 100
                if x.dropna().shape[0] > 0
                else 0
            )
            .reset_index(
                name="Readmission Rate (%)"
            )
        )

        fig = px.bar(
            readmission_dept,
            x="department",
            y="Readmission Rate (%)",
            color="Readmission Rate (%)",
            color_continuous_scale="Blues",
            title="30-Day Readmission Rate"
        )

        fig.update_layout(
            xaxis_title="Department",
            yaxis_title="Readmission Rate (%)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # SATISFACTION
        # ----------------------------------------------------

        st.subheader("⭐ Patient Satisfaction by Department")

        satisfaction_dept = (
            filtered_admissions
            .groupby("department")[
                "patient_satisfaction"
            ]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            satisfaction_dept,
            x="department",
            y="patient_satisfaction",
            color="patient_satisfaction",
            color_continuous_scale="Blues",
            title="Average Patient Satisfaction"
        )

        fig.update_layout(
            xaxis_title="Department",
            yaxis_title="Average Satisfaction"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # SUMMARY TABLE
        # ----------------------------------------------------

        st.subheader("📋 Department Performance Summary")

        display_summary = dept_summary.copy()

        display_summary["Average_LOS"] = (
            display_summary["Average_LOS"]
            .round(2)
        )

        display_summary["Average_Satisfaction"] = (
            display_summary["Average_Satisfaction"]
            .round(2)
        )

        display_summary.columns = [
            "Department",
            "Patient Volume",
            "Average LOS",
            "Average Satisfaction",
            "Readmissions"
        ]

        st.dataframe(
            display_summary,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PAGE 4 — RESOURCE UTILIZATION
# ============================================================

elif page == "Resource Utilization":

    st.title("🛏️ Resource Utilization")

    st.write(
        "Monitor available beds, staffing levels, and estimated "
        "hospital capacity utilization."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # AVAILABLE BEDS
    # --------------------------------------------------------

    st.subheader("🛏️ Available Beds by Service")

    beds = (
        weekly_df
        .groupby("service")["available_beds"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        beds,
        x="service",
        y="available_beds",
        color="available_beds",
        color_continuous_scale="Blues",
        title="Average Available Beds"
    )

    fig.update_layout(
        xaxis_title="Service",
        yaxis_title="Average Available Beds"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # STAFF
    # --------------------------------------------------------

    st.subheader("👨‍⚕️ Staff Allocation")

    staff = (
        weekly_df
        .groupby("service")[
            ["staff_present", "staff_count"]
        ]
        .mean()
        .reset_index()
    )

    staff_long = staff.melt(
        id_vars="service",
        value_vars=[
            "staff_present",
            "staff_count"
        ],
        var_name="Staff Metric",
        value_name="Staff Count"
    )

    staff_long["Staff Metric"] = (
        staff_long["Staff Metric"]
        .replace({
            "staff_present": "Staff Present",
            "staff_count": "Total Staff"
        })
    )

    fig = px.bar(
        staff_long,
        x="service",
        y="Staff Count",
        color="Staff Metric",
        barmode="group",
        title="Staff Presence vs Total Staff"
    )

    fig.update_layout(
        xaxis_title="Service",
        yaxis_title="Average Staff Count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # STAFF COVERAGE
    # --------------------------------------------------------

    st.subheader("👨‍⚕️ Staff Coverage")

    staff["Staff Coverage (%)"] = (
        staff["staff_present"]
        / staff["staff_count"].replace(0, pd.NA)
        * 100
    )

    staff_coverage = staff.dropna(
        subset=["Staff Coverage (%)"]
    )

    fig = px.bar(
        staff_coverage,
        x="service",
        y="Staff Coverage (%)",
        color="Staff Coverage (%)",
        color_continuous_scale="Blues",
        title="Average Staff Coverage"
    )

    fig.update_layout(
        xaxis_title="Service",
        yaxis_title="Staff Coverage (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # ESTIMATED BED UTILIZATION
    # --------------------------------------------------------

    st.subheader("📊 Estimated Bed Utilization")

    util_data = weekly_df.copy()

    denominator = (
        util_data["available_beds"] * 7
    )

    util_data["estimated_utilization"] = (
        util_data["patient_count"]
        * util_data["average_length_of_stay"]
        / denominator.replace(0, pd.NA)
        * 100
    )

    util_data = util_data.dropna(
        subset=["estimated_utilization"]
    )

    util_service = (
        util_data
        .groupby("service")[
            "estimated_utilization"
        ]
        .mean()
        .reset_index()
    )

    util_service.columns = [
        "Service",
        "Estimated Utilization (%)"
    ]

    fig = px.bar(
        util_service,
        x="Service",
        y="Estimated Utilization (%)",
        color="Estimated Utilization (%)",
        color_continuous_scale="Blues",
        title="Estimated Bed Utilization by Service"
    )

    fig.update_layout(
        xaxis_title="Service",
        yaxis_title="Estimated Utilization (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "Bed utilization is an estimated operational indicator based on "
        "patient count, average length of stay, available beds, and a 7-day week. "
        "The dataset does not contain direct occupied-bed measurements."
    )

    # --------------------------------------------------------
    # EQUIPMENT
    # --------------------------------------------------------

    st.subheader("⚙️ Equipment Utilization")

    st.info(
        "Equipment-level usage data is not available in the supplied datasets. "
        "Therefore, equipment utilization is not calculated to avoid presenting "
        "unsupported values."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Hospital Performance Intelligence System | "
    "Milestone 3 | Interactive Streamlit Dashboard"
)