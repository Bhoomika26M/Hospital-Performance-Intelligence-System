import re
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Patient Flow | MedTrack",
    page_icon="📈",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
TRANSFER_FILE = BASE_DIR / "milestone3_data" / "patient_transfers.csv"
OCCUPANCY_FILE = BASE_DIR / "milestone3_data" / "daily_occupancy.csv"

TRANSFER_COLUMNS = (
    "patient_id",
    "admission_id",
    "hospital",
    "from_department",
    "to_department",
    "transfer_date",
    "transfer_reason",
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
    for column in ("length_of_stay",):
        if column in patients.columns:
            patients[column] = pd.to_numeric(
                patients[column], errors="coerce"
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


def filter_rows(
    data: pd.DataFrame,
    date_column: str,
    selected_date_range,
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
    if selected_date_range and date_column in filtered_data.columns:
        start_date, end_date = selected_date_range
        filtered_data = filtered_data[
            filtered_data[date_column].notna()
            & filtered_data[date_column].dt.date.between(
                start_date, end_date
            )
        ]
    return filtered_data


def style_figure(
    figure: go.Figure,
    x_title: str,
    y_title: str,
    legend_title: str = "",
):
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

transfers = load_supplementary_data(
    str(TRANSFER_FILE),
    file_modified_time(TRANSFER_FILE),
    TRANSFER_COLUMNS,
)
occupancy = load_supplementary_data(
    str(OCCUPANCY_FILE),
    file_modified_time(OCCUPANCY_FILE),
    OCCUPANCY_COLUMNS,
)

missing_patient_columns = {
    "date_of_admission",
    "discharge_date",
    "department",
    "hospital",
    "admission_type",
    "length_of_stay",
} - set(patients.columns)
if missing_patient_columns:
    st.error(
        "hospital_cleaned.csv is missing required columns: "
        + ", ".join(sorted(missing_patient_columns))
    )
    st.stop()

for data, expected_columns, label in (
    (transfers, TRANSFER_COLUMNS, "transfer"),
    (occupancy, OCCUPANCY_COLUMNS, "occupancy"),
):
    missing_columns = set(expected_columns) - set(data.columns)
    if missing_columns:
        st.warning(
            f"Synthetic {label} data is missing columns: "
            + ", ".join(sorted(missing_columns))
        )
        if label == "transfer":
            transfers = pd.DataFrame(columns=TRANSFER_COLUMNS)
        else:
            occupancy = pd.DataFrame(columns=OCCUPANCY_COLUMNS)

for data, date_columns, numeric_columns in (
    (transfers, ("transfer_date",), ()),
    (
        occupancy,
        ("date",),
        ("total_beds", "occupied_beds", "available_beds"),
    ),
):
    for column in date_columns:
        if column in data.columns:
            data[column] = pd.to_datetime(data[column], errors="coerce")
    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors="coerce")

if not TRANSFER_FILE.is_file():
    st.warning(
        "Synthetic transfer data is unavailable: "
        "milestone3_data/patient_transfers.csv was not found."
    )
if not OCCUPANCY_FILE.is_file():
    st.warning(
        "Synthetic occupancy data is unavailable: "
        "milestone3_data/daily_occupancy.csv was not found."
    )

st.sidebar.title("🏥 MedTrack")
st.sidebar.caption("Patient Flow Analytics")
st.sidebar.divider()
st.sidebar.subheader("Dashboard Filters")

date_series = [
    patients["date_of_admission"].dropna(),
    patients["discharge_date"].dropna(),
    transfers["transfer_date"].dropna()
    if "transfer_date" in transfers.columns
    else pd.Series(dtype="datetime64[ns]"),
    occupancy["date"].dropna()
    if "date" in occupancy.columns
    else pd.Series(dtype="datetime64[ns]"),
]
available_dates = pd.concat(date_series, ignore_index=True).dropna()
selected_date_range = None
if not available_dates.empty:
    min_date = available_dates.min().date()
    max_date = available_dates.max().date()
    date_input = st.sidebar.date_input(
        "Event Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if isinstance(date_input, (tuple, list)) and len(date_input) == 2:
        selected_date_range = (date_input[0], date_input[1])

department_values = set(patients["department"].dropna().astype(str))
if "department" in occupancy.columns:
    department_values.update(occupancy["department"].dropna().astype(str))
for column in ("from_department", "to_department"):
    if column in transfers.columns:
        department_values.update(transfers[column].dropna().astype(str))
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

patient_scope = patients.copy()
patient_scope = patient_scope[
    patient_scope["department"].isin(selected_departments)
]
if hospital_search:
    patient_scope = patient_scope[
        patient_scope["hospital"].astype("string").str.contains(
            re.escape(hospital_search),
            case=False,
            na=False,
            regex=True,
        )
    ]

if "admission_type" in patient_scope.columns:
    admission_type_options = sorted(
        patient_scope["admission_type"].dropna().astype(str).unique()
    )
    selected_admission_types = st.sidebar.multiselect(
        "Admission Type",
        admission_type_options,
        default=admission_type_options,
    )
    patient_scope = patient_scope[
        patient_scope["admission_type"].isin(selected_admission_types)
    ]

if "medical_condition" in patient_scope.columns:
    condition_options = sorted(
        patient_scope["medical_condition"].dropna().astype(str).unique()
    )
    selected_conditions = st.sidebar.multiselect(
        "Medical Condition",
        condition_options,
        default=condition_options,
    )
    patient_scope = patient_scope[
        patient_scope["medical_condition"].isin(selected_conditions)
    ]

admission_records = filter_rows(
    patient_scope,
    "date_of_admission",
    selected_date_range,
    selected_departments,
    hospital_search,
)
discharge_records = filter_rows(
    patient_scope,
    "discharge_date",
    selected_date_range,
    selected_departments,
    hospital_search,
)
filtered_transfers = transfers.copy()
if hospital_search and "hospital" in filtered_transfers.columns:
    filtered_transfers = filtered_transfers[
        filtered_transfers["hospital"].astype("string").str.contains(
            re.escape(hospital_search),
            case=False,
            na=False,
            regex=True,
        )
    ]
filtered_transfers = filtered_transfers[
    filtered_transfers["from_department"].isin(selected_departments)
    | filtered_transfers["to_department"].isin(selected_departments)
]
if selected_date_range:
    start_date, end_date = selected_date_range
    filtered_transfers = filtered_transfers[
        filtered_transfers["transfer_date"].notna()
        & filtered_transfers["transfer_date"].dt.date.between(
            start_date, end_date
        )
    ]

filtered_occupancy = filter_rows(
    occupancy,
    "date",
    selected_date_range,
    selected_departments,
    hospital_search,
)
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
        "Synthetic occupancy rows with missing or invalid bed counts are "
        "excluded from the occupancy analysis."
    )

st.title("📈 Patient Flow Analytics")
st.markdown(
    "Explore admissions, discharges, department stays, and synthetic "
    "demonstrations of patient movement and occupancy."
)
st.divider()

total_admissions = len(admission_records)
average_stay = admission_records["length_of_stay"].mean()
valid_admissions = admission_records["date_of_admission"].notna().sum()
valid_discharges = discharge_records["discharge_date"].notna().sum()
kpi_columns = st.columns(4)
kpi_columns[0].metric("Admission Records", f"{total_admissions:,}")
kpi_columns[1].metric(
    "Average Length of Stay",
    f"{average_stay:.1f} days" if pd.notna(average_stay) else "N/A",
)
kpi_columns[2].metric("Admissions in Range", f"{valid_admissions:,}")
kpi_columns[3].metric("Discharges in Range", f"{valid_discharges:,}")

st.info(
    "Transfers and occupancy below use synthetic demonstration data. They "
    "are filtered independently and are not linked to the source patient "
    "records. Do not interpret them as actual hospital operations."
)
st.divider()

left, right = st.columns(2)
with left:
    st.subheader("Monthly Admission Trends")
    admission_dates = admission_records.dropna(
        subset=["date_of_admission"]
    ).copy()
    if admission_dates.empty:
        show_figure(None, "No admissions match the selected filters.")
    else:
        admission_dates["month"] = (
            admission_dates["date_of_admission"].dt.to_period("M").dt.to_timestamp()
        )
        monthly_admissions = (
            admission_dates.groupby(["month", "department"])
            .size()
            .reset_index(name="admissions")
        )
        figure = px.line(
            monthly_admissions,
            x="month",
            y="admissions",
            color="department",
            markers=True,
            title="Monthly Admission Volume by Department",
            labels={
                "month": "Admission Month",
                "admissions": "Admission Records",
                "department": "Department",
            },
        )
        show_figure(
            style_figure(
                figure, "Admission Month", "Admission Records", "Department"
            ),
            "No monthly admission trend is available.",
        )

with right:
    st.subheader("Monthly Admissions vs. Discharges")
    monthly_events = []
    for data, date_column, event_name in (
        (admission_records, "date_of_admission", "Admissions"),
        (discharge_records, "discharge_date", "Discharges"),
    ):
        event_data = data.dropna(subset=[date_column]).copy()
        if not event_data.empty:
            event_data["month"] = (
                event_data[date_column].dt.to_period("M").dt.to_timestamp()
            )
            counts = event_data.groupby("month").size().reset_index(name="count")
            counts["event"] = event_name
            monthly_events.append(counts)
    if not monthly_events:
        show_figure(None, "No admission or discharge events match the filters.")
    else:
        event_comparison = pd.concat(monthly_events, ignore_index=True)
        figure = px.line(
            event_comparison,
            x="month",
            y="count",
            color="event",
            markers=True,
            title="Monthly Admission and Discharge Volume",
            labels={
                "month": "Event Month",
                "count": "Patient Records",
                "event": "Event",
            },
        )
        show_figure(
            style_figure(figure, "Event Month", "Patient Records", "Event"),
            "No monthly event comparison is available.",
        )

left, right = st.columns(2)
with left:
    st.subheader("Admission Type Distribution")
    admission_type_counts = (
        admission_records["admission_type"]
        .value_counts()
        .rename_axis("admission_type")
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
                "admissions": "Admission Records",
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
            style_figure(
                figure, "", "Admission Records", "Admission Type"
            ),
            "No admission type distribution is available.",
        )

with right:
    st.subheader("Average Length of Stay by Department")
    stay_data = admission_records.dropna(
        subset=["department", "length_of_stay"]
    )
    if stay_data.empty:
        show_figure(None, "No length-of-stay records match the filters.")
    else:
        stay_summary = (
            stay_data.groupby("department", as_index=False)
            .agg(
                average_stay=("length_of_stay", "mean"),
                records=("length_of_stay", "size"),
            )
            .sort_values("average_stay", ascending=True)
        )
        figure = px.bar(
            stay_summary,
            x="average_stay",
            y="department",
            orientation="h",
            title="Average Stay by Department",
            labels={
                "department": "Department",
                "average_stay": "Average Stay (Days)",
                "records": "Admission Records",
            },
            text="average_stay",
            custom_data=["records"],
        )
        figure.update_traces(
            texttemplate="%{x:.1f} days",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b><br>Average stay: %{x:.2f} days"
                "<br>Records: %{customdata[0]:,.0f}<extra></extra>"
            ),
        )
        show_figure(
            style_figure(figure, "Average Stay (Days)", "Department"),
            "No department stay averages are available.",
        )

st.subheader("Length-of-Stay Distribution")
valid_stays = admission_records.dropna(subset=["length_of_stay"])
if valid_stays.empty:
    show_figure(None, "No length-of-stay records match the filters.")
else:
    figure = px.histogram(
        valid_stays,
        x="length_of_stay",
        color="department",
        nbins=30,
        marginal="box",
        title="Distribution of Length of Stay",
        labels={
            "length_of_stay": "Length of Stay (Days)",
            "count": "Admission Records",
            "department": "Department",
        },
        hover_data={"length_of_stay": ":.1f"},
    )
    show_figure(
        style_figure(
            figure, "Length of Stay (Days)", "Admission Records", "Department"
        ),
        "No length-of-stay distribution is available.",
    )

st.header("Patient Movement (Synthetic)")
st.caption(
    "Synthetic transfers link only to synthetic admissions. They are not "
    "joined to the source patient dataset and are not actual transfer events."
)
left, right = st.columns(2)
with left:
    st.subheader("Transfers by Department")
    if filtered_transfers.empty:
        show_figure(None, "No synthetic transfers match the selected filters.")
    else:
        transfer_departments = pd.concat(
            [
                filtered_transfers["from_department"].rename("department"),
                filtered_transfers["to_department"].rename("department"),
            ],
            ignore_index=True,
        )
        transfer_counts = (
            transfer_departments.value_counts()
            .rename_axis("department")
            .reset_index(name="transfer endpoints")
            .sort_values("transfer endpoints", ascending=True)
        )
        figure = px.bar(
            transfer_counts,
            x="transfer endpoints",
            y="department",
            orientation="h",
            title="Synthetic Transfer Endpoints by Department",
            labels={
                "department": "Department",
                "transfer endpoints": "Transfer Endpoints",
            },
            text="transfer endpoints",
        )
        figure.update_traces(textposition="outside", cliponaxis=False)
        show_figure(
            style_figure(figure, "Transfer Endpoints", "Department"),
            "No department transfer counts are available.",
        )

with right:
    st.subheader("Transfers by Reason")
    if filtered_transfers.empty:
        show_figure(None, "No synthetic transfers match the selected filters.")
    else:
        transfer_reasons = (
            filtered_transfers["transfer_reason"]
            .value_counts()
            .rename_axis("reason")
            .reset_index(name="transfers")
            .sort_values("transfers", ascending=True)
        )
        figure = px.bar(
            transfer_reasons,
            x="transfers",
            y="reason",
            orientation="h",
            title="Synthetic Transfers by Reason",
            labels={"reason": "Transfer Reason", "transfers": "Transfers"},
            text="transfers",
        )
        figure.update_traces(textposition="outside", cliponaxis=False)
        show_figure(
            style_figure(figure, "Transfers", "Transfer Reason"),
            "No synthetic transfer reasons are available.",
        )

st.subheader("Department-to-Department Movement (Synthetic)")
if filtered_transfers.empty:
    show_figure(None, "No synthetic transfers match the selected filters.")
else:
    movement = (
        filtered_transfers.groupby(
            ["from_department", "to_department"], as_index=False
        )
        .size()
        .rename(columns={"size": "transfers"})
    )
    department_volume = (
        pd.concat(
            [
                movement[["from_department", "transfers"]].rename(
                    columns={"from_department": "department"}
                ),
                movement[["to_department", "transfers"]].rename(
                    columns={"to_department": "department"}
                ),
            ],
            ignore_index=True,
        )
        .groupby("department")["transfers"]
        .sum()
        .sort_values(ascending=False, kind="stable")
    )
    departments = department_volume.index.tolist()
    department_indices = {
        department: index for index, department in enumerate(departments)
    }
    department_colors = {
        "Cardiology": "#38BDF8",
        "Endocrinology": "#A78BFA",
        "General Medicine": "#34D399",
        "Oncology": "#FB7185",
        "Pulmonology": "#FBBF24",
        "Rheumatology": "#2DD4BF",
    }
    colors = [
        department_colors.get(department, "#CBD5E1")
        for department in departments
    ]
    link_colors = [
        (
            f"rgba("
            f"{int(department_colors.get(source, '#CBD5E1')[1:3], 16)},"
            f"{int(department_colors.get(source, '#CBD5E1')[3:5], 16)},"
            f"{int(department_colors.get(source, '#CBD5E1')[5:7], 16)},"
            "0.30)"
        )
        for source in movement["from_department"]
    ]
    node_y = [
        index / (len(departments) - 1) if len(departments) > 1 else 0.5
        for index in range(len(departments))
    ]
    figure = go.Figure(
        data=[
            go.Sankey(
                arrangement="fixed",
                node=dict(
                    label=departments + departments,
                    color=colors + colors,
                    x=[0.02] * len(departments)
                    + [0.82] * len(departments),
                    y=node_y + node_y,
                    pad=28,
                    thickness=22,
                    line=dict(color="rgba(226,232,240,0.7)", width=1),
                ),
                link=dict(
                    source=[
                        department_indices[value]
                        for value in movement["from_department"]
                    ],
                    target=[
                        len(departments) + department_indices[value]
                        for value in movement["to_department"]
                    ],
                    value=movement["transfers"],
                    color=link_colors,
                    hovertemplate=(
                        "Source department: %{source.label}"
                        "<br>Destination department: %{target.label}"
                        "<br>Synthetic transfer count: %{value:,}"
                        "<extra></extra>"
                    ),
                ),
            )
        ]
    )
    figure.update_layout(
        template="plotly_dark",
        title="Synthetic Transfer Flow Between Departments",
        height=720,
        margin=dict(l=30, r=30, t=100, b=35),
        hoverlabel=dict(namelength=-1),
        annotations=[
            dict(
                x=0.02,
                y=1.08,
                xref="paper",
                yref="paper",
                text="SOURCE DEPARTMENT",
                showarrow=False,
                xanchor="left",
                font=dict(color="#CBD5E1", size=12),
            ),
            dict(
                x=0.82,
                y=1.08,
                xref="paper",
                yref="paper",
                text="DESTINATION DEPARTMENT",
                showarrow=False,
                xanchor="left",
                font=dict(color="#CBD5E1", size=12),
            ),
        ],
    )
    st.plotly_chart(
        figure,
        width="stretch",
        config={"displayModeBar": False},
    )

st.header("Peak Patient Load (Synthetic Occupancy)")
st.caption(
    "Occupancy observations are synthetic demonstrations, not actual bed "
    "capacity or hospital census records."
)
if valid_occupancy.empty:
    st.info("No synthetic occupancy records match the selected filters.")
else:
    monthly_occupancy = (
        valid_occupancy.assign(
            month=valid_occupancy["date"].dt.to_period("M").dt.to_timestamp()
        )
        .groupby("month", as_index=False)
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
    peak_row = monthly_occupancy.loc[
        monthly_occupancy["occupancy_rate"].idxmax()
    ]
    st.metric(
        "Highest Monthly Synthetic Occupancy",
        f"{peak_row['occupancy_rate']:.1f}%",
        help=(
            f"{peak_row['month']:%B %Y}; weighted by total beds. "
            "Synthetic demonstration only."
        ),
    )
    figure = px.area(
        monthly_occupancy,
        x="month",
        y="occupancy_rate",
        title="Monthly Weighted Occupancy Trend (Synthetic)",
        labels={
            "month": "Month",
            "occupancy_rate": "Occupancy Rate (%)",
            "occupied_beds": "Occupied Beds",
            "total_beds": "Total Beds",
        },
        custom_data=["occupied_beds", "total_beds"],
    )
    figure.add_scatter(
        x=[peak_row["month"]],
        y=[peak_row["occupancy_rate"]],
        mode="markers",
        marker=dict(color="#ef4444", size=11, symbol="diamond"),
        name="Peak month",
        hovertemplate=(
            "Peak: %{x|%B %Y}<br>Occupancy: %{y:.1f}%<extra></extra>"
        ),
    )
    figure.update_traces(
        selector=dict(type="scatter", mode="lines"),
        hovertemplate=(
            "%{x|%B %Y}<br>Occupancy: %{y:.1f}%"
            "<br>Occupied beds: %{customdata[0]:,.0f}"
            "<br>Total beds: %{customdata[1]:,.0f}<extra></extra>"
        ),
    )
    figure.update_yaxes(ticksuffix="%", rangemode="tozero")
    show_figure(
        style_figure(figure, "Month", "Occupancy Rate (%)"),
        "No monthly occupancy trend is available.",
    )
    st.caption(
        f"Highest filtered synthetic occupancy month: "
        f"{peak_row['month']:%B %Y} ({peak_row['occupancy_rate']:.1f}%). "
        "Rates are weighted as total occupied beds ÷ total beds."
    )

st.divider()
st.subheader("Patient Flow Records")
if admission_records.empty:
    st.info("No admission records match the selected filters.")
else:
    columns_to_show = [
        column
        for column in (
            "name",
            "medical_condition",
            "admission_type",
            "date_of_admission",
            "discharge_date",
            "length_of_stay",
        )
        if column in admission_records.columns
    ]
    st.dataframe(
        admission_records[columns_to_show],
        width="stretch",
        hide_index=True,
    )

st.download_button(
    "Download Patient Flow Data",
    data=admission_records.to_csv(index=False).encode("utf-8"),
    file_name="patient_flow_data.csv",
    mime="text/csv",
)

st.divider()
st.caption("MedTrack | Patient Flow Analytics")
