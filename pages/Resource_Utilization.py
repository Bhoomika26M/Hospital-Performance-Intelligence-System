from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Resource Utilization | MedTrack",
    page_icon="🏥",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "milestone3_data"
PATIENT_FILE = BASE_DIR / "hospital_cleaned.csv"
OCCUPANCY_FILE = DATA_DIR / "daily_occupancy.csv"
STAFF_FILE = DATA_DIR / "synthetic_staff_allocation.csv"
EQUIPMENT_FILE = DATA_DIR / "synthetic_equipment_utilization.csv"

OCCUPANCY_COLUMNS = [
    "date", "hospital", "department", "total_beds", "occupied_beds",
    "available_beds", "occupancy_rate",
]
STAFF_COLUMNS = [
    "date", "hospital", "department", "shift", "staff_role",
    "allocated_staff", "required_staff", "available_staff", "absent_staff",
]
EQUIPMENT_COLUMNS = [
    "date", "hospital", "department", "equipment_type", "total_units",
    "in_use_units", "available_units", "maintenance_units", "utilization_rate",
]
PATIENT_COLUMNS = [
    "department", "hospital", "date_of_admission", "length_of_stay",
    "billing_amount",
]
SYNTHETIC_DISCLAIMER = (
    "Staff allocation, equipment utilization and occupancy datasets contain "
    "synthetic demonstration data generated for academic project purposes. "
    "These values do not represent actual hospital operational records and "
    "must not be used for clinical decision-making."
)


@st.cache_data
def load_dataset(
    file_path: str,
    modified_time: float | None,
    date_columns: tuple[str, ...],
    numeric_columns: tuple[str, ...],
) -> pd.DataFrame:
    if modified_time is None:
        return pd.DataFrame()
    data = pd.read_csv(file_path)
    data.columns = (
        data.columns.str.strip().str.lower().str.replace(" ", "_")
    )
    for column in date_columns:
        if column in data.columns:
            data[column] = pd.to_datetime(data[column], errors="coerce")
    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")
    return data


def modified_time(file_path: Path) -> float | None:
    return file_path.stat().st_mtime if file_path.is_file() else None


def load_required(
    file_path: Path,
    required_columns: list[str],
    date_columns: tuple[str, ...] = ("date",),
    numeric_columns: tuple[str, ...] = (),
) -> pd.DataFrame:
    data = load_dataset(
        str(file_path),
        modified_time(file_path),
        date_columns,
        numeric_columns,
    )
    if modified_time(file_path) is None:
        st.warning(f"Data file is unavailable: {file_path.name}")
        return pd.DataFrame(columns=required_columns)
    missing_columns = set(required_columns) - set(data.columns)
    if missing_columns:
        st.warning(
            f"{file_path.name} is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )
        return pd.DataFrame(columns=required_columns)
    return data


def filter_data(
    data: pd.DataFrame,
    date_column: str,
    date_range: tuple,
    departments: list[str],
    hospitals: list[str],
) -> pd.DataFrame:
    result = data
    if "department" in result.columns:
        result = result[result["department"].isin(departments)]
    if "hospital" in result.columns:
        result = result[result["hospital"].isin(hospitals)]
    if date_column in result.columns and date_range:
        start_date, end_date = date_range
        result = result[
            result[date_column].notna()
            & result[date_column].dt.date.between(start_date, end_date)
        ]
    return result.copy()


def style_figure(
    figure: go.Figure,
    x_title: str,
    y_title: str,
    legend_title: str = "",
) -> go.Figure:
    figure.update_layout(
        template="plotly_dark",
        margin=dict(l=20, r=20, t=65, b=25),
        xaxis_title=x_title,
        yaxis_title=y_title,
        legend_title_text=legend_title,
        hoverlabel=dict(namelength=-1),
        height=360,
    )
    return figure


def show_figure(figure: go.Figure | None, empty_message: str) -> None:
    if figure is None:
        st.info(empty_message)
    else:
        st.plotly_chart(
            figure,
            width="stretch",
            config={"displayModeBar": False},
        )


def weighted_ratio(numerator: float, denominator: float) -> float:
    return numerator / denominator * 100 if denominator > 0 else float("nan")


def status_label(value: float, high: float, moderate: float) -> str:
    if pd.isna(value):
        return "Unavailable"
    if value >= high:
        return "High"
    if value >= moderate:
        return "Moderate"
    return "Low"


def safe_metric(value: float, suffix: str = "", decimals: int = 0) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:,.{decimals}f}{suffix}"


patients = load_required(
    PATIENT_FILE,
    PATIENT_COLUMNS,
    date_columns=("date_of_admission",),
    numeric_columns=("length_of_stay", "billing_amount"),
)
occupancy = load_required(
    OCCUPANCY_FILE,
    OCCUPANCY_COLUMNS,
    numeric_columns=(
        "total_beds", "occupied_beds", "available_beds", "occupancy_rate",
    ),
)
staff = load_required(
    STAFF_FILE,
    STAFF_COLUMNS,
    numeric_columns=(
        "allocated_staff", "required_staff", "available_staff", "absent_staff",
    ),
)
equipment = load_required(
    EQUIPMENT_FILE,
    EQUIPMENT_COLUMNS,
    numeric_columns=(
        "total_units", "in_use_units", "available_units", "maintenance_units",
        "utilization_rate",
    ),
)

