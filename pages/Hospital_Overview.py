import re
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Hospital Overview | MedTrack",
    page_icon="🏥",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
OCCUPANCY_FILE = BASE_DIR / "milestone3_data" / "daily_occupancy.csv"
READMISSIONS_FILE = (
    BASE_DIR / "milestone3_data" / "synthetic_patient_readmissions.csv"
)

OCCUPANCY_COLUMNS = (
    "date",
    "hospital",
    "department",
    "total_beds",
    "occupied_beds",
    "available_beds",
    "occupancy_rate",
)
READMISSION_COLUMNS = (
    "patient_id",
    "admission_id",
    "admission_date",
    "discharge_date",
    "hospital",
    "department",
    "previous_admission_date",
    "days_since_previous_discharge",
    "readmission_flag",
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

    for column in ("billing_amount", "length_of_stay"):
        if column in patients.columns:
            patients[column] = pd.to_numeric(
                patients[column], errors="coerce"
            )

    if "department" not in patients.columns:
        department_mapping = {
            "Cancer": "Oncology",
            "Obesity": "General Medicine",
            "Diabetes": "Endocrinology",
            "Asthma": "Pulmonology",
            "Hypertension": "Cardiology",
            "Arthritis": "Rheumatology",
        }
        if "medical_condition" in patients.columns:
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


def apply_filters(
    data: pd.DataFrame,
    date_column: str,
    date_range,
    selected_departments: list[str],
    hospital_search: str,
):
    filtered_data = data.copy()

    if "department" in filtered_data.columns:
        filtered_data = filtered_data[
            filtered_data["department"].isin(selected_departments)
        ]

    if hospital_search and "hospital" in filtered_data.columns:
        filtered_data = filtered_data[
            filtered_data["hospital"].astype("string").str.contains(
                re.escape(hospital_search),
                case=False,
                na=False,
                regex=True,
            )
        ]

    if date_range and date_column in filtered_data.columns:
        start_date, end_date = date_range
        filtered_data = filtered_data[
            filtered_data[date_column].notna()
            & filtered_data[date_column].dt.date.between(
                start_date, end_date
            )
        ]

    return filtered_data


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


try:
    patients = load_patient_data()
except FileNotFoundError:
    st.error("hospital_cleaned.csv was not found in the project folder.")
    st.stop()

occupancy = load_supplementary_data(
    str(OCCUPANCY_FILE),
    file_modified_time(OCCUPANCY_FILE),
    OCCUPANCY_COLUMNS,
)
readmissions = load_supplementary_data(
    str(READMISSIONS_FILE),
    file_modified_time(READMISSIONS_FILE),
    READMISSION_COLUMNS,
)

required_patient_columns = {
    "date_of_admission",
    "department",
    "hospital",
    "medical_condition",
    "admission_type",
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

missing_occupancy_columns = set(OCCUPANCY_COLUMNS) - set(occupancy.columns)
if missing_occupancy_columns:
    st.warning(
        "Synthetic occupancy data is unavailable because its CSV is missing "
        "columns: "
        + ", ".join(sorted(missing_occupancy_columns))
    )
    occupancy = pd.DataFrame(columns=OCCUPANCY_COLUMNS)

missing_readmission_columns = (
    set(READMISSION_COLUMNS) - set(readmissions.columns)
)
if missing_readmission_columns:
    st.warning(
        "Synthetic readmission data is unavailable because its CSV is "
        "missing columns: "
        + ", ".join(sorted(missing_readmission_columns))
    )
    readmissions = pd.DataFrame(columns=READMISSION_COLUMNS)

for data, date_columns, numeric_columns in (
    (
        occupancy,
        ("date",),
        ("total_beds", "occupied_beds", "available_beds", "occupancy_rate"),
    ),
    (
        readmissions,
        ("admission_date", "discharge_date"),
        ("readmission_flag",),
    ),
):
    for column in date_columns:
        if column in data.columns:
            data[column] = pd.to_datetime(data[column], errors="coerce")
    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")

if not OCCUPANCY_FILE.is_file():
    st.warning(
        "Synthetic occupancy data is unavailable: "
        "milestone3_data/daily_occupancy.csv was not found."
    )
if not READMISSIONS_FILE.is_file():
    st.warning(
        "Synthetic readmission data is unavailable: "
        "milestone3_data/synthetic_patient_readmissions.csv was not found."
    )

st.sidebar.title("🏥 MedTrack")
st.sidebar.caption("Hospital Analytics Platform")
st.sidebar.divider()
st.sidebar.subheader("Dashboard Filters")

date_series = [
    patients["date_of_admission"].dropna(),
    occupancy["date"].dropna()
    if "date" in occupancy.columns
    else pd.Series(dtype="datetime64[ns]"),
    readmissions["admission_date"].dropna()
    if "admission_date" in readmissions.columns
    else pd.Series(dtype="datetime64[ns]"),
]
available_dates = pd.concat(date_series, ignore_index=True).dropna()
selected_date_range = None
if not available_dates.empty:
    min_date = available_dates.min().date()
    max_date = available_dates.max().date()
    date_input = st.sidebar.date_input(
        "Admission / Snapshot Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if isinstance(date_input, (tuple, list)) and len(date_input) == 2:
        selected_date_range = (date_input[0], date_input[1])

department_values = set(patients["department"].dropna().astype(str))
for data in (occupancy, readmissions):
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

patient_candidates = apply_filters(
    patients,
    "date_of_admission",
    selected_date_range,
    selected_departments,
    hospital_search,
)
condition_options = sorted(
    patient_candidates["medical_condition"].dropna().astype(str).unique()
)
selected_conditions = st.sidebar.multiselect(
    "Medical Condition",
    condition_options,
    default=condition_options,
)
filtered_patients = patient_candidates[
    patient_candidates["medical_condition"].isin(selected_conditions)
].copy()

filtered_occupancy = apply_filters(
    occupancy,
    "date",
    selected_date_range,
    selected_departments,
    hospital_search,
)
filtered_readmissions = apply_filters(
    readmissions,
    "admission_date",
    selected_date_range,
    selected_departments,
    hospital_search,
)

st.title("🏥 Hospital Overview")
st.markdown(
    "A consolidated view of hospital admissions and patient statistics."
)
st.caption("MedTrack | Hospital Data Analytics")
st.divider()

st.subheader("Hospital Overview")

total_admissions = len(filtered_patients)
average_stay = filtered_patients["length_of_stay"].mean()
average_billing = filtered_patients["billing_amount"].mean()

valid_occupancy = filtered_occupancy.dropna(
    subset=["total_beds", "occupied_beds"]
).copy()
valid_occupancy = valid_occupancy[
    (valid_occupancy["total_beds"] > 0)
    & (valid_occupancy["occupied_beds"] >= 0)
    & (valid_occupancy["occupied_beds"] <= valid_occupancy["total_beds"])
]
if len(valid_occupancy) < len(filtered_occupancy):
    st.warning(
        "Some synthetic occupancy rows have missing or invalid bed counts "
        "and are excluded from occupancy calculations."
    )
occupancy_total_beds = valid_occupancy["total_beds"].sum()
occupancy_rate = (
    valid_occupancy["occupied_beds"].sum() / occupancy_total_beds
    if occupancy_total_beds > 0
    else float("nan")
)

readmission_flags = filtered_readmissions["readmission_flag"]
valid_readmission_flags = readmission_flags.dropna()
readmission_data_valid = (
    not filtered_readmissions.empty
    and len(valid_readmission_flags) == len(filtered_readmissions)
    and valid_readmission_flags.isin([0, 1]).all()
)
if not filtered_readmissions.empty and not readmission_data_valid:
    st.warning(
        "Synthetic readmission rate is unavailable because the selected "
        "cohort has missing or invalid readmission flags."
    )
readmission_rate = (
    valid_readmission_flags.sum() / len(filtered_readmissions)
    if readmission_data_valid
    else float("nan")
)

metric_columns = st.columns(5)
metric_columns[0].metric("Total Admissions", f"{total_admissions:,}")
metric_columns[1].metric(
    "Average Length of Stay",
    f"{average_stay:.1f} days" if pd.notna(average_stay) else "N/A",
)
metric_columns[2].metric(
    "Average Billing",
    f"₹{average_billing:,.2f}" if pd.notna(average_billing) else "N/A",
)
metric_columns[3].metric(
    "Weighted Bed Occupancy Rate (Synthetic)",
    f"{occupancy_rate:.1%}" if pd.notna(occupancy_rate) else "N/A",
)
metric_columns[4].metric(
    "Overall Synthetic Readmission Rate",
    f"{readmission_rate:.1%}" if pd.notna(readmission_rate) else "N/A",
)
st.caption(
    "Occupancy and readmission values are synthetic demonstrations, not "
    "actual hospital performance. They are calculated from separate "
    "synthetic datasets and are not linked to the patient records."
)

st.divider()

left, right = st.columns(2)
with left:
    st.subheader("Monthly Admissions")
    monthly_data = filtered_patients.dropna(
        subset=["date_of_admission"]
    ).copy()
    if monthly_data.empty:
        show_figure(None, "No admission records match the selected filters.")
    else:
        monthly_data["month"] = (
            monthly_data["date_of_admission"].dt.to_period("M").astype(str)
        )
        monthly_admissions = (
            monthly_data.groupby("month")
            .size()
            .reset_index(name="admissions")
        )
        figure = px.line(
            monthly_admissions,
            x="month",
            y="admissions",
            markers=True,
            title="Monthly Admission Records",
            labels={"month": "Month", "admissions": "Admissions"},
        )
        show_figure(
            style_figure(figure, "Month", "Admissions"),
            "No monthly admissions are available.",
        )

with right:
    st.subheader("Admissions by Department")
    department_counts = (
        filtered_patients.groupby("department")
        .size()
        .reset_index(name="admissions")
    )
    if department_counts.empty:
        show_figure(None, "No department data matches the selected filters.")
    else:
        figure = px.pie(
            department_counts,
            names="department",
            values="admissions",
            hole=0.5,
            title="Share of Admission Records by Department",
            labels={"department": "Department", "admissions": "Admissions"},
        )
        figure.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate=(
                "<b>%{label}</b><br>Admissions: %{value:,}"
                "<br>Share: %{percent}<extra></extra>"
            ),
        )
        show_figure(
            style_figure(figure, "", "Admissions", "Department"),
            "No department admissions are available.",
        )

left, right = st.columns(2)
with left:
    st.subheader("Admissions by Medical Condition")
    condition_counts = (
        filtered_patients.groupby("medical_condition")
        .size()
        .reset_index(name="admissions")
        .sort_values("admissions", ascending=True)
    )
    if condition_counts.empty:
        show_figure(None, "No condition data matches the selected filters.")
    else:
        figure = px.bar(
            condition_counts,
            x="admissions",
            y="medical_condition",
            orientation="h",
            title="Admission Records by Medical Condition",
            labels={
                "medical_condition": "Medical Condition",
                "admissions": "Admissions",
            },
            text="admissions",
        )
        figure.update_traces(textposition="outside", cliponaxis=False)
        show_figure(
            style_figure(figure, "Admissions", "Medical Condition"),
            "No condition admissions are available.",
        )

with right:
    st.subheader("Occupancy Trends (Synthetic)")
    if valid_occupancy.empty:
        show_figure(
            None,
            "No synthetic occupancy records match the selected filters.",
        )
    else:
        occupancy_by_date = (
            valid_occupancy.groupby("date", as_index=False)
            .agg(
                occupied_beds=("occupied_beds", "sum"),
                total_beds=("total_beds", "sum"),
            )
        )
        occupancy_by_date["occupancy_rate"] = (
            occupancy_by_date["occupied_beds"]
            / occupancy_by_date["total_beds"]
            * 100
        )
        figure = px.area(
            occupancy_by_date,
            x="date",
            y="occupancy_rate",
            title="Daily Occupancy Rate (Synthetic)",
            labels={
                "date": "Snapshot Date",
                "occupancy_rate": "Occupancy Rate (%)",
            },
            custom_data=["occupied_beds", "total_beds"],
        )
        figure.update_traces(
            hovertemplate=(
                "%{x|%b %d, %Y}<br>Occupancy: %{y:.1f}%"
                "<br>Occupied beds: %{customdata[0]:,.0f}"
                "<br>Total beds: %{customdata[1]:,.0f}<extra></extra>"
            )
        )
        figure.update_yaxes(ticksuffix="%", rangemode="tozero")
        show_figure(
            style_figure(figure, "Snapshot Date", "Occupancy Rate (%)"),
            "No synthetic occupancy trend is available.",
        )
    st.caption("Synthetic demonstration data; not actual hospital occupancy.")

left, right = st.columns(2)
with left:
    st.subheader("Occupancy by Department (Synthetic)")
    if valid_occupancy.empty:
        show_figure(
            None,
            "No synthetic occupancy records match the selected filters.",
        )
    else:
        occupancy_by_department = (
            valid_occupancy.groupby("department", as_index=False)
            .agg(
                occupied_beds=("occupied_beds", "sum"),
                total_beds=("total_beds", "sum"),
            )
        )
        occupancy_by_department["occupancy_rate"] = (
            occupancy_by_department["occupied_beds"]
            / occupancy_by_department["total_beds"]
            * 100
        )
        occupancy_by_department = occupancy_by_department.sort_values(
            "occupancy_rate", ascending=True
        )
        figure = px.bar(
            occupancy_by_department,
            x="occupancy_rate",
            y="department",
            orientation="h",
            title="Weighted Occupancy Rate by Department",
            labels={
                "department": "Department",
                "occupancy_rate": "Occupancy Rate (%)",
            },
            text="occupancy_rate",
            custom_data=["occupied_beds", "total_beds"],
        )
        figure.update_traces(
            texttemplate="%{x:.1f}%",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b><br>Occupancy: %{x:.1f}%"
                "<br>Occupied beds: %{customdata[0]:,.0f}"
                "<br>Total beds: %{customdata[1]:,.0f}<extra></extra>"
            ),
        )
        figure.update_xaxes(ticksuffix="%", rangemode="tozero")
        show_figure(
            style_figure(figure, "Occupancy Rate (%)", "Department"),
            "No department occupancy data is available.",
        )
    st.caption("Synthetic demonstration data; not actual hospital occupancy.")

with right:
    st.subheader("Readmission by Department (Synthetic)")
    if not readmission_data_valid:
        show_figure(
            None,
            "No valid synthetic readmission cohort matches the selected filters.",
        )
    else:
        readmission_by_department = (
            filtered_readmissions.groupby("department", as_index=False)
            .agg(
                admissions=("readmission_flag", "size"),
                readmissions=("readmission_flag", "sum"),
                readmission_rate=("readmission_flag", "mean"),
            )
        )
        readmission_by_department["readmission_rate"] *= 100
        readmission_by_department = readmission_by_department.sort_values(
            "readmission_rate", ascending=True
        )
        figure = px.bar(
            readmission_by_department,
            x="readmission_rate",
            y="department",
            orientation="h",
            title="Flagged Synthetic Admissions by Department",
            labels={
                "department": "Department",
                "readmission_rate": "Readmission Rate (%)",
                "admissions": "Synthetic Admissions",
                "readmissions": "Flagged Admissions",
            },
            custom_data=["readmissions", "admissions"],
        )
        figure.update_traces(
            texttemplate="%{x:.1f}%",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b><br>Readmission rate: %{x:.1f}%"
                "<br>Flagged admissions: %{customdata[0]:,.0f}"
                "<br>Total synthetic admissions: %{customdata[1]:,.0f}"
                "<extra></extra>"
            ),
        )
        figure.update_xaxes(ticksuffix="%", rangemode="tozero")
        show_figure(
            style_figure(figure, "Readmission Rate (%)", "Department"),
            "No department readmission data is available.",
        )
    st.caption(
        "Synthetic demonstration data; readmissions are defined by the "
        "source file's 30-day flag and are not linked to patient records."
    )

