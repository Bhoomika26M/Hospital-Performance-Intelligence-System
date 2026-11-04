import re
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Department Analytics | MedTrack",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
READMISSION_FILE = (
    BASE_DIR / "milestone3_data" / "synthetic_patient_readmissions.csv"
)
OCCUPANCY_FILE = BASE_DIR / "milestone3_data" / "daily_occupancy.csv"

READMISSION_COLUMNS = (
    "admission_date",
    "hospital",
    "department",
    "readmission_flag",
)
OCCUPANCY_COLUMNS = (
    "date",
    "hospital",
    "department",
    "total_beds",
    "occupied_beds",
    "available_beds",
)


@st.cache_data
def load_patient_data():
    patients = pd.read_csv(BASE_DIR / "hospital_cleaned.csv")
    patients.columns = (
        patients.columns.str.strip().str.lower().str.replace(" ", "_")
    )
    for column in ("date_of_admission", "discharge_date"):
        if column in patients.columns:
            patients[column] = pd.to_datetime(
                patients[column], errors="coerce"
            )
    for column in ("length_of_stay", "billing_amount"):
        if column in patients.columns:
            patients[column] = pd.to_numeric(
                patients[column], errors="coerce"
            )
    if "department" not in patients.columns and "medical_condition" in patients:
        department_mapping = {
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
            .map(department_mapping)
            .fillna("Other")
        )
    return patients


@st.cache_data
def load_supplementary_data(
    file_path: str,
    modified_time: float | None,
    expected_columns: tuple[str, ...],
):
    if modified_time is None:
        return pd.DataFrame(columns=expected_columns)
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")
    return data


def file_modified_time(file_path: Path):
    return file_path.stat().st_mtime if file_path.is_file() else None


def filter_data(
    data: pd.DataFrame,
    date_column: str,
    date_range,
    departments: list[str],
    hospital_search: str,
):
    result = data.copy()
    if "department" in result.columns:
        result = result[result["department"].isin(departments)]
    if hospital_search and "hospital" in result.columns:
        result = result[
            result["hospital"].astype("string").str.contains(
                re.escape(hospital_search),
                case=False,
                na=False,
                regex=True,
            )
        ]
    if date_range and date_column in result.columns:
        start_date, end_date = date_range
        result = result[
            result[date_column].notna()
            & result[date_column].dt.date.between(start_date, end_date)
        ]
    return result


def style_figure(figure, x_title: str, y_title: str, legend_title: str = ""):
    figure.update_layout(
        template="plotly_dark",
        margin=dict(l=20, r=20, t=65, b=20),
        xaxis_title=x_title,
        yaxis_title=y_title,
        legend_title_text=legend_title,
        hoverlabel=dict(namelength=-1),
    )
    return figure


def show_figure(figure, empty_message: str):
    if figure is None:
        st.info(empty_message)
    else:
        st.plotly_chart(
            figure,
            width="stretch",
            config={"displayModeBar": False},
        )