for frame, date_column in (
    (patients, "date_of_admission"),
    (occupancy, "date"),
    (staff, "date"),
    (equipment, "date"),
):
    if date_column in frame.columns:
        frame[date_column] = pd.to_datetime(frame[date_column], errors="coerce")

date_series = [
    frame[column].dropna()
    for frame, column in (
        (patients, "date_of_admission"),
        (occupancy, "date"),
        (staff, "date"),
        (equipment, "date"),
    )
    if column in frame.columns
]
available_dates = pd.concat(date_series, ignore_index=True).dropna()

st.sidebar.title("🏥 MedTrack")
st.sidebar.caption("Resource Utilization")
st.sidebar.divider()
st.sidebar.subheader("Dashboard Filters")

selected_date_range = None
if not available_dates.empty:
    earliest = available_dates.min().date()
    latest = available_dates.max().date()
    date_value = st.sidebar.date_input(
        "Date Range",
        value=(earliest, latest),
        min_value=earliest,
        max_value=latest,
    )
    if isinstance(date_value, (tuple, list)) and len(date_value) == 2:
        selected_date_range = (date_value[0], date_value[1])

department_values: set[str] = set()
hospital_values: set[str] = set()
for frame in (patients, occupancy, staff, equipment):
    if "department" in frame.columns:
        department_values.update(frame["department"].dropna().astype(str))
    if "hospital" in frame.columns:
        hospital_values.update(frame["hospital"].dropna().astype(str))
department_options = sorted(department_values)
hospital_options = sorted(hospital_values)
selected_departments = st.sidebar.multiselect(
    "Department",
    department_options,
    default=department_options,
)
selected_hospitals = st.sidebar.multiselect(
    "Hospital",
    hospital_options,
    default=hospital_options,
)

filtered_patients = filter_data(
    patients, "date_of_admission", selected_date_range,
    selected_departments, selected_hospitals,
)
filtered_occupancy = filter_data(
    occupancy, "date", selected_date_range,
    selected_departments, selected_hospitals,
)
filtered_staff = filter_data(
    staff, "date", selected_date_range,
    selected_departments, selected_hospitals,
)
filtered_equipment = filter_data(
    equipment, "date", selected_date_range,
    selected_departments, selected_hospitals,
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
        "Occupancy rows with missing, negative, or inconsistent bed counts "
        "are excluded from calculations."
    )

valid_staff = filtered_staff.dropna(
    subset=[
        "allocated_staff", "required_staff", "available_staff", "absent_staff",
    ]
).copy()
valid_staff = valid_staff[
    valid_staff[
        ["allocated_staff", "required_staff", "available_staff", "absent_staff"]
    ].ge(0).all(axis=1)
    & valid_staff["absent_staff"].le(valid_staff["allocated_staff"])
    & valid_staff["available_staff"].eq(
        valid_staff["allocated_staff"] - valid_staff["absent_staff"]
    )
]
if len(valid_staff) < len(filtered_staff):
    st.warning(
        "Staff rows with missing or inconsistent counts are excluded from "
        "calculations."
    )

valid_equipment = filtered_equipment.dropna(
    subset=[
        "total_units", "in_use_units", "available_units", "maintenance_units",
    ]
).copy()
valid_equipment = valid_equipment[
    valid_equipment[
        ["total_units", "in_use_units", "available_units", "maintenance_units"]
    ].ge(0).all(axis=1)
    & valid_equipment["total_units"].eq(
        valid_equipment["in_use_units"]
        + valid_equipment["available_units"]
        + valid_equipment["maintenance_units"]
    )
]
if len(valid_equipment) < len(filtered_equipment):
    st.warning(
        "Equipment rows with missing, negative, or inconsistent counts are "
        "excluded from calculations."
    )

st.title("🏥 Resource Utilization")
st.markdown(
    "Explore bed capacity, synthetic staffing demonstrations, and synthetic "
    "equipment utilization for the selected period and locations."
)
st.info(SYNTHETIC_DISCLAIMER)

st.header("Bed Utilization")
st.caption(
    "Bed totals across daily snapshots are bed-days. Weighted occupancy is "
    "calculated from summed occupied beds divided by summed total beds."
)
if valid_occupancy.empty:
    st.info("No valid occupancy observations match the selected filters.")
