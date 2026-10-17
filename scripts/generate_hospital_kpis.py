
import pandas as pd
from pathlib import Path

# Get the project root directory
ROOT = Path(__file__).resolve().parent.parent

# Load the final cleaned CSV dataset
DATA_PATH = ROOT / "data" / "hospital_dashboard_demo_data.csv"
df = pd.read_csv(DATA_PATH)

print("\n========== HOSPITAL KPI REPORT ==========\n")

# 1. Total Admissions
total_admissions = len(df)
print(f"Total Admissions: {total_admissions}")

# 2. Average Length of Stay
if "length_of_stay" in df.columns:
    average_los = df["length_of_stay"].mean()
    print(f"Average Length of Stay: {average_los:.2f} days")
elif "length_of_stay_days_for_kpi" in df.columns:
    average_los = df["length_of_stay_days_for_kpi"].mean()
    print(f"Average Length of Stay: {average_los:.2f} days")
else:
    print("Average Length of Stay: N/A (column not found)")

# 3. Readmission Rate
print(
    "Readmission Rate: N/A "
    "(reliable patient IDs and admission history required)"
)

# 4. Bed Occupancy Rate
if {
    "demo_occupied_beds",
    "demo_available_beds"
}.issubset(df.columns):

    total_occupied = df["demo_occupied_beds"].sum()
    total_available = df["demo_available_beds"].sum()

    if total_available > 0:
        occupancy_rate = (
            total_occupied / total_available
        ) * 100
        print(f"Demo Bed Occupancy Rate: {occupancy_rate:.2f}%")
    else:
        print("Demo Bed Occupancy Rate: N/A")
else:
    print("Bed Occupancy Rate: N/A (bed data unavailable)")

# 5. Average Staff Count
if "demo_staff_count" in df.columns:
    print(
        f"Average Demo Staff Count: "
        f"{df['demo_staff_count'].mean():.2f}"
    )
else:
    print("Staff Count: N/A (staff data unavailable)")

# 6. Average Equipment Count
if "demo_equipment_available_count" in df.columns:
    print(
        f"Average Demo Equipment Count: "
        f"{df['demo_equipment_available_count'].mean():.2f}"
    )
else:
    print("Equipment Count: N/A (equipment data unavailable)")

# 7. Total Transfers
if "demo_transfer_count" in df.columns:
    print(
        f"Total Demo Transfers: "
        f"{df['demo_transfer_count'].sum()}"
    )
else:
    print("Transfer Count: N/A (transfer data unavailable)")

# 8. Department Efficiency
print(
    "Department Efficiency: N/A "
    "(actual department-level performance data required)"
)

print("\n=========================================\n")