def min_max_score(values: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce")
    minimum = numeric.min()
    maximum = numeric.max()
    if pd.isna(minimum) or pd.isna(maximum):
        return pd.Series(np.nan, index=values.index, dtype="float64")
    if maximum == minimum:
        return pd.Series(50.0, index=values.index, dtype="float64")
    return (numeric - minimum) / (maximum - minimum) * 100


try:
    patients = load_patient_data()
except FileNotFoundError:
    st.error("hospital_cleaned.csv was not found in the project folder.")
    st.stop()

readmissions = load_supplementary_data(
    str(READMISSION_FILE),
    file_modified_time(READMISSION_FILE),
    READMISSION_COLUMNS,
)
occupancy = load_supplementary_data(
    str(OCCUPANCY_FILE),
    file_modified_time(OCCUPANCY_FILE),
    OCCUPANCY_COLUMNS,
)

required_patient_columns = {
    "date_of_admission",
    "department",
    "hospital",
    "length_of_stay",
    "billing_amount",
}
missing_patient_columns = required_patient_columns - set(patients.columns)
if missing_patient_columns:
    st.error(
        "hospital_cleaned.csv is missing required columns: "
        + ", ".join(sorted(missing_patient_columns))
    )
    st.stop()

for data, expected, label in (
    (readmissions, READMISSION_COLUMNS, "readmission"),
    (occupancy, OCCUPANCY_COLUMNS, "occupancy"),
):
    missing_columns = set(expected) - set(data.columns)
    if missing_columns:
        st.warning(
            f"Synthetic {label} data is missing columns: "
            + ", ".join(sorted(missing_columns))
        )
        if label == "readmission":
            readmissions = pd.DataFrame(columns=READMISSION_COLUMNS)
        else:
            occupancy = pd.DataFrame(columns=OCCUPANCY_COLUMNS)

for data, date_column, numeric_columns in (
    (readmissions, "admission_date", ("readmission_flag",)),
    (
        occupancy,
        "date",
        ("total_beds", "occupied_beds", "available_beds"),
    ),
):
    if date_column in data.columns:
        data[date_column] = pd.to_datetime(data[date_column], errors="coerce")
    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")

if not READMISSION_FILE.is_file():
    st.warning(
        "Synthetic readmission data is unavailable: "
        "milestone3_data/synthetic_patient_readmissions.csv was not found."
    )
if not OCCUPANCY_FILE.is_file():
    st.warning(
        "Synthetic occupancy data is unavailable: "
        "milestone3_data/daily_occupancy.csv was not found."
    )

st.sidebar.title("🏥 MedTrack")
st.sidebar.caption("Department Analytics")
st.sidebar.divider()
st.sidebar.subheader("Dashboard Filters")

date_series = [
    patients["date_of_admission"].dropna(),
    readmissions["admission_date"].dropna()
    if "admission_date" in readmissions.columns
    else pd.Series(dtype="datetime64[ns]"),
    occupancy["date"].dropna()
    if "date" in occupancy.columns
    else pd.Series(dtype="datetime64[ns]"),
]
available_dates = pd.concat(date_series, ignore_index=True).dropna()
date_range = None
if not available_dates.empty:
    earliest = available_dates.min().date()
    latest = available_dates.max().date()
    date_value = st.sidebar.date_input(
        "Admission / Snapshot Date Range",
        value=(earliest, latest),
        min_value=earliest,
        max_value=latest,
    )
    if isinstance(date_value, (tuple, list)) and len(date_value) == 2:
        date_range = (date_value[0], date_value[1])

department_values = set(patients["department"].dropna().astype(str))
for data in (readmissions, occupancy):
    if "department" in data.columns:
        department_values.update(data["department"].dropna().astype(str))
department_options = sorted(department_values)
selected_departments = st.sidebar.multiselect(
    "Department",
    department_options,
    default=department_options,
)
hospital_search = st.sidebar.text_input(
    "Hospital name contains",
    help=(
        "Search by exact name or a case-insensitive text fragment. "
        "The same text is applied independently to each dataset."
    ),
).strip()

filtered_patients = filter_data(
    patients,
    "date_of_admission",
    date_range,
    selected_departments,
    hospital_search,
)
filtered_readmissions = filter_data(
    readmissions,
    "admission_date",
    date_range,
    selected_departments,
    hospital_search,
)
filtered_occupancy = filter_data(
    occupancy,
    "date",
    date_range,
    selected_departments,
    hospital_search,
)

valid_occupancy = filtered_occupancy.dropna(
    subset=["total_beds", "occupied_beds", "available_beds"]
).copy()
valid_occupancy = valid_occupancy[
    (valid_occupancy["total_beds"] > 0)
    & (valid_occupancy["occupied_beds"] >= 0)
    & (valid_occupancy["available_beds"] >= 0)
    & (
        valid_occupancy["total_beds"]
        == valid_occupancy["occupied_beds"]
        + valid_occupancy["available_beds"]
    )
]
if len(valid_occupancy) < len(filtered_occupancy):
    st.warning(
        "Synthetic occupancy rows with missing or inconsistent bed counts "
        "are excluded from the capacity analysis."
    )

st.title("📊 Department Analytics")
st.markdown(
    "Compare source-data department performance with separately filtered "
    "synthetic readmission and bed-capacity demonstrations."
)
st.divider()

st.subheader("Department Performance — Source Patient Data")
total_admissions = len(filtered_patients)
average_stay = filtered_patients["length_of_stay"].mean()
average_billing = filtered_patients["billing_amount"].mean()
department_count = filtered_patients["department"].nunique()
metric_columns = st.columns(4)
metric_columns[0].metric("Admissions", f"{total_admissions:,}")
metric_columns[1].metric("Departments", f"{department_count:,}")
metric_columns[2].metric(
    "Average Length of Stay",
    f"{average_stay:.1f} days" if pd.notna(average_stay) else "N/A",
)
metric_columns[3].metric(
    "Average Billing",
    f"₹{average_billing:,.2f}" if pd.notna(average_billing) else "N/A",
)

department_summary = (
    filtered_patients.groupby("department", as_index=False)
    .agg(
        total_admissions=("department", "size"),
        average_length_of_stay=("length_of_stay", "mean"),
        average_billing=("billing_amount", "mean"),
    )
)
if "doctor" in filtered_patients.columns:
    doctor_summary = (
        filtered_patients.groupby("department")["doctor"]
        .nunique()
        .rename("unique_doctors")
        .reset_index()
    )
    department_summary = department_summary.merge(
        doctor_summary, on="department", how="left"
    )
    department_summary["admissions_per_listed_doctor"] = (
        department_summary["total_admissions"]
        / department_summary["unique_doctors"].replace(0, np.nan)
    )

left, right = st.columns(2)
with left:
    st.subheader("Patient Volume by Department")
    if department_summary.empty:
        show_figure(None, "No patient admissions match the selected filters.")
    else:
        volume = department_summary.sort_values(
            "total_admissions", ascending=True
        )
        figure = px.bar(
            volume,
            x="total_admissions",
            y="department",
            orientation="h",
            title="Admission Records by Department",
            labels={
                "department": "Department",
                "total_admissions": "Admission Records",
            },
            text="total_admissions",
        )
        figure.update_traces(textposition="outside", cliponaxis=False)
        show_figure(
            style_figure(figure, "Admission Records", "Department"),
            "No department admission volume is available.",
        )

with right:
    st.subheader("Department Share of Admissions")
    if department_summary.empty:
        show_figure(None, "No patient admissions match the selected filters.")
    else:
        figure = px.pie(
            department_summary,
            names="department",
            values="total_admissions",
            hole=0.5,
            title="Share of Admission Records",
            labels={
                "department": "Department",
                "total_admissions": "Admission Records",
            },
        )
        figure.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate=(
                "<b>%{label}</b><br>Admission records: %{value:,}"
                "<br>Share: %{percent}<extra></extra>"
            ),
        )
        show_figure(
            style_figure(figure, "", "Admission Records", "Department"),
            "No department share is available.",
        )