else:
    total_beds = float(valid_occupancy["total_beds"].sum())
    occupied_beds = float(valid_occupancy["occupied_beds"].sum())
    available_beds = float(valid_occupancy["available_beds"].sum())
    occupancy_rate = weighted_ratio(occupied_beds, total_beds)
    bed_cols = st.columns(4)
    bed_cols[0].metric("Total Beds (Bed-Days)", safe_metric(total_beds))
    bed_cols[1].metric("Occupied Beds (Bed-Days)", safe_metric(occupied_beds))
    bed_cols[2].metric("Available Beds (Bed-Days)", safe_metric(available_beds))
    bed_cols[3].metric(
        "Weighted Bed Occupancy Rate (Synthetic)",
        safe_metric(occupancy_rate, "%", 1),
    )

    department_beds = (
        valid_occupancy.groupby("department", as_index=False, observed=True)
        .agg(
            total_beds=("total_beds", "sum"),
            occupied_beds=("occupied_beds", "sum"),
            available_beds=("available_beds", "sum"),
        )
    )
    department_beds["occupancy_rate"] = (
        department_beds["occupied_beds"] / department_beds["total_beds"] * 100
    )
    monthly_beds = (
        valid_occupancy.assign(
            month=valid_occupancy["date"].dt.to_period("M").dt.to_timestamp()
        )
        .groupby("month", as_index=False, observed=True)
        .agg(
            total_beds=("total_beds", "sum"),
            occupied_beds=("occupied_beds", "sum"),
            available_beds=("available_beds", "sum"),
        )
    )
    monthly_beds["occupancy_rate"] = (
        monthly_beds["occupied_beds"] / monthly_beds["total_beds"] * 100
    )
    left, right = st.columns(2)
    with left:
        st.subheader("Department Occupancy")
        fig = px.bar(
            department_beds.sort_values("occupancy_rate"),
            x="occupancy_rate",
            y="department",
            orientation="h",
            color="occupancy_rate",
            color_continuous_scale="Teal",
            text="occupancy_rate",
            custom_data=["occupied_beds", "total_beds"],
            title="Weighted Occupancy by Department",
            labels={
                "department": "Department",
                "occupancy_rate": "Occupancy (%)",
            },
        )
        fig.update_traces(
            texttemplate="%{x:.1f}%",
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>Occupancy: %{x:.2f}%"
                "<br>Occupied bed-days: %{customdata[0]:,.0f}"
                "<br>Total bed-days: %{customdata[1]:,.0f}<extra></extra>"
            ),
        )
        fig.update_xaxes(ticksuffix="%", rangemode="tozero")
        show_figure(style_figure(fig, "Occupancy (%)", "Department"),
                    "No department occupancy data is available.")
    with right:
        st.subheader("Monthly Occupancy Trend")
        fig = px.line(
            monthly_beds,
            x="month",
            y="occupancy_rate",
            markers=True,
            title="Monthly Weighted Bed Occupancy",
            labels={"month": "Month", "occupancy_rate": "Occupancy (%)"},
            custom_data=["occupied_beds", "total_beds"],
        )
        fig.update_traces(
            hovertemplate=(
                "%{x|%B %Y}<br>Occupancy: %{y:.2f}%"
                "<br>Occupied bed-days: %{customdata[0]:,.0f}"
                "<br>Total bed-days: %{customdata[1]:,.0f}<extra></extra>"
            )
        )
        fig.update_yaxes(ticksuffix="%", rangemode="tozero")
        show_figure(style_figure(fig, "Month", "Occupancy (%)"),
                    "No monthly occupancy trend is available.")

    left, right = st.columns(2)
    with left:
        st.subheader("Occupied vs. Available Beds")
        bed_long = department_beds.melt(
            id_vars="department",
            value_vars=["occupied_beds", "available_beds"],
            var_name="bed_status",
            value_name="bed_days",
        )
        bed_long["bed_status"] = bed_long["bed_status"].map(
            {"occupied_beds": "Occupied", "available_beds": "Available"}
        )
        fig = px.bar(
            bed_long,
            x="bed_days",
            y="department",
            color="bed_status",
            barmode="stack",
            orientation="h",
            title="Bed-Days by Department",
            labels={
                "department": "Department",
                "bed_days": "Bed-Days",
                "bed_status": "Bed Status",
            },
            color_discrete_map={"Occupied": "#38BDF8", "Available": "#34D399"},
        )
        show_figure(style_figure(fig, "Bed-Days", "Department", "Bed Status"),
                    "No bed comparison is available.")
    with right:
        st.subheader("Bed Availability Over Time")
        fig = px.area(
            monthly_beds,
            x="month",
            y="available_beds",
            title="Available Bed-Days by Month",
            labels={"month": "Month", "available_beds": "Available Bed-Days"},
        )
        show_figure(style_figure(fig, "Month", "Available Bed-Days"),
                    "No bed availability trend is available.")

st.header("Staff Allocation Monitoring (Synthetic Demonstration)")
st.caption(
    "Staff metrics are summed staff-shifts across selected dates and roles; "
    "they are not unique-person headcounts. Available staff is distinct from "
    "allocated staff."
)
if valid_staff.empty:
    st.info("No valid staff allocation records match the selected filters.")