left, right = st.columns(2)
with left:
    st.subheader("Admission Type Distribution")
    admission_type_counts = (
        filtered_patients.groupby("admission_type")
        .size()
        .reset_index(name="admissions")
    )
    if admission_type_counts.empty:
        show_figure(None, "No admission types match the selected filters.")
    else:
        figure = px.pie(
            admission_type_counts,
            names="admission_type",
            values="admissions",
            title="Share of Admission Records by Type",
            labels={
                "admission_type": "Admission Type",
                "admissions": "Admissions",
            },
        )
        figure.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate=(
                "<b>%{label}</b><br>Admissions: %{value:,}"
                "<br>Share: %{percent}<extra></extra>"
            ),
        )
        show_figure(
            style_figure(figure, "", "Admissions", "Admission Type"),
            "No admission type distribution is available.",
        )

with right:
    st.subheader("Department Summary")
    if filtered_patients.empty:
        st.info("No department summary matches the selected filters.")
    else:
        summary = (
            filtered_patients.groupby("department")
            .agg(
                Total_Admissions=("department", "size"),
                Average_Length_of_Stay=("length_of_stay", "mean"),
                Average_Billing=("billing_amount", "mean"),
            )
            .reset_index()
            .round(2)
        )
        st.dataframe(
            summary,
            width="stretch",
            hide_index=True,
        )

st.download_button(
    "Download Overview Data",
    data=filtered_patients.to_csv(index=False).encode("utf-8"),
    file_name="hospital_overview.csv",
    mime="text/csv",
)

st.divider()
st.caption("MedTrack | Hospital Analytics Project")