st.subheader("Department Performance Comparison")
if department_summary.empty:
    st.info("No department performance data matches the selected filters.")
else:
    performance_long = department_summary.melt(
        id_vars="department",
        value_vars=[
            "total_admissions",
            "average_length_of_stay",
            "average_billing",
        ],
        var_name="metric",
        value_name="value",
    )
    performance_long["metric"] = performance_long["metric"].map(
        {
            "total_admissions": "Admissions",
            "average_length_of_stay": "Average Stay (Days)",
            "average_billing": "Average Billing",
        }
    )
    figure = px.bar(
        performance_long,
        x="department",
        y="value",
        color="metric",
        barmode="group",
        title="Admissions, Average Stay, and Average Billing",
        labels={
            "department": "Department",
            "value": "Metric Value (different units)",
            "metric": "Metric",
        },
        hover_data={"value": ":,.2f"},
    )
    show_figure(
        style_figure(figure, "Department", "Metric Value", "Metric"),
        "No department performance comparison is available.",
    )
    st.caption(
        "The grouped comparison shares an axis for metrics with different "
        "units; use the department summary table for exact values."
    )

left, right = st.columns(2)
with left:
    st.subheader("Admission Mix by Department")
    if filtered_patients.empty or "admission_type" not in filtered_patients:
        show_figure(None, "No admission-type data matches the filters.")
    else:
        admission_mix = (
            filtered_patients.groupby(
                ["department", "admission_type"], as_index=False
            )
            .size()
            .rename(columns={"size": "admissions"})
        )
        figure = px.bar(
            admission_mix,
            x="department",
            y="admissions",
            color="admission_type",
            barmode="group",
            title="Admission Records by Department and Type",
            labels={
                "department": "Department",
                "admissions": "Admission Records",
                "admission_type": "Admission Type",
            },
        )
        show_figure(
            style_figure(figure, "Department", "Admission Records", "Type"),
            "No admission mix is available.",
        )