else:
    staff_allocated = float(valid_staff["allocated_staff"].sum())
    staff_required = float(valid_staff["required_staff"].sum())
    staff_available = float(valid_staff["available_staff"].sum())
    staff_absent = float(valid_staff["absent_staff"].sum())
    staff_shortage = float(
        np.maximum(
            valid_staff["required_staff"] - valid_staff["available_staff"], 0
        ).sum()
    )
    staff_coverage = weighted_ratio(staff_available, staff_required)
    staff_cols = st.columns(6)
    staff_cols[0].metric("Allocated Staff-Shifts", safe_metric(staff_allocated))
    staff_cols[1].metric("Available Staff-Shifts", safe_metric(staff_available))
    staff_cols[2].metric("Required Staff-Shifts", safe_metric(staff_required))
    staff_cols[3].metric("Absent Staff-Shifts", safe_metric(staff_absent))
    staff_cols[4].metric("Staff Shortage", safe_metric(staff_shortage))
    staff_cols[5].metric(
        "Staff Coverage", safe_metric(staff_coverage, "%", 1)
    )

    staff_department = (
        valid_staff.groupby("department", as_index=False, observed=True)
        .agg(
            allocated_staff=("allocated_staff", "sum"),
            required_staff=("required_staff", "sum"),
            available_staff=("available_staff", "sum"),
            absent_staff=("absent_staff", "sum"),
        )
    )
    staff_department["shortage"] = np.maximum(
        staff_department["required_staff"] - staff_department["available_staff"],
        0,
    )
    staff_department["coverage"] = (
        staff_department["available_staff"]
        / staff_department["required_staff"].replace(0, np.nan)
        * 100
    )
    staff_month = (
        valid_staff.assign(
            month=valid_staff["date"].dt.to_period("M").dt.to_timestamp()
        )
        .groupby("month", as_index=False, observed=True)
        .agg(
            available_staff=("available_staff", "sum"),
            required_staff=("required_staff", "sum"),
        )
    )
    staff_month["coverage"] = (
        staff_month["available_staff"]
        / staff_month["required_staff"].replace(0, np.nan)
        * 100
    )
    left, right = st.columns(2)
    with left:
        st.subheader("Staff Allocation by Department")
        fig = px.bar(
            staff_department.sort_values("allocated_staff"),
            x="allocated_staff",
            y="department",
            orientation="h",
            color="allocated_staff",
            color_continuous_scale="Blues",
            title="Allocated Staff-Shifts by Department",
            labels={
                "department": "Department",
                "allocated_staff": "Allocated Staff-Shifts",
            },
            text="allocated_staff",
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        show_figure(style_figure(fig, "Allocated Staff-Shifts", "Department"),
                    "No staff allocation by department is available.")
    with right:
        st.subheader("Required vs. Allocated vs. Available")
        staffing_long = staff_department.melt(
            id_vars="department",
            value_vars=["required_staff", "allocated_staff", "available_staff"],
            var_name="staff_measure",
            value_name="staff_shifts",
        )
        staffing_long["staff_measure"] = staffing_long["staff_measure"].map(
            {
                "required_staff": "Required",
                "allocated_staff": "Allocated",
                "available_staff": "Available",
            }
        )
        fig = px.bar(
            staffing_long,
            x="department",
            y="staff_shifts",
            color="staff_measure",
            barmode="group",
            title="Staffing Levels by Department",
            labels={
                "department": "Department",
                "staff_shifts": "Staff-Shifts",
                "staff_measure": "Measure",
            },
            color_discrete_map={
                "Required": "#F59E0B",
                "Allocated": "#38BDF8",
                "Available": "#34D399",
            },
        )
        show_figure(style_figure(fig, "Department", "Staff-Shifts", "Measure"),
                    "No staffing level comparison is available.")

    left, right = st.columns(2)
    with left:
        st.subheader("Shift-Wise Staffing")
        shift_summary = (
            valid_staff.groupby("shift", as_index=False, observed=True)
            .agg(
                required_staff=("required_staff", "sum"),
                allocated_staff=("allocated_staff", "sum"),
                available_staff=("available_staff", "sum"),
            )
        )
        shift_long = shift_summary.melt(
            id_vars="shift",
            var_name="staff_measure",
            value_name="staff_shifts",
        )
        shift_long["staff_measure"] = shift_long["staff_measure"].map(
            {
                "required_staff": "Required",
                "allocated_staff": "Allocated",
                "available_staff": "Available",
            }
        )
        fig = px.bar(
            shift_long,
            x="shift",
            y="staff_shifts",
            color="staff_measure",
            barmode="group",
            title="Staff-Shifts by Shift",
            labels={
                "shift": "Shift",
                "staff_shifts": "Staff-Shifts",
                "staff_measure": "Measure",
            },
        )
        show_figure(style_figure(fig, "Shift", "Staff-Shifts", "Measure"),
                    "No shift-wise staffing data is available.")
    with right:
        st.subheader("Staff Role Distribution")
        role_summary = (
            valid_staff.groupby("staff_role", as_index=False, observed=True)
            .agg(allocated_staff=("allocated_staff", "sum"))
        )
        fig = px.pie(
            role_summary,
            names="staff_role",
            values="allocated_staff",
            hole=0.5,
            title="Allocated Staff-Shifts by Role",
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="%{label}<br>Staff-shifts: %{value:,.0f}<extra></extra>",
        )
        show_figure(style_figure(fig, "", "Allocated Staff-Shifts", "Role"),
                    "No staff role distribution is available.")

    left, right = st.columns(2)
    with left:
        st.subheader("Shortage by Department")
        fig = px.bar(
            staff_department.sort_values("shortage"),
            x="shortage",
            y="department",
            orientation="h",
            color="shortage",
            color_continuous_scale="Oranges",
            title="Staff Shortage Staff-Shifts",
            labels={
                "department": "Department",
                "shortage": "Shortage Staff-Shifts",
                "coverage": "Coverage (%)",
            },
            custom_data=["coverage"],
        )
        fig.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>Shortage: %{x:,.0f} staff-shifts"
                "<br>Coverage: %{customdata[0]:.1f}%<extra></extra>"
            )
        )
        show_figure(style_figure(fig, "Shortage Staff-Shifts", "Department"),
                    "No staff shortage data is available.")
    with right:
        st.subheader("Monthly Staff Availability")
        fig = px.line(
            staff_month,
            x="month",
            y="available_staff",
            markers=True,
            title="Available Staff-Shifts by Month",
            labels={
                "month": "Month",
                "available_staff": "Available Staff-Shifts",
            },
            custom_data=["required_staff", "coverage"],
        )
        fig.update_traces(
            hovertemplate=(
                "%{x|%B %Y}<br>Available: %{y:,.0f} staff-shifts"
                "<br>Required: %{customdata[0]:,.0f}"
                "<br>Coverage: %{customdata[1]:.1f}%<extra></extra>"
            )
        )
        show_figure(style_figure(fig, "Month", "Available Staff-Shifts"),
                    "No monthly staff availability trend is available.")

