
# MedTrack - Hospital Operations & Patient Analytics

from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Page settings
st.set_page_config(
    page_title="MedTrack Hospital Dashboard",
    page_icon="🏥",
    layout="wide"
)

# 2. Load the demo dataset
ROOT = Path(__file__).resolve().parent.parent
file_path = ROOT / "data" / "hospital_dashboard_demo_data.csv"

if not file_path.exists():
    st.error(f"CSV file not found: {file_path}")
    st.info("Run: python scripts/add_demo_resource_columns.py")
    st.stop()

df = pd.read_csv(file_path)

# 3. Prepare the data
df["date_of_admission"] = pd.to_datetime(
    df["date_of_admission"], errors="coerce"
)
df["discharge_date"] = pd.to_datetime(
    df["discharge_date"], errors="coerce"
)

for col in [
    "length_of_stay_days_for_kpi",
    "billing_amount",
    "demo_available_beds",
    "demo_occupied_beds",
    "demo_bed_occupancy_pct",
    "demo_staff_count",
    "demo_staff_working_hours",
    "demo_equipment_available_count",
    "demo_equipment_usage_hours",
    "demo_transfer_count"
]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["date_of_admission"]).copy()
df["year"] = df["date_of_admission"].dt.year
df["month"] = (
    df["date_of_admission"].dt.to_period("M").dt.to_timestamp()
)
df["month_name"] = df["date_of_admission"].dt.strftime("%b")

# 4. Dashboard navigation
st.title("🏥 MedTrack Hospital Analytics")

page = st.sidebar.radio(
    "Choose Dashboard",
    [
        "Hospital Overview",
        "Patient Flow",
        "Department Analytics",
        "Resource Utilization"
    ]
)

# 5. Global filters
st.sidebar.header("Filters")

years = sorted(df["year"].dropna().unique().tolist())
genders = sorted(df["gender"].dropna().astype(str).unique().tolist())
conditions = sorted(
    df["medical_condition"].dropna().astype(str).unique().tolist()
)

selected_years = st.sidebar.multiselect(
    "Admission Year", years, default=years
)
selected_genders = st.sidebar.multiselect(
    "Gender", genders, default=genders
)
selected_conditions = st.sidebar.multiselect(
    "Medical Condition", conditions, default=conditions
)

filtered = df[
    df["year"].isin(selected_years)
    & df["gender"].astype(str).isin(selected_genders)
    & df["medical_condition"].astype(str).isin(selected_conditions)
].copy()

if filtered.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

st.caption(f"Records displayed: {len(filtered):,}")

# 6. Common KPIs
total_admissions = len(filtered)
average_stay = filtered["length_of_stay_days_for_kpi"].mean()
total_billing = filtered["billing_amount"].sum()
average_billing = filtered["billing_amount"].mean()

# Monthly admissions: only months with actual admission records
monthly_admissions = (
    filtered.groupby("month")
    .size()
    .reset_index(name="Admissions")
    .sort_values("month")
)

# Helper function to prevent crowded monthly labels
def format_month_axis(fig):
    fig.update_xaxes(
        tickformat="%b %Y",
        nticks=8,
        tickangle=-45
    )
    fig.update_layout(xaxis_title="Month")
    return fig