with right:
    st.subheader("Medical Conditions by Department")
    if filtered_patients.empty or "medical_condition" not in filtered_patients:
        show_figure(None, "No condition data matches the filters.")
    else:
        condition_mix = (
            filtered_patients.groupby(
                ["department", "medical_condition"], as_index=False
            )
            .size()
            .rename(columns={"size": "admissions"})
        )
        figure = px.bar(
            condition_mix,
            x="department",
            y="admissions",
            color="medical_condition",
            barmode="stack",
            title="Admission Records by Department and Condition",
            labels={
                "department": "Department",
                "admissions": "Admission Records",
                "medical_condition": "Medical Condition",
            },
        )
        show_figure(
            style_figure(
                figure, "Department", "Admission Records", "Condition"
            ),
            "No condition distribution is available.",
        )

st.header("Readmission by Department (Synthetic)")
st.caption(
    "Synthetic demonstration only. These admissions are not linked to the "
    "original patient dataset. Rate = flagged synthetic admissions divided "
    "by all synthetic admissions in the selected cohort."
)
readmission_flags = filtered_readmissions.get(
    "readmission_flag", pd.Series(dtype="float64")
)
valid_flags = readmission_flags.dropna()
readmission_data_valid = (
    not filtered_readmissions.empty
    and len(valid_flags) == len(filtered_readmissions)
    and valid_flags.isin([0, 1]).all()
)
if not filtered_readmissions.empty and not readmission_data_valid:
    st.warning(
        "Synthetic readmission results are unavailable because the selected "
        "cohort has missing or invalid readmission flags."
    )
if not readmission_data_valid:
    st.info("No valid synthetic readmissions match the selected filters.")
else:
    readmission_by_department = (
        filtered_readmissions.groupby("department", as_index=False)
        .agg(
            synthetic_admissions=("readmission_flag", "size"),
            readmission_count=("readmission_flag", "sum"),
        )
    )
    readmission_by_department["readmission_rate"] = (
        readmission_by_department["readmission_count"]
        / readmission_by_department["synthetic_admissions"]
        * 100
    )
    readmission_kpis = st.columns(3)
    readmission_kpis[0].metric(
        "Synthetic Admissions", f"{len(filtered_readmissions):,}"
    )
    readmission_kpis[1].metric(
        "Synthetic Readmission Count",
        f"{int(valid_flags.sum()):,}",
    )
    readmission_kpis[2].metric(
        "Overall Synthetic Readmission Rate",
        f"{valid_flags.mean():.1%}",
    )
    figure = px.bar(
        readmission_by_department.sort_values(
            "readmission_rate", ascending=True
        ),
        x="readmission_rate",
        y="department",
        orientation="h",
        color="readmission_rate",
        color_continuous_scale="Teal",
        title="Synthetic Readmission Rate by Department",
        labels={
            "department": "Department",
            "readmission_rate": "Readmission Rate (%)",
            "synthetic_admissions": "Synthetic Admissions",
            "readmission_count": "Flagged Admissions",
        },
        text="readmission_rate",
        custom_data=["readmission_count", "synthetic_admissions"],
    )
    figure.update_traces(
        texttemplate="%{x:.1f}%",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>Rate: %{x:.2f}%"
            "<br>Flagged: %{customdata[0]:,.0f}"
            "<br>Synthetic admission denominator: %{customdata[1]:,.0f}"
            "<extra></extra>"
        ),
    )
    figure.update_xaxes(ticksuffix="%", rangemode="tozero")
    show_figure(
        style_figure(
            figure, "Synthetic Readmission Rate (%)", "Department"
        ),
        "No synthetic department readmission data is available.",
    )