st.header("Equipment Utilization (Synthetic Demonstration)")
st.caption(
    "Weighted equipment utilization is total in-use units divided by total "
    "operational units (total units minus maintenance units)."
)
if valid_equipment.empty:
    st.info("No valid equipment records match the selected filters.")
else:
    total_units = float(valid_equipment["total_units"].sum())
    in_use_units = float(valid_equipment["in_use_units"].sum())
    available_units = float(valid_equipment["available_units"].sum())
    maintenance_units = float(valid_equipment["maintenance_units"].sum())
    operational_units = total_units - maintenance_units
    equipment_utilization = weighted_ratio(in_use_units, operational_units)
    equipment_cols = st.columns(5)
    equipment_cols[0].metric("Total Equipment Units", safe_metric(total_units))
    equipment_cols[1].metric("In-Use Equipment", safe_metric(in_use_units))
    equipment_cols[2].metric("Available Equipment", safe_metric(available_units))
    equipment_cols[3].metric(
        "Under Maintenance", safe_metric(maintenance_units)
    )
    equipment_cols[4].metric(
        "Weighted Utilization",
        safe_metric(equipment_utilization, "%", 1),
    )

    department_equipment = (
        valid_equipment.groupby("department", as_index=False, observed=True)
        .agg(
            total_units=("total_units", "sum"),
            in_use_units=("in_use_units", "sum"),
            available_units=("available_units", "sum"),
            maintenance_units=("maintenance_units", "sum"),
        )
    )
    department_equipment["operational_units"] = (
        department_equipment["total_units"]
        - department_equipment["maintenance_units"]
    )
    department_equipment["utilization"] = (
        department_equipment["in_use_units"]
        / department_equipment["operational_units"].replace(0, np.nan)
        * 100
    )
    department_equipment["availability_pct"] = (
        department_equipment["available_units"]
        / department_equipment["operational_units"].replace(0, np.nan)
        * 100
    )
    equipment_month = (
        valid_equipment.assign(
            month=valid_equipment["date"].dt.to_period("M").dt.to_timestamp()
        )
        .groupby("month", as_index=False, observed=True)
        .agg(
            total_units=("total_units", "sum"),
            in_use_units=("in_use_units", "sum"),
            maintenance_units=("maintenance_units", "sum"),
        )
    )
    equipment_month["utilization"] = (
        equipment_month["in_use_units"]
        / (
            equipment_month["total_units"]
            - equipment_month["maintenance_units"]
        ).replace(0, np.nan)
        * 100
    )
    left, right = st.columns(2)
    with left:
        st.subheader("Department Equipment Utilization")
        fig = px.bar(
            department_equipment.sort_values("utilization"),
            x="utilization",
            y="department",
            orientation="h",
            color="utilization",
            color_continuous_scale="Sunset",
            title="Weighted Utilization by Department",
            labels={
                "department": "Department",
                "utilization": "Utilization (%)",
                "in_use_units": "In-Use Units",
                "operational_units": "Operational Units",
            },
            text="utilization",
            custom_data=["in_use_units", "operational_units"],
        )
        fig.update_traces(
            texttemplate="%{x:.1f}%",
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>Utilization: %{x:.2f}%"
                "<br>In-use units: %{customdata[0]:,.0f}"
                "<br>Operational units: %{customdata[1]:,.0f}<extra></extra>"
            ),
        )
        fig.update_xaxes(ticksuffix="%", rangemode="tozero")
        show_figure(style_figure(fig, "Utilization (%)", "Department"),
                    "No department equipment utilization is available.")
    with right:
        st.subheader("Equipment Type Distribution")
        equipment_types = (
            valid_equipment.groupby("equipment_type", as_index=False, observed=True)
            .agg(total_units=("total_units", "sum"))
            .sort_values("total_units", ascending=False)
        )
        fig = px.pie(
            equipment_types,
            names="equipment_type",
            values="total_units",
            hole=0.48,
            title="Equipment Units by Type",
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate="%{label}<br>Total units: %{value:,.0f}<extra></extra>",
        )
        show_figure(style_figure(fig, "", "Equipment Units", "Equipment Type"),
                    "No equipment type data is available.")

    left, right = st.columns(2)
    with left:
        st.subheader("Equipment Status by Department")
        equipment_long = department_equipment.melt(
            id_vars="department",
            value_vars=["in_use_units", "available_units", "maintenance_units"],
            var_name="equipment_status",
            value_name="units",
        )
        equipment_long["equipment_status"] = equipment_long[
            "equipment_status"
        ].map(
            {
                "in_use_units": "In Use",
                "available_units": "Available",
                "maintenance_units": "Maintenance",
            }
        )
        fig = px.bar(
            equipment_long,
            x="units",
            y="department",
            color="equipment_status",
            barmode="stack",
            orientation="h",
            title="Equipment Units by Status",
            labels={
                "department": "Department",
                "units": "Equipment Units",
                "equipment_status": "Status",
            },
            color_discrete_map={
                "In Use": "#38BDF8",
                "Available": "#34D399",
                "Maintenance": "#F59E0B",
            },
        )
        show_figure(style_figure(fig, "Equipment Units", "Department", "Status"),
                    "No equipment status comparison is available.")
    with right:
        st.subheader("Monthly Equipment Utilization")
        fig = px.line(
            equipment_month,
            x="month",
            y="utilization",
            markers=True,
            title="Monthly Weighted Equipment Utilization",
            labels={"month": "Month", "utilization": "Utilization (%)"},
            custom_data=["in_use_units", "total_units", "maintenance_units"],
        )
        fig.update_traces(
            hovertemplate=(
                "%{x|%B %Y}<br>Utilization: %{y:.2f}%"
                "<br>In-use units: %{customdata[0]:,.0f}"
                "<br>Total units: %{customdata[1]:,.0f}"
                "<br>Maintenance units: %{customdata[2]:,.0f}<extra></extra>"
            )
        )
        fig.update_yaxes(ticksuffix="%", rangemode="tozero")
        show_figure(style_figure(fig, "Month", "Utilization (%)"),
                    "No monthly equipment utilization trend is available.")

    equipment_by_type = (
        valid_equipment.groupby("equipment_type", as_index=False, observed=True)
        .agg(
            total_units=("total_units", "sum"),
            in_use_units=("in_use_units", "sum"),
            available_units=("available_units", "sum"),
            maintenance_units=("maintenance_units", "sum"),
        )
    )
    equipment_by_type["operational_units"] = (
        equipment_by_type["total_units"]
        - equipment_by_type["maintenance_units"]
    )
    equipment_by_type["utilization"] = (
        equipment_by_type["in_use_units"]
        / equipment_by_type["operational_units"].replace(0, np.nan)
        * 100
    )
    st.subheader("High-Utilization Equipment Analysis")
    high_equipment = equipment_by_type.sort_values(
        "utilization", ascending=False
    )
    high_equipment["Utilization Status"] = high_equipment["utilization"].map(
        lambda value: status_label(value, 80, 60)
    )
    high_equipment = high_equipment.rename(
        columns={
            "equipment_type": "Equipment Type",
            "total_units": "Total Units",
            "in_use_units": "In-Use Units",
            "available_units": "Available Units",
            "maintenance_units": "Maintenance Units",
            "utilization": "Weighted Utilization (%)",
        }
    )
    high_equipment["Weighted Utilization (%)"] = high_equipment[
        "Weighted Utilization (%)"
    ].round(2)
    st.dataframe(
        high_equipment[
            [
                "Equipment Type", "Total Units", "In-Use Units",
                "Available Units", "Maintenance Units",
                "Weighted Utilization (%)", "Utilization Status",
            ]
        ],
        width="stretch",
        hide_index=True,
    )

