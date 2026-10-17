
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==================================================
# PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="MedTrack DV | Hospital Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "hospital_final_dataset.xlsx"

NAVY = "#0B1220"
SIDEBAR = "#080E19"
CARD = "#111D30"
BORDER = "#263951"
TEAL = "#2D94D4"
BLUE = "#60A5FA"
AMBER = "#A37708"
TEXT = "#E5EDF7"
MUTED = "#93A8C2"

# ==================================================
# DARK THEME STYLING
# ==================================================
st.markdown("""
<style>
    .stApp {
        background-color: #0B1220;
        color: #E5EDF7;
    }

    [data-testid="stHeader"] {
        background-color: #0B1220;
    }

    .block-container {
        max-width: 1450px;
        padding: 1.3rem 1.8rem 2rem 1.8rem;
    }

    [data-testid="stSidebar"] {
        background-color: #080E19;
        border-right: 1px solid #263951;
    }

    [data-testid="stSidebar"] * {
        color: #DCE7F5;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #B6C8DC;
    }

    .brand {
        font-size: 1.65rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.5px;
    }

    .brand-subtitle {
        color: #93A8C2;
        font-size: 0.85rem;
        margin-bottom: 1.4rem;
    }

    .hero {
        background: linear-gradient(120deg, #111D30, #123B53);
        border: 1px solid #28435E;
        padding: 1.35rem 1.65rem;
        border-radius: 15px;
        margin-bottom: 1rem;
    }

    .hero h1 {
        color: #F8FAFC;
        font-size: 1.9rem;
        margin: 0;
        padding: 0;
    }

    .hero p {
        color: #B6C8DC;
        margin: 0.4rem 0 0 0;
        font-size: 0.92rem;
    }

    .section-label {
        font-size: 1.15rem;
        font-weight: 750;
        color: #E5EDF7;
        margin: 0.8rem 0 0.55rem 0;
    }

    h1, h2, h3, p, label {
        color: #E5EDF7;
    }

    [data-testid="stMetric"] {
        background: #111D30;
        border: 1px solid #263951;
        border-radius: 12px;
        padding: 14px 16px;
        min-height: 100px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
    }

    [data-testid="stMetricLabel"] {
        color: #A8BAD0;
        font-size: 0.82rem;
    }

    [data-testid="stMetricValue"] {
        color: #F1F7FF;
        font-size: 1.65rem;
        font-weight: 750;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.78rem;
    }

    [data-testid="stTabs"] button {
        font-weight: 650;
        color: #B6C8DC;
    }

    div[data-testid="stPlotlyChart"] {
        background: #111D30;
        border: 1px solid #263951;
        border-radius: 12px;
        padding: 6px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #263951;
        border-radius: 10px;
        overflow: hidden;
    }

    div[data-testid="stDownloadButton"] button {
        border-radius: 8px;
    }

    .note {
        color: #93A8C2;
        font-size: 0.82rem;
    }

    [data-testid="stCaptionContainer"] {
        color: #93A8C2;
    }

    hr {
        border-color: #263951;
    }
</style>
""", unsafe_allow_html=True)


# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data(path):
    patients = pd.read_excel(path, sheet_name="Patient Data")
    resources = pd.read_excel(path, sheet_name="Resource Data")
    kpis = pd.read_excel(path, sheet_name="KPI Summary")
    return patients, resources, kpis


if not DATA_PATH.exists():
    st.error(
        "Excel workbook not found. "
        "Run scripts/generate_hospital_kpis.py first."
    )
    st.stop()

try:
    patients, resources, kpis = load_data(DATA_PATH)
except Exception as error:
    st.error(f"Could not load the workbook: {error}")
    st.stop()


# ==================================================
# HELPER FUNCTIONS
# ==================================================
def page_header(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def chart_layout(fig, height=310):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=12, r=20, t=48, b=18),
        font=dict(
            family="Arial, sans-serif",
            color=TEXT,
            size=12
        ),
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        title_font=dict(size=15, color="#F1F7FF"),
        legend_title_text=""
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#29394F",
        zerolinecolor="#29394F"
    )

    fig.update_yaxes(
        showgrid=False,
        zerolinecolor="#29394F"
    )

    return fig