st.header("Department Efficiency Comparison")
st.caption(
    "This provisional analytical score combines min-max scaled admissions "
    "per listed doctor and inverse min-max scaled average length of stay, "
    "then averages the two scores. It is not clinically validated. Listed "
    "doctor names are not staffing allocation or measured workload."
)
if (
    not department_summary.empty
    and "admissions_per_listed_doctor" in department_summary.columns
):
    department_summary["admissions_score"] = min_max_score(
        department_summary["admissions_per_listed_doctor"]
    )
    department_summary["stay_score"] = (
        100
        - min_max_score(department_summary["average_length_of_stay"])
    )
    department_summary["department_efficiency_score"] = (
        (
            department_summary["admissions_score"]
            + department_summary["stay_score"]
        )
        / 2
    )
    efficiency_data = department_summary.dropna(
        subset=["department_efficiency_score"]
    )
    if efficiency_data.empty:
        st.info("No department efficiency scores can be calculated.")
    else:
        figure = px.scatter(
            efficiency_data,
            x="average_length_of_stay",
            y="average_billing",
            size="total_admissions",
            color="department_efficiency_score",
            hover_name="department",
            color_continuous_scale="Viridis",
            title="Department Stay, Billing, Volume, and Provisional Score",
            labels={
                "average_length_of_stay": "Average Stay (Days)",
                "average_billing": "Average Billing",
                "total_admissions": "Admission Records",
                "department_efficiency_score": "Provisional Score",
            },
            custom_data=["total_admissions"],
        )
        figure.update_traces(
            hovertemplate=(
                "<b>%{hovertext}</b><br>Average stay: %{x:.2f} days"
                "<br>Average billing: %{y:,.2f}"
                "<br>Admissions: %{customdata[0]:,.0f}"
                "<br>Provisional score: %{marker.color:.1f}"
                "<extra></extra>"
            )
        )
        show_figure(
            style_figure(
                figure,
                "Average Length of Stay (Days)",
                "Average Billing",
                "Provisional Score",
            ),
            "No efficiency comparison is available.",
        )
        score_data = efficiency_data[
            ["department", "department_efficiency_score"]
        ].sort_values("department_efficiency_score", ascending=False)
        st.dataframe(
            score_data.round(2),
            width="stretch",
            hide_index=True,
        )
else:
    st.info(
        "A provisional score cannot be calculated without listed doctor data."
    )

st.header("Treatment Capacity (Synthetic Occupancy)")
st.caption(
    "Synthetic demonstration data only. It is not actual hospital bed "
    "capacity or patient census and is not linked to source patient records."
)
if valid_occupancy.empty:
    st.info("No valid synthetic occupancy observations match the filters.")