st.header("Capacity Planning (Academic Demonstration)")
st.caption(
    "Thresholds: bed occupancy High ≥80%, Moderate 60–<80%, Low <60%; "
    "staff shortage ratio High ≥10%, Moderate 5–<10%, Low <5%; equipment "
    "utilization High ≥80%, Moderate 60–<80%, Low <60%. Low availability is "
    "bed availability <20% of bed-days, staff coverage <90%, or equipment "
    "available units <20% of operational units. These labels are descriptive "
    "only and are not clinical recommendations."
)
if valid_occupancy.empty and valid_staff.empty and valid_equipment.empty:
    st.info("No resource records match the selected filters.")
else:
    departments_in_view = sorted(
        set(valid_occupancy.get("department", pd.Series(dtype=str)).dropna())
        | set(valid_staff.get("department", pd.Series(dtype=str)).dropna())
        | set(valid_equipment.get("department", pd.Series(dtype=str)).dropna())
    )
    capacity_summary = pd.DataFrame({"Department": departments_in_view})

    if not valid_occupancy.empty:
        bed_summary = (
            valid_occupancy.groupby("department", as_index=False, observed=True)
            .agg(
                total_bed_days=("total_beds", "sum"),
                occupied_bed_days=("occupied_beds", "sum"),
                available_bed_days=("available_beds", "sum"),
            )
        )
        bed_summary["Bed Occupancy (%)"] = (
            bed_summary["occupied_bed_days"]
            / bed_summary["total_bed_days"]
            * 100
        )
        bed_summary["Bed Availability (%)"] = (
            bed_summary["available_bed_days"]
            / bed_summary["total_bed_days"]
            * 100
        )
        bed_summary["Bed Status"] = bed_summary["Bed Occupancy (%)"].map(
            lambda value: status_label(value, 80, 60)
        )
        capacity_summary = capacity_summary.merge(
            bed_summary.rename(columns={"department": "Department"}),
            on="Department",
            how="left",
        )

    if not valid_staff.empty:
        staff_summary = (
            valid_staff.groupby("department", as_index=False, observed=True)
            .agg(
                required_staff=("required_staff", "sum"),
                available_staff=("available_staff", "sum"),
            )
        )
        staff_summary["Staff Coverage (%)"] = (
            staff_summary["available_staff"]
            / staff_summary["required_staff"].replace(0, np.nan)
            * 100
        )
        staff_summary["Staff Shortage"] = np.maximum(
            staff_summary["required_staff"] - staff_summary["available_staff"],
            0,
        )
        staff_summary["Staff Shortage (%)"] = (
            staff_summary["Staff Shortage"]
            / staff_summary["required_staff"].replace(0, np.nan)
            * 100
        )
        staff_summary["Staff Status"] = staff_summary[
            "Staff Shortage (%)"
        ].map(lambda value: status_label(value, 10, 5))
        capacity_summary = capacity_summary.merge(
            staff_summary.rename(columns={"department": "Department"}),
            on="Department",
            how="left",
        )

    if not valid_equipment.empty:
        equipment_summary = (
            valid_equipment.groupby("department", as_index=False, observed=True)
            .agg(
                total_equipment=("total_units", "sum"),
                in_use_equipment=("in_use_units", "sum"),
                available_equipment=("available_units", "sum"),
                maintenance_equipment=("maintenance_units", "sum"),
            )
        )
        equipment_summary["Equipment Utilization (%)"] = (
            equipment_summary["in_use_equipment"]
            / (
                equipment_summary["total_equipment"]
                - equipment_summary["maintenance_equipment"]
            ).replace(0, np.nan)
            * 100
        )
        equipment_summary["Equipment Availability (%)"] = (
            equipment_summary["available_equipment"]
            / (
                equipment_summary["total_equipment"]
                - equipment_summary["maintenance_equipment"]
            ).replace(0, np.nan)
            * 100
        )
        equipment_summary["Equipment Status"] = equipment_summary[
            "Equipment Utilization (%)"
        ].map(lambda value: status_label(value, 80, 60))
        capacity_summary = capacity_summary.merge(
            equipment_summary.rename(columns={"department": "Department"}),
            on="Department",
            how="left",
        )

    for column in ("Bed Status", "Staff Status", "Equipment Status"):
        if column not in capacity_summary.columns:
            capacity_summary[column] = "Unavailable"
        else:
            capacity_summary[column] = capacity_summary[column].fillna(
                "Unavailable"
            )
    for column in (
        "Bed Availability (%)", "Staff Coverage (%)",
        "Equipment Availability (%)",
    ):
        if column not in capacity_summary.columns:
            capacity_summary[column] = np.nan

    def resource_availability_status(row: pd.Series) -> str:
        measured = [
            row["Bed Availability (%)"],
            row["Staff Coverage (%)"],
            row["Equipment Availability (%)"],
        ]
        if all(pd.isna(value) for value in measured):
            return "Unavailable"
        low_availability = (
            (pd.notna(measured[0]) and measured[0] < 20)
            or (pd.notna(measured[1]) and measured[1] < 90)
            or (pd.notna(measured[2]) and measured[2] < 20)
        )
        return "Yes" if low_availability else "No"

    capacity_summary["Low Resource Availability"] = capacity_summary.apply(
        resource_availability_status,
        axis=1,
    )
    st.dataframe(
        capacity_summary.round(2),
        width="stretch",
        hide_index=True,
    )