# 7. Hospital Overview
if page == "Hospital Overview":

    st.subheader("Hospital Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Admissions", f"{total_admissions:,}")
    c2.metric(
        "Average Stay",
        f"{average_stay:.2f} days"
        if pd.notna(average_stay) else "N/A"
    )
    c3.metric(
        "Total Billing",
        f"{total_billing:,.0f}"
        if pd.notna(total_billing) else "N/A"
    )
    c4.metric(
        "Average Billing",
        f"{average_billing:,.0f}"
        if pd.notna(average_billing) else "N/A"
    )

    st.caption(
        "Billing has no confirmed currency label. "
        "Resource and department demo values are simulated."
    )

    # Monthly admission trend: only months with records
    fig = px.line(
        monthly_admissions,
        x="month",
        y="Admissions",
        markers=True,
        title="Monthly Admission Trend",
        labels={
            "month": "Month",
            "Admissions": "Admissions"
        }
    )

    format_month_axis(fig)
    fig.update_layout(yaxis_title="Number of Admissions")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        type_data = (
            filtered.groupby("admission_type")
            .size()
            .reset_index(name="Admissions")
        )

        fig = px.pie(
            type_data,
            names="admission_type",
            values="Admissions",
            hole=0.45,
            title="Admissions by Type"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        condition_data = (
            filtered.groupby("medical_condition")
            .size()
            .reset_index(name="Admissions")
        )

        fig = px.pie(
            condition_data,
            names="medical_condition",
            values="Admissions",
            hole=0.45,
            title="Admissions by Medical Condition"
        )
        st.plotly_chart(fig, use_container_width=True)


# 8. Patient Flow
elif page == "Patient Flow":

    st.subheader("Patient Flow")

    c1, c2, c3 = st.columns(3)
    c1.metric("Admissions", f"{total_admissions:,}")
    c2.metric(
        "Records with Discharge Dates",
        f"{filtered['discharge_date'].notna().sum():,}"
    )
    c3.metric(
        "Average Stay",
        f"{average_stay:.2f} days"
        if pd.notna(average_stay) else "N/A"
    )

    # Monthly admissions
    admissions = (
        filtered.groupby("month")
        .size()
        .rename("Admissions")
    )

    # Monthly discharges
    discharge_data = filtered.dropna(
        subset=["discharge_date"]
    ).copy()

    discharge_data["discharge_month"] = (
        discharge_data["discharge_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    discharges = (
        discharge_data.groupby("discharge_month")
        .size()
        .rename("Discharges")
    )

    # Combine the two series and keep only months with records
    flow = pd.concat([admissions, discharges], axis=1)
    flow.index.name = "Month"
    flow = flow.dropna(how="all").fillna(0).reset_index()
    flow = flow.sort_values("Month")

    fig = px.line(
        flow,
        x="Month",
        y=["Admissions", "Discharges"],
        markers=True,
        title="Monthly Admissions vs Discharges",
        labels={
            "Month": "Month",
            "value": "Number of Records",
            "variable": "Category"
        }
    )

    format_month_axis(fig)
    fig.update_layout(
        yaxis_title="Number of Records",
        legend_title_text="Category"
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        stay_data = filtered.dropna(
            subset=["length_of_stay_days_for_kpi"]
        )

        fig = px.box(
            stay_data,
            x="admission_type",
            y="length_of_stay_days_for_kpi",
            color="admission_type",
            title="Length of Stay by Admission Type",
            labels={
                "admission_type": "Admission Type",
                "length_of_stay_days_for_kpi": "Stay (Days)"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        daily = (
            filtered.groupby(
                filtered["date_of_admission"].dt.date
            )
            .size()
            .reset_index(name="Admissions")
        )
        daily.columns = ["Admission Date", "Admissions"]

        fig = px.scatter(
            daily,
            x="Admission Date",
            y="Admissions",
            title="Daily Admission Pattern"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Demonstration transfer data
    st.subheader("Patient Transfer Demonstration")

    transfer_total = filtered["demo_transfer_count"].sum()
    st.metric("Simulated Transfers", f"{transfer_total:,.0f}")

    transfer_data = (
        filtered.groupby("demo_transfer_destination")
        .size()
        .reset_index(name="Records")
    )

    fig = px.pie(
        transfer_data,
        names="demo_transfer_destination",
        values="Records",
        hole=0.4,
        title="Simulated Transfer Destinations"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Transfer values and destinations are simulated for demonstration; "
        "they are not actual patient movement records."
    )


# 9. Department Analytics
elif page == "Department Analytics":

    st.subheader("Department Analytics")

    st.warning(
        "All department assignments in this view are simulated. "
        "They do not represent verified hospital departments."
    )

    department_data = filtered.groupby("demo_department").agg(
        Admissions=("demo_department", "size"),
        Average_Stay=("length_of_stay_days_for_kpi", "mean"),
        Average_Billing=("billing_amount", "mean")
    ).reset_index()

    c1, c2 = st.columns(2)

    with c1:
        fig = px.pie(
            department_data,
            names="demo_department",
            values="Admissions",
            hole=0.4,
            title="Admission Share by Demo Department"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.box(
            filtered,
            x="demo_department",
            y="length_of_stay_days_for_kpi",
            color="demo_department",
            title="Length of Stay by Demo Department",
            labels={
                "demo_department": "Demo Department",
                "length_of_stay_days_for_kpi": "Stay (Days)"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(
        department_data,
        x="Average_Stay",
        y="Average_Billing",
        size="Admissions",
        color="demo_department",
        hover_name="demo_department",
        title="Average Stay vs Average Billing",
        labels={
            "Average_Stay": "Average Stay (Days)",
            "Average_Billing": "Average Billing",
            "Admissions": "Admissions"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        department_data,
        use_container_width=True,
        hide_index=True
    )


# 10. Resource Utilization
else:

    st.subheader("Resource Utilization")

    st.warning(
        "The bed, staff, and equipment values shown here are simulated "
        "for dashboard demonstration, not actual hospital measurements."
    )

    # Calculate demonstration metrics from simulated values
    available_beds = filtered["demo_available_beds"].sum()
    occupied_beds = filtered["demo_occupied_beds"].sum()

    occupancy = (
        occupied_beds / available_beds * 100
        if available_beds > 0 else 0
    )

    avg_staff = filtered["demo_staff_count"].mean()
    equipment_count = filtered["demo_equipment_available_count"].mean()
    equipment_hours = filtered["demo_equipment_usage_hours"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Admissions", f"{total_admissions:,}")
    c2.metric("Demo Occupancy Ratio", f"{occupancy:.1f}%")
    c3.metric("Average Demo Staff Count", f"{avg_staff:.1f}")
    c4.metric("Average Demo Equipment Count", f"{equipment_count:.1f}")

    st.caption(
        "The occupancy ratio is calculated from simulated record-level "
        "counts, not from a daily occupied-bed census."
    )

    # Monthly workload: only months with admission records
    monthly_workload = (
        filtered.groupby("month")
        .agg(
            Admissions=("date_of_admission", "size"),
            Estimated_Stay_Days=(
                "length_of_stay_days_for_kpi", "sum"
            ),
            Average_Staff=("demo_staff_count", "mean"),
            Equipment_Hours=("demo_equipment_usage_hours", "mean")
        )
        .reset_index()
        .sort_values("month")
    )

    # Monthly admission workload area chart
    fig = px.area(
        monthly_workload,
        x="month",
        y="Admissions",
        title="Monthly Admission Workload",
        labels={
            "month": "Month",
            "Admissions": "Admissions"
        }
    )

    format_month_axis(fig)
    fig.update_layout(yaxis_title="Number of Admissions")
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap of monthly admission counts
    # Intentionally retains all 12 calendar months
    heatmap_data = filtered.copy()
    heatmap_data["Month_Name"] = (
        heatmap_data["date_of_admission"].dt.month
    )

    heatmap = heatmap_data.pivot_table(
        index="year",
        columns="Month_Name",
        values="date_of_admission",
        aggfunc="count",
        fill_value=0
    ).reindex(columns=range(1, 13), fill_value=0)

    heatmap.columns = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    fig = px.imshow(
        heatmap,
        aspect="auto",
        color_continuous_scale="Blues",
        title="Admission Workload Heatmap",
        labels={
            "x": "Month",
            "y": "Year",
            "color": "Admissions"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    # Monthly workload comparison
    fig = px.scatter(
        monthly_workload,
        x="Admissions",
        y="Estimated_Stay_Days",
        hover_data=["month"],
        title="Monthly Admissions vs Estimated Stay-Days",
        labels={
            "Admissions": "Admissions",
            "Estimated_Stay_Days": "Estimated Stay-Days",
            "month": "Month"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    # Simulated staff and equipment summaries
    c1, c2 = st.columns(2)

    with c1:
        fig = px.line(
            monthly_workload,
            x="month",
            y="Average_Staff",
            markers=True,
            title="Average Simulated Staff Count by Month",
            labels={
                "month": "Month",
                "Average_Staff": "Average Staff Count"
            }
        )
        format_month_axis(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.line(
            monthly_workload,
            x="month",
            y="Equipment_Hours",
            markers=True,
            title="Average Simulated Equipment Usage Hours",
            labels={
                "month": "Month",
                "Equipment_Hours": "Average Usage Hours"
            }
        )
        format_month_axis(fig)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("About the demo data"):
        st.markdown("""
        - Bed occupancy uses simulated occupied and available bed counts.
        - Staff counts and working hours are simulated.
        - Equipment availability and usage hours are simulated.
        - Department assignments and transfer destinations are simulated.
        - These values demonstrate charts and calculations only; they are
          not suitable for real hospital operational conclusions.
        """)

# 11. Footer
st.sidebar.divider()
st.sidebar.caption("MedTrack | Milestone 3")