else:
    occupied_total = valid_occupancy["occupied_beds"].sum()
    capacity_total = valid_occupancy["total_beds"].sum()
    weighted_occupancy = (
        occupied_total / capacity_total if capacity_total > 0 else np.nan
    )
    occupancy_metrics = st.columns(2)
    occupancy_metrics[0].metric(
        "Weighted Bed Occupancy Rate (Synthetic)",
        f"{weighted_occupancy:.1%}"
        if pd.notna(weighted_occupancy)
        else "N/A",
    )
    occupancy_metrics[1].metric(
        "Synthetic Occupancy Observations",
        f"{len(valid_occupancy):,}",
    )

    capacity_by_department = (
        valid_occupancy.groupby("department", as_index=False)
        .agg(
            occupied_beds=("occupied_beds", "mean"),
            available_beds=("available_beds", "mean"),
            total_beds=("total_beds", "mean"),
            occupied_bed_days=("occupied_beds", "sum"),
            bed_days=("total_beds", "sum"),
            observations=("date", "size"),
        )
    )
    capacity_by_department["occupancy_rate"] = (
        capacity_by_department["occupied_bed_days"]
        / capacity_by_department["bed_days"]
        * 100
    )
    left, right = st.columns(2)
    with left:
        st.subheader("Average Daily Beds by Department")
        capacity_long = capacity_by_department.melt(
            id_vars="department",
            value_vars=["occupied_beds", "available_beds"],
            var_name="bed_status",
            value_name="average_beds",
        )
        capacity_long["bed_status"] = capacity_long["bed_status"].map(
            {"occupied_beds": "Occupied", "available_beds": "Available"}
        )
        figure = px.bar(
            capacity_long,
            x="average_beds",
            y="department",
            color="bed_status",
            barmode="group",
            orientation="h",
            title="Average Occupied and Available Beds per Snapshot",
            labels={
                "department": "Department",
                "average_beds": "Average Beds per Snapshot",
                "bed_status": "Bed Status",
            },
        )
        show_figure(
            style_figure(
                figure, "Average Beds per Snapshot", "Department", "Bed Status"
            ),
            "No department capacity data is available.",
        )
    with right:
        st.subheader("Weighted Occupancy by Department")
        capacity_sorted = capacity_by_department.sort_values(
            "occupancy_rate", ascending=True
        )
        figure = px.bar(
            capacity_sorted,
            x="occupancy_rate",
            y="department",
            orientation="h",
            color="occupancy_rate",
            color_continuous_scale="Teal",
            title="Weighted Synthetic Occupancy Rate",
            labels={
                "department": "Department",
                "occupancy_rate": "Occupancy Rate (%)",
                "total_beds": "Bed Capacity per Snapshot",
                "observations": "Snapshots",
            },
            text="occupancy_rate",
            custom_data=["total_beds", "observations"],
        )
        figure.update_traces(
            texttemplate="%{x:.1f}%",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b><br>Weighted occupancy: %{x:.2f}%"
                "<br>Average capacity per snapshot: %{customdata[0]:,.1f}"
                "<br>Snapshots: %{customdata[1]:,.0f}<extra></extra>"
            ),
        )
        figure.update_xaxes(ticksuffix="%", rangemode="tozero")
        show_figure(
            style_figure(figure, "Occupancy Rate (%)", "Department"),
            "No department occupancy rates are available.",
        )

    st.subheader("Monthly Occupancy by Department (Synthetic)")
    monthly_occupancy = (
        valid_occupancy.assign(
            month=valid_occupancy["date"].dt.to_period("M").dt.to_timestamp()
        )
        .groupby(["month", "department"], as_index=False)
        .agg(
            occupied_beds=("occupied_beds", "sum"),
            total_beds=("total_beds", "sum"),
        )
    )
    monthly_occupancy["occupancy_rate"] = (
        monthly_occupancy["occupied_beds"]
        / monthly_occupancy["total_beds"]
        * 100
    )
    if monthly_occupancy.empty:
        show_figure(None, "No monthly occupancy observations are available.")
    else:
        heatmap_data = monthly_occupancy.pivot(
            index="department",
            columns="month",
            values="occupancy_rate",
        )
        figure = px.imshow(
            heatmap_data,
            aspect="auto",
            color_continuous_scale="Teal",
            title="Weighted Monthly Occupancy Rate by Department",
            labels={
                "x": "Month",
                "y": "Department",
                "color": "Occupancy (%)",
            },
        )
        figure.update_coloraxes(colorbar_ticksuffix="%")
        show_figure(
            style_figure(figure, "Month", "Department", "Occupancy"),
            "No monthly occupancy heatmap is available.",
        )
        peak_month = monthly_occupancy.loc[
            monthly_occupancy["occupancy_rate"].idxmax()
        ]
        st.caption(
            f"Highest filtered synthetic occupancy: "
            f"{peak_month['department']} in {peak_month['month']:%B %Y} "
            f"({peak_month['occupancy_rate']:.1f}%)."
        )

st.subheader("Detailed Department Summary — Source Patient Data")
if department_summary.empty:
    st.info("No department summary matches the selected filters.")
else:
    display_columns = [
        column
        for column in (
            "department",
            "total_admissions",
            "average_length_of_stay",
            "average_billing",
            "unique_doctors",
            "admissions_per_listed_doctor",
            "department_efficiency_score",
        )
        if column in department_summary.columns
    ]
    summary = department_summary[display_columns].round(2)
    st.dataframe(summary, width="stretch", hide_index=True)
    st.download_button(
        "Download Department Analytics",
        data=summary.to_csv(index=False).encode("utf-8"),
        file_name="department_analytics.csv",
        mime="text/csv",
    )

st.divider()
st.caption("MedTrack | Department Analytics")