st.header("Resource Availability by Department")
st.caption(
    "Availability percentages use distinct denominators: available beds / "
    "total beds, available staff / required staff, and available equipment / "
    "operational equipment. Values are not interchangeable resource units."
)
availability_rows = []
if not valid_occupancy.empty:
    by_department = valid_occupancy.groupby(
        "department", observed=True
    ).agg(
        available=("available_beds", "sum"),
        denominator=("total_beds", "sum"),
    )
    for department, row in by_department.iterrows():
        availability_rows.append(
            {
                "department": department,
                "resource": "Beds",
                "available": row["available"],
                "availability_pct": weighted_ratio(
                    row["available"], row["denominator"]
                ),
            }
        )
if not valid_staff.empty:
    by_department = valid_staff.groupby(
        "department", observed=True
    ).agg(
        available=("available_staff", "sum"),
        denominator=("required_staff", "sum"),
    )
    for department, row in by_department.iterrows():
        availability_rows.append(
            {
                "department": department,
                "resource": "Staff",
                "available": row["available"],
                "availability_pct": weighted_ratio(
                    row["available"], row["denominator"]
                ),
            }
        )
if not valid_equipment.empty:
    equipment_availability = valid_equipment.assign(
        operational_units=(
            valid_equipment["total_units"]
            - valid_equipment["maintenance_units"]
        )
    ).groupby("department", observed=True).agg(
        available=("available_units", "sum"),
        denominator=("operational_units", "sum"),
    )
    for department, row in equipment_availability.iterrows():
        availability_rows.append(
            {
                "department": department,
                "resource": "Equipment",
                "available": row["available"],
                "availability_pct": weighted_ratio(
                    row["available"], row["denominator"]
                ),
            }
        )

