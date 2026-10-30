
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
AMBER = "#D6A84F"
TEXT = "#E5EDF7"
MUTED = "#93A8C2"

# ==================================================
# DARK THEME STYLING
# ==================================================
st.markdown("""
<style>
    :root {
        --navy: #0B1220;
        --sidebar: #080E19;
        --card: #111D30;
        --card-raised: #14243A;
        --border: #263951;
        --border-soft: rgba(96, 165, 250, 0.18);
        --text: #E5EDF7;
        --muted: #93A8C2;
        --blue: #60A5FA;
        --teal: #2D94D4;
    }

    .stApp {
        background:
            radial-gradient(circle at 85% -10%, rgba(45, 148, 212, 0.12), transparent 34rem),
            #0B1220;
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background-color: rgba(11, 18, 32, 0.88);
        border-bottom: 1px solid rgba(38, 57, 81, 0.55);
    }

    .block-container {
        max-width: 1450px;
        padding: 1.5rem 2rem 2.5rem 2rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080E19 0%, #0A1423 100%);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: #DCE7F5;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #B6C8DC;
    }

    .brand {
        font-size: 1.5rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.6px;
        padding-top: 0.25rem;
    }

    .brand-subtitle {
        color: var(--muted);
        font-size: 0.78rem;
        letter-spacing: 0.02em;
        margin: 0.25rem 0 1.5rem;
    }

    .hero {
        background:
            linear-gradient(115deg, rgba(17, 29, 48, 0.98), rgba(18, 59, 83, 0.94)),
            radial-gradient(circle at 95% 0%, rgba(96, 165, 250, 0.25), transparent 23rem);
        border: 1px solid #28435E;
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.16);
        margin-bottom: 1.35rem;
        overflow: hidden;
        padding: 1.45rem 1.7rem 1.5rem;
        position: relative;
    }

    .hero::after {
        background: linear-gradient(90deg, var(--teal), var(--blue));
        content: "";
        height: 3px;
        left: 0;
        position: absolute;
        right: 0;
        top: 0;
    }

    .hero h1 {
        color: #F8FAFC;
        font-size: clamp(1.55rem, 2.2vw, 2rem);
        font-weight: 780;
        letter-spacing: -0.04em;
        margin: 0;
        padding: 0;
    }

    .hero p {
        color: #B6C8DC;
        font-size: 0.9rem;
        line-height: 1.55;
        margin: 0.45rem 0 0;
        max-width: 760px;
    }

    .section-label {
        border-left: 3px solid var(--teal);
        color: #E5EDF7;
        font-size: 1.02rem;
        font-weight: 750;
        letter-spacing: -0.01em;
        margin: 1.45rem 0 0.7rem;
        padding: 0.1rem 0 0.1rem 0.7rem;
    }

    h1, h2, h3, p, label {
        color: var(--text);
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted);
        font-size: 0.78rem;
        line-height: 1.5;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #7890AD;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    [data-testid="stSidebar"] hr {
        border-color: rgba(38, 57, 81, 0.7);
        margin: 1.15rem 0;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > label {
        color: #7890AD;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        margin-bottom: 0.45rem;
        text-transform: uppercase;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > div {
        gap: 0.35rem;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: transparent;
        border: 1px solid transparent;
        border-radius: 9px;
        color: #AFC1D5;
        padding: 0.5rem 0.65rem;
        transition: background 120ms ease, border-color 120ms ease;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(96, 165, 250, 0.08);
        border-color: rgba(96, 165, 250, 0.16);
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(90deg, rgba(45, 148, 212, 0.2), rgba(96, 165, 250, 0.08));
        border-color: rgba(45, 148, 212, 0.45);
        color: #F1F7FF;
        font-weight: 700;
    }

    [data-testid="stSidebar"] [data-testid="stMultiSelect"] label {
        color: #AFC1D5;
        font-size: 0.78rem;
        font-weight: 650;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: rgba(17, 29, 48, 0.82);
        border-color: rgba(38, 57, 81, 0.95);
        border-radius: 8px;
    }

    [data-testid="stSidebar"] [data-testid="stButton"] button {
        background: rgba(45, 148, 212, 0.12);
        border: 1px solid rgba(45, 148, 212, 0.42);
        border-radius: 8px;
        color: #DCEBFA;
        font-weight: 700;
        min-height: 2.45rem;
    }

    [data-testid="stSidebar"] [data-testid="stButton"] button:hover {
        background: rgba(45, 148, 212, 0.23);
        border-color: var(--teal);
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(20, 36, 58, 0.98), rgba(17, 29, 48, 0.98));
        border: 1px solid var(--border);
        border-radius: 13px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.14);
        min-height: 104px;
        padding: 15px 16px;
        transition: border-color 120ms ease, transform 120ms ease;
    }

    [data-testid="stMetric"]:hover {
        border-color: rgba(96, 165, 250, 0.44);
        transform: translateY(-1px);
    }

    [data-testid="stMetricLabel"] {
        color: #A8BAD0;
        font-size: 0.76rem;
        font-weight: 650;
        letter-spacing: 0.01em;
    }

    [data-testid="stMetricValue"] {
        color: #F1F7FF;
        font-size: clamp(1.35rem, 2.2vw, 1.75rem);
        font-weight: 750;
        letter-spacing: -0.03em;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.78rem;
    }

    [data-testid="stTabs"] button {
        font-weight: 650;
        color: #B6C8DC;
    }

    div[data-testid="stPlotlyChart"] {
        background: rgba(17, 29, 48, 0.88);
        border: 1px solid var(--border);
        border-radius: 13px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        margin-bottom: 0.7rem;
        padding: 7px 8px 4px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-testid="stDownloadButton"] button {
        background: rgba(45, 148, 212, 0.12);
        border: 1px solid rgba(45, 148, 212, 0.42);
        border-radius: 8px;
        color: #DCEBFA;
        font-weight: 650;
    }

    .note {
        color: var(--muted);
        font-size: 0.82rem;
    }

    [data-testid="stAlert"] {
        background: rgba(17, 29, 48, 0.72);
        border: 1px solid rgba(96, 165, 250, 0.25);
        border-radius: 10px;
        color: #C9D8E9;
        margin: 0.55rem 0 0.8rem;
    }

    [data-testid="stSelectbox"] label,
    [data-testid="stTextInput"] label {
        color: #AFC1D5;
        font-size: 0.78rem;
        font-weight: 650;
    }

    [data-baseweb="select"] > div {
        background-color: rgba(17, 29, 48, 0.9);
        border-color: var(--border);
        border-radius: 8px;
    }

    hr {
        border-color: rgba(38, 57, 81, 0.75);
        margin: 1.6rem 0 1.15rem;
    }

    @media (max-width: 900px) {
        .block-container {
            padding: 1rem 1rem 2rem;
        }

        .hero {
            padding: 1.25rem 1.25rem 1.3rem;
        }
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
        title=dict(
            font=dict(size=15, color="#F1F7FF"),
            x=0.02,
            xanchor="left"
        ),
        legend_title_text="",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor="#172B46",
            bordercolor="#41617F",
            font=dict(color="#F1F7FF", size=12)
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#29394F",
        zerolinecolor="#29394F",
        linecolor="#3A506B",
        title_font=dict(color=MUTED, size=11),
        tickfont=dict(color="#A8BAD0", size=11)
    )

    fig.update_yaxes(
        showgrid=False,
        zerolinecolor="#29394F",
        linecolor="#3A506B",
        title_font=dict(color=MUTED, size=11),
        tickfont=dict(color="#A8BAD0", size=11)
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


def resource_utilization_metrics(data):
    numeric_columns = [
        "beds_allocated",
        "beds_occupied",
        "staff_allocated",
        "staff_on_duty",
        "equipment_allocated",
        "equipment_in_use"
    ]
    totals = {
        column: pd.to_numeric(data[column], errors="coerce").fillna(0).sum()
        for column in numeric_columns
        if column in data.columns
    }

    def percentage(numerator, denominator):
        return numerator / denominator * 100 if denominator > 0 else None

    return {
        **totals,
        "bed_rate": percentage(
            totals.get("beds_occupied", 0),
            totals.get("beds_allocated", 0)
        ),
        "staff_rate": percentage(
            totals.get("staff_on_duty", 0),
            totals.get("staff_allocated", 0)
        ),
        "equipment_rate": percentage(
            totals.get("equipment_in_use", 0),
            totals.get("equipment_allocated", 0)
        )
    }


def format_rate(value):
    return f"{value:.2f}%" if value is not None else "N/A"


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

    st.caption("MILESTONE 3 · HOSPITAL INTELLIGENCE")


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
        "Monitor beds, staff, equipment, and dated allocation activity."
    )

    resource_view = resources.copy()

    filter_columns = st.columns(3)
    with filter_columns[0]:
        selected_bed_types = st.multiselect(
            "Bed type",
            sorted(resource_view["bed_type"].dropna().unique()),
            default=sorted(resource_view["bed_type"].dropna().unique())
        )
    with filter_columns[1]:
        selected_staff_types = st.multiselect(
            "Staff type",
            sorted(resource_view["staff_type"].dropna().unique()),
            default=sorted(resource_view["staff_type"].dropna().unique())
        )
    with filter_columns[2]:
        selected_equipment_types = st.multiselect(
            "Equipment type",
            sorted(resource_view["equipment_type"].dropna().unique()),
            default=sorted(resource_view["equipment_type"].dropna().unique())
        )

    resource_view = resource_view[
        resource_view["bed_type"].isin(selected_bed_types)
        & resource_view["staff_type"].isin(selected_staff_types)
        & resource_view["equipment_type"].isin(selected_equipment_types)
    ].copy()

    metrics = resource_utilization_metrics(resource_view)

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric("Beds Allocated", f"{metrics.get('beds_allocated', 0):,.0f}")
    c2.metric("Beds Occupied", f"{metrics.get('beds_occupied', 0):,.0f}")
    c3.metric("Bed Occupancy", format_rate(metrics["bed_rate"]))
    c4.metric("Staff On-Duty Rate", format_rate(metrics["staff_rate"]))
    c5.metric(
        "Equipment In Use",
        f"{metrics.get('equipment_in_use', 0):,.0f}"
    )
    c6.metric("Equipment Utilization", format_rate(metrics["equipment_rate"]))

    if resource_view.empty:
        st.warning("No resource records match the selected filters.")
    else:
        st.caption(
            f"Showing {len(resource_view):,} of {len(resources):,} resource "
            "allocation records."
        )

        st.markdown(
            '<div class="section-label">Bed Utilization</div>',
            unsafe_allow_html=True
        )

        left, right = st.columns(2, gap="medium")

        with left:
            bed_summary = (
                resource_view.groupby("bed_type", as_index=False)
                [["beds_allocated", "beds_occupied"]]
                .sum()
                .sort_values("beds_allocated", ascending=True)
            )
            bed_long = bed_summary.melt(
                id_vars="bed_type",
                value_vars=["beds_allocated", "beds_occupied"],
                var_name="Bed Status",
                value_name="Beds"
            )
            bed_long["Bed Status"] = bed_long["Bed Status"].map({
                "beds_allocated": "Allocated",
                "beds_occupied": "Occupied"
            })

            fig = px.bar(
                bed_long,
                x="Beds",
                y="bed_type",
                color="Bed Status",
                orientation="h",
                barmode="group",
                title="Bed Allocation and Occupancy by Bed Type",
                labels={"bed_type": "Bed type"},
                color_discrete_map={"Allocated": BLUE, "Occupied": TEAL}
            )
            st.plotly_chart(
                chart_layout(fig, max(300, len(bed_summary) * 55)),
                use_container_width=True
            )

        with right:
            if "hospital_name" in resource_view.columns:
                hospital_summary = (
                    resource_view.groupby("hospital_name", as_index=False)
                    [["beds_allocated", "beds_occupied"]]
                    .sum()
                    .sort_values("beds_allocated", ascending=False)
                    .head(10)
                    .sort_values("beds_allocated", ascending=True)
                )

                hospital_long = hospital_summary.melt(
                    id_vars="hospital_name",
                    value_vars=["beds_allocated", "beds_occupied"],
                    var_name="Bed Status",
                    value_name="Beds"
                )
                hospital_long["Bed Status"] = hospital_long["Bed Status"].map({
                    "beds_allocated": "Allocated",
                    "beds_occupied": "Occupied"
                })
                fig = px.bar(
                    hospital_long,
                    x="Beds",
                    y="hospital_name",
                    color="Bed Status",
                    orientation="h",
                    barmode="group",
                    title="Top 10 Hospitals by Allocated Beds",
                    labels={"hospital_name": "Hospital"},
                    color_discrete_map={"Allocated": BLUE, "Occupied": TEAL}
                )
                st.plotly_chart(
                    chart_layout(fig, 420),
                    use_container_width=True
                )

        st.markdown(
            '<div class="section-label">Staff and Equipment Allocation</div>',
            unsafe_allow_html=True
        )

        left, right = st.columns(2, gap="medium")

        with left:
            staffing = (
                resource_view.groupby("staff_type", as_index=False)
                [["staff_allocated", "staff_on_duty"]]
                .sum()
                .melt(
                    id_vars="staff_type",
                    var_name="Staff Status",
                    value_name="Staff"
                )
            )
            staffing["Staff Status"] = staffing["Staff Status"].map({
                "staff_allocated": "Allocated",
                "staff_on_duty": "On Duty"
            })
            fig = px.bar(
                staffing,
                x="staff_type",
                y="Staff",
                color="Staff Status",
                barmode="group",
                title="Staff Allocation and On-Duty Counts",
                labels={"staff_type": "Staff type"},
                color_discrete_map={"Allocated": BLUE, "On Duty": TEAL}
            )
            st.plotly_chart(
                chart_layout(fig, 340),
                use_container_width=True
            )

        with right:
            equipment = (
                resource_view.groupby("equipment_type", as_index=False)
                [["equipment_allocated", "equipment_in_use"]]
                .sum()
                .melt(
                    id_vars="equipment_type",
                    var_name="Equipment Status",
                    value_name="Equipment"
                )
            )
            equipment["Equipment Status"] = equipment["Equipment Status"].map({
                "equipment_allocated": "Allocated",
                "equipment_in_use": "In Use"
            })
            fig = px.bar(
                equipment,
                x="equipment_type",
                y="Equipment",
                color="Equipment Status",
                barmode="group",
                title="Equipment Allocation and Utilization",
                labels={"equipment_type": "Equipment type"},
                color_discrete_map={"Allocated": BLUE, "In Use": TEAL}
            )
            st.plotly_chart(
                chart_layout(fig, 340),
                use_container_width=True
            )

        st.markdown(
            '<div class="section-label">Resource Allocation Trends</div>',
            unsafe_allow_html=True
        )
        trend = resource_view.copy()
        trend["allocation_date"] = pd.to_datetime(
            trend["allocation_date"],
            errors="coerce"
        )
        trend = trend.dropna(subset=["allocation_date"])
        if trend.empty:
            st.info("No valid allocation dates are available for trend analysis.")
        else:
            trend["Month"] = trend["allocation_date"].dt.to_period("M").astype(str)
            monthly = (
                trend.groupby("Month", as_index=False)
                [["beds_allocated", "beds_occupied", "equipment_allocated",
                  "equipment_in_use"]]
                .sum()
            )
            monthly_long = monthly.melt(
                id_vars="Month",
                var_name="Measure",
                value_name="Count"
            )
            monthly_long["Measure"] = monthly_long["Measure"].map({
                "beds_allocated": "Beds allocated",
                "beds_occupied": "Beds occupied",
                "equipment_allocated": "Equipment allocated",
                "equipment_in_use": "Equipment in use"
            })
            fig = px.line(
                monthly_long,
                x="Month",
                y="Count",
                color="Measure",
                markers=True,
                title="Monthly Resource Allocation Records",
                labels={"Month": "Allocation month", "Count": "Count"}
            )
            st.plotly_chart(
                chart_layout(fig, 350),
                use_container_width=True
            )
            st.caption(
                "These are monthly sums of resource allocation records, not "
                "patient admissions, discharges, or daily census values. "
                "Because the records are aggregated, they should not "
                "automatically be interpreted as unique hospital-wide totals."
            )

        st.markdown(
            '<div class="section-label">Availability Insights</div>',
            unsafe_allow_html=True
        )
        availability = pd.DataFrame({
            "Resource": ["Beds", "Staff", "Equipment"],
            "Available / Not in use": [
                metrics.get("beds_allocated", 0) - metrics.get("beds_occupied", 0),
                metrics.get("staff_allocated", 0) - metrics.get("staff_on_duty", 0),
                metrics.get("equipment_allocated", 0) - metrics.get("equipment_in_use", 0)
            ]
        })
        fig = px.bar(
            availability,
            x="Resource",
            y="Available / Not in use",
            text="Available / Not in use",
            color="Resource",
            title="Resource Capacity Not Currently in Use",
            color_discrete_sequence=[BLUE, TEAL, AMBER]
        )
        fig.update_layout(showlegend=False)
        fig.update_traces(textposition="outside")
        st.plotly_chart(
            chart_layout(fig, 290),
            use_container_width=True
        )

        surge_count = int(resource_view["surge_status"].eq(True).sum())
        st.info(
            f"Surge status is active in {surge_count:,} of "
            f"{len(resource_view):,} selected allocation records. "
            "This is a resource-record indicator, not a patient census measure."
        )
        st.caption(
            "Missing numeric resource values are treated as zero in aggregate "
            "calculations."
        )

    st.caption(
        "Resource metrics are aggregated across allocation records. "
        "They should not be interpreted as unique hospital-wide totals "
        "without a confirmed snapshot grain."
    )

    st.markdown(
        '<div class="section-label">Department Analytics Availability</div>',
        unsafe_allow_html=True
    )
    st.info(
        "Department-level analysis is not available in the validated datasets. "
        "There is no reliable department field linking patients to departments "
        "or resources to departments, so department volume, readmission, "
        "efficiency, and capacity comparisons are intentionally not generated."
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
    'Patient Analytics · Milestone 3</p>',
    unsafe_allow_html=True
)