def patient_metrics(data):
    total = len(data)

    avg_stay = (
        data["Length_of_Stay"].mean()
        if total else 0
    )

    readmission_rate = (
        data["Readmission"]
        .astype(str).str.strip().str.lower()
        .eq("yes").mean() * 100
        if total else 0
    )

    recovery_rate = (
        data["Outcome"]
        .astype(str).str.strip().str.lower()
        .eq("recovered").mean() * 100
        if total else 0
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Admissions", f"{total:,}")
    c2.metric("Average Length of Stay", f"{avg_stay:.2f}")
    c3.metric("Readmission Rate", f"{readmission_rate:.2f}%")
    c4.metric("Recovery Rate", f"{recovery_rate:.2f}%")


def resource_totals(data):
    beds_allocated = data["beds_allocated"].sum()
    beds_occupied = data["beds_occupied"].sum()
    staff_allocated = data["staff_allocated"].sum()
    staff_on_duty = data["staff_on_duty"].sum()

    bed_rate = (
        beds_occupied / beds_allocated * 100
        if beds_allocated else 0
    )

    staff_rate = (
        staff_on_duty / staff_allocated * 100
        if staff_allocated else 0
    )

    return (
        beds_allocated,
        beds_occupied,
        staff_allocated,
        staff_on_duty,
        bed_rate,
        staff_rate
    )


# ==================================================
# SIDEBAR NAVIGATION AND FILTERS
# ==================================================
with st.sidebar:
    st.markdown(
        '<div class="brand">✚ MedTrack DV</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'Hospital Intelligence Platform</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.caption("WORKSPACE")

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Patient Analytics",
            "Resource Utilization",
            "Data Explorer"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.caption("PATIENT FILTERS")

    genders = sorted(
        patients["Gender"].dropna().unique().tolist()
    )

    conditions = sorted(
        patients["Condition"].dropna().unique().tolist()
    )

    selected_genders = st.multiselect(
        "Gender",
        genders,
        default=genders
    )

    selected_conditions = st.multiselect(
        "Condition",
        conditions,
        default=conditions
    )

    st.markdown("---")

    if st.button("Reset filters", use_container_width=True):
        st.rerun()

    st.caption("MILESTONE 2 · KPI ENGINEERING")


# ==================================================
# APPLY FILTERS
# ==================================================
filtered = patients[
    patients["Gender"].isin(selected_genders)
    & patients["Condition"].isin(selected_conditions)
].copy()


# ==================================================
# OVERVIEW PAGE
# ==================================================
if page == "Overview":

    page_header(
        "Hospital Overview",
        "A clear snapshot of patient outcomes and hospital resources."
    )

    patient_metrics(filtered)

    st.markdown(
        '<div class="section-label">Patient Insights</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2, gap="medium")

    with left:
        outcome_counts = (
            filtered["Outcome"].value_counts()
            .rename_axis("Outcome")
            .reset_index(name="Patients")
        )

        fig = px.pie(
            outcome_counts,
            names="Outcome",
            values="Patients",
            hole=0.58,
            title="Patient Outcomes",
            color="Outcome",
            color_discrete_map={
                "Recovered": TEAL,
                "Stable": BLUE
            }
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(
            chart_layout(fig, 310),
            use_container_width=True
        )

    with right:
        readmission_counts = (
            filtered["Readmission"].value_counts()
            .rename_axis("Readmission")
            .reset_index(name="Patients")
        )

        fig = px.bar(
            readmission_counts,
            x="Readmission",
            y="Patients",
            color="Readmission",
            text="Patients",
            title="Readmission Status",
            color_discrete_map={
                "No": BLUE,
                "Yes": AMBER
            }
        )

        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)

        st.plotly_chart(
            chart_layout(fig, 310),
            use_container_width=True
        )

    st.markdown(
        '<div class="section-label">Resource Snapshot</div>',
        unsafe_allow_html=True
    )

    (
        beds_allocated,
        beds_occupied,
        staff_allocated,
        staff_on_duty,
        bed_rate,
        staff_rate
    ) = resource_totals(resources)

    r1, r2, r3, r4 = st.columns(4)

    r1.metric("Beds Allocated", f"{beds_allocated:,.0f}")
    r2.metric("Beds Occupied", f"{beds_occupied:,.0f}")
    r3.metric("Bed Occupancy Rate", f"{bed_rate:.2f}%")
    r4.metric("Staff On-Duty Rate", f"{staff_rate:.2f}%")

    st.caption(
        "Resource totals are calculated across records and may not "
        "represent unique hospital-wide totals."
    )


# ==================================================
# PATIENT ANALYTICS PAGE
# ==================================================
elif page == "Patient Analytics":

    page_header(
        "Patient Analytics",
        "Explore patient admissions, outcomes, readmissions, and costs."
    )

    patient_metrics(filtered)

    if filtered.empty:
        st.warning("No patient records match the selected filters.")
    else:
        st.markdown(
            '<div class="section-label">Clinical Insights</div>',
            unsafe_allow_html=True
        )

        left, right = st.columns(2, gap="medium")

        with left:
            readmission_counts = (
                filtered["Readmission"].value_counts()
                .rename_axis("Readmission")
                .reset_index(name="Patients")
            )

            fig = px.bar(
                readmission_counts,
                x="Patients",
                y="Readmission",
                orientation="h",
                color="Readmission",
                text="Patients",
                title="Readmission Comparison",
                color_discrete_map={
                    "No": BLUE,
                    "Yes": AMBER
                }
            )

            fig.update_traces(textposition="outside")
            fig.update_layout(showlegend=False)

            st.plotly_chart(
                chart_layout(fig, 290),
                use_container_width=True
            )

        with right:
            outcome_counts = (
                filtered["Outcome"].value_counts()
                .rename_axis("Outcome")
                .reset_index(name="Patients")
            )

            fig = px.bar(
                outcome_counts,
                x="Outcome",
                y="Patients",
                text="Patients",
                color="Outcome",
                title="Outcome Comparison",
                color_discrete_map={
                    "Recovered": TEAL,
                    "Stable": BLUE
                }
            )

            fig.update_traces(textposition="outside")
            fig.update_layout(showlegend=False)

            st.plotly_chart(
                chart_layout(fig, 290),
                use_container_width=True
            )

        st.markdown(
            '<div class="section-label">Length of Stay</div>',
            unsafe_allow_html=True
        )

        fig = px.histogram(
            filtered,
            x="Length_of_Stay",
            nbins=18,
            title="Patient Stay Distribution",
            color_discrete_sequence=[TEAL],
            labels={
                "Length_of_Stay": "Recorded Length of Stay",
                "count": "Number of Patients"
            }
        )

        st.plotly_chart(
            chart_layout(fig, 300),
            use_container_width=True
        )

        st.markdown(
            '<div class="section-label">Average Cost by Condition</div>',
            unsafe_allow_html=True
        )

        avg_cost = filtered["Cost"].mean()
        st.metric("Average Patient Cost", f"{avg_cost:,.2f}")

        cost_summary = (
            filtered.groupby("Condition", as_index=False)["Cost"]
            .mean()
            .sort_values("Cost", ascending=True)
        )

        fig = px.bar(
            cost_summary,
            x="Cost",
            y="Condition",
            orientation="h",
            title="Average Patient Cost by Condition",
            text_auto=",.0f",
            color_discrete_sequence=[TEAL],
            labels={
                "Cost": "Average Cost",
                "Condition": ""
            }
        )

        fig.update_traces(textposition="outside")
        fig.update_layout(
            height=max(300, len(cost_summary) * 30),
            margin=dict(l=10, r=60, t=50, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)


# ==================================================
# RESOURCE UTILIZATION PAGE
# ==================================================
elif page == "Resource Utilization":

    page_header(
        "Resource Utilization",
        "Explore bed allocation and staffing across resource records."
    )

    (
        beds_allocated,
        beds_occupied,
        staff_allocated,
        staff_on_duty,
        bed_rate,
        staff_rate
    ) = resource_totals(resources)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Beds Allocated", f"{beds_allocated:,.0f}")
    c2.metric("Beds Occupied", f"{beds_occupied:,.0f}")
    c3.metric("Bed Occupancy Rate", f"{bed_rate:.2f}%")
    c4.metric("Staff On-Duty Rate", f"{staff_rate:.2f}%")

    st.markdown(
        '<div class="section-label">Bed Allocation by Hospital</div>',
        unsafe_allow_html=True
    )

    if "hospital_name" in resources.columns:
        hospital_summary = (
            resources.groupby("hospital_name", as_index=False)
            [["beds_allocated", "beds_occupied"]]
            .sum()
            .sort_values("beds_allocated", ascending=False)
            .head(10)
            .sort_values("beds_allocated", ascending=True)
        )

        fig = px.bar(
            hospital_summary,
            x=["beds_allocated", "beds_occupied"],
            y="hospital_name",
            orientation="h",
            barmode="group",
            title="Top 10 Hospitals by Allocated Beds",
            labels={
                "value": "Number of Beds",
                "hospital_name": "Hospital",
                "variable": "Bed Status"
            },
            color_discrete_sequence=[BLUE, TEAL]
        )

        fig.update_layout(
            height=420,
            margin=dict(l=10, r=20, t=50, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="section-label">Staffing Comparison</div>',
        unsafe_allow_html=True
    )

    staffing = pd.DataFrame({
        "Staff Status": ["Allocated", "On Duty"],
        "Staff Count": [staff_allocated, staff_on_duty]
    })

    fig = px.bar(
        staffing,
        x="Staff Status",
        y="Staff Count",
        text="Staff Count",
        color="Staff Status",
        title="Staff Allocated vs On Duty",
        color_discrete_map={
            "Allocated": BLUE,
            "On Duty": TEAL
        }
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False)

    st.plotly_chart(
        chart_layout(fig, 290),
        use_container_width=True
    )

    st.caption(
        "Resource metrics are aggregated across records. "
        "Check for repeated hospital snapshots before interpreting "
        "these figures as unique hospital-wide totals."
    )


# ==================================================
# DATA EXPLORER PAGE
# ==================================================
elif page == "Data Explorer":

    page_header(
        "Data Explorer",
        "Inspect and export the datasets used by MedTrack DV."
    )

    dataset_choice = st.selectbox(
        "Choose a dataset",
        [
            "Patient Data",
            "Resource Data",
            "KPI Summary"
        ]
    )

    if dataset_choice == "Patient Data":
        view_df = filtered.copy()
    elif dataset_choice == "Resource Data":
        view_df = resources.copy()
    else:
        view_df = kpis.copy()

    c1, c2, c3 = st.columns(3)

    c1.metric("Rows", f"{len(view_df):,}")
    c2.metric("Columns", f"{len(view_df.columns):,}")
    c3.metric(
        "Missing Values",
        f"{int(view_df.isna().sum().sum()):,}"
    )

    st.markdown(
        '<div class="section-label">Dataset Preview</div>',
        unsafe_allow_html=True
    )

    preview_rows = st.selectbox(
        "Rows to display",
        [10, 25, 50, 100],
        index=1
    )

    st.dataframe(
        view_df.head(preview_rows),
        use_container_width=True,
        hide_index=True
    )

    csv = view_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download selected data as CSV",
        data=csv,
        file_name=dataset_choice.lower().replace(" ", "_") + ".csv",
        mime="text/csv"
    )

    with st.expander("View all records"):
        st.dataframe(
            view_df,
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# FOOTER
# ==================================================
st.markdown("---")

st.markdown(
    '<p class="note">MedTrack DV · Hospital Operations & '
    'Patient Analytics · Milestone 2</p>',
    unsafe_allow_html=True
)