if not availability_rows:
    st.info("No resource availability data matches the selected filters.")
else:
    availability = pd.DataFrame(availability_rows)
    left, right = st.columns(2)
    with left:
        st.subheader("Availability Percentage Comparison")
        fig = px.bar(
            availability,
            x="department",
            y="availability_pct",
            color="resource",
            barmode="group",
            title="Available Share by Department",
            labels={
                "department": "Department",
                "availability_pct": "Availability (%)",
                "resource": "Resource",
            },
            color_discrete_map={
                "Beds": "#38BDF8",
                "Staff": "#A78BFA",
                "Equipment": "#34D399",
            },
        )
        fig.update_yaxes(ticksuffix="%", rangemode="tozero")
        show_figure(
            style_figure(fig, "Department", "Availability (%)", "Resource"),
            "No availability percentage comparison is available.",
        )
    with right:
        st.subheader("Available Resource Counts")
        fig = px.bar(
            availability,
            x="available",
            y="department",
            color="resource",
            barmode="group",
            orientation="h",
            title="Available Counts (Resource-Specific Units)",
            labels={
                "department": "Department",
                "available": "Available Bed-Days / Staff-Shifts / Units",
                "resource": "Resource",
            },
        )
        show_figure(
            style_figure(
                fig,
                "Available Counts (Units Differ by Resource)",
                "Department",
                "Resource",
            ),
            "No available resource counts are available.",
        )

st.header("Source-Data Workload Indicators")
st.caption(
    "These measures use original patient records and are not joined to "
    "synthetic occupancy, staff, or equipment data."
)
patient_metrics = st.columns(3)
patient_metrics[0].metric("Admission Records", f"{len(filtered_patients):,}")
average_stay = filtered_patients["length_of_stay"].mean()
patient_metrics[1].metric(
    "Average Length of Stay",
    f"{average_stay:.1f} days" if pd.notna(average_stay) else "N/A",
)
average_billing = filtered_patients["billing_amount"].mean()
patient_metrics[2].metric(
    "Average Billing",
    f"₹{average_billing:,.2f}" if pd.notna(average_billing) else "N/A",
)

if filtered_patients.empty:
    st.info("No patient records match the selected filters.")
else:
    patient_department = (
        filtered_patients.groupby("department", as_index=False, observed=True)
        .agg(
            admission_records=("department", "size"),
            average_length_of_stay=("length_of_stay", "mean"),
            average_billing=("billing_amount", "mean"),
        )
        .round(2)
    )
    left, right = st.columns(2)
    with left:
        st.subheader("Admission Workload by Department")
        fig = px.bar(
            patient_department.sort_values("admission_records"),
            x="admission_records",
            y="department",
            orientation="h",
            title="Source Admission Records",
            labels={
                "department": "Department",
                "admission_records": "Admission Records",
            },
            text="admission_records",
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        show_figure(style_figure(fig, "Admission Records", "Department"),
                    "No workload data is available.")
    with right:
        st.subheader("Average Length of Stay by Department")
        fig = px.bar(
            patient_department.sort_values("average_length_of_stay"),
            x="average_length_of_stay",
            y="department",
            orientation="h",
            title="Average Source-Data Length of Stay",
            labels={
                "department": "Department",
                "average_length_of_stay": "Average Stay (Days)",
            },
            text="average_length_of_stay",
        )
        fig.update_traces(
            texttemplate="%{x:.1f} days",
            textposition="outside",
            cliponaxis=False,
        )
        show_figure(style_figure(fig, "Average Stay (Days)", "Department"),
                    "No length-of-stay summary is available.")

    if "doctor" in filtered_patients.columns:
        st.subheader("Admissions per Listed Doctor Name — Descriptive Only")
        doctor_summary = (
            filtered_patients.groupby("department", as_index=False, observed=True)
            .agg(
                admission_records=("department", "size"),
                distinct_names=("doctor", "nunique"),
            )
        )
        doctor_summary["admissions_per_name"] = (
            doctor_summary["admission_records"]
            / doctor_summary["distinct_names"].replace(0, np.nan)
        )
        fig = px.bar(
            doctor_summary.sort_values("admissions_per_name"),
            x="admissions_per_name",
            y="department",
            orientation="h",
            title="Admissions per Distinct Listed Doctor Name",
            labels={
                "department": "Department",
                "admissions_per_name": "Admissions per Listed Name",
            },
            custom_data=["admission_records", "distinct_names"],
        )
        fig.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>Admissions per name: %{x:.2f}"
                "<br>Admissions: %{customdata[0]:,.0f}"
                "<br>Distinct names: %{customdata[1]:,.0f}<extra></extra>"
            )
        )
        show_figure(
            style_figure(fig, "Admissions per Listed Name", "Department"),
            "No listed-name summary is available.",
        )
        st.caption(
            "Listed names are descriptive source-data values, not staff "
            "availability, allocation, or staffing levels."
        )

    st.subheader("Resource Summary by Department — Source Data")
    st.dataframe(patient_department, width="stretch", hide_index=True)
    st.download_button(
        "Download Resource Summary",
        data=patient_department.to_csv(index=False).encode("utf-8"),
        file_name="hospital_resource_summary.csv",
        mime="text/csv",
    )

st.divider()
st.caption("MedTrack | Hospital Analytics Project")
