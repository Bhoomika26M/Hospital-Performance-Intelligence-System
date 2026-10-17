
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

patient_path = DATA_DIR / "hospital data analysis.csv"
resource_path = DATA_DIR / "hospital-resource-allocation-records.csv"

patients = pd.read_csv(patient_path)
resources = pd.read_csv(resource_path)

print("=" * 55)
print("MEDTRACK DV - KPI VALIDATION")
print("=" * 55)

# 1. PATIENT DATA VALIDATION
print("\n1. PATIENT DATA")
print("-" * 35)

print("Total patient records:", len(patients))
print("Duplicate rows:", patients.duplicated().sum())
print("Missing values:", patients.isna().sum().sum())

readmission_values = (
    patients["Readmission"].astype(str).str.strip().str.lower()
)
print("\nReadmission values:")
print(readmission_values.value_counts(dropna=False))

valid_readmission = readmission_values.isin(["yes", "no"])
print("Unrecognized readmission values:", (~valid_readmission).sum())

print("\nLength of stay:")
print(patients["Length_of_Stay"].describe())

print("Non-positive stay records:",
      (patients["Length_of_Stay"] <= 0).sum())

print("\nPatient outcome values:")
print(patients["Outcome"].value_counts(dropna=False))

# 2. RESOURCE DATA VALIDATION
print("\n2. RESOURCE DATA")
print("-" * 35)

print("Resource records:", len(resources))
print("Duplicate rows:", resources.duplicated().sum())
print("Missing values:", resources.isna().sum().sum())

print("\nZero or negative allocations:")
for col in ["beds_allocated", "staff_allocated"]:
    print(f"{col}: {(resources[col] <= 0).sum()} records")

# Compare occupied and allocated beds
over_capacity = resources[
    resources["beds_occupied"] > resources["beds_allocated"]
]

print("\nRecords where occupied beds exceed allocated beds:",
      len(over_capacity))

if not over_capacity.empty:
    print(over_capacity[
        ["hospital_name", "allocation_date",
         "beds_allocated", "beds_occupied"]
    ].head(10).to_string(index=False))

# Check whether resource records repeat the same hospital/date
print("\nRepeated hospital and allocation date combinations:")
print(
    resources.duplicated(
        subset=["hospital_id", "allocation_date"],
        keep=False
    ).sum()
)

# 3. RECOMPUTE OVERALL RATES
print("\n3. RECOMPUTED METRICS")
print("-" * 35)

total_beds = resources["beds_allocated"].sum()
occupied_beds = resources["beds_occupied"].sum()

if total_beds > 0:
    print("Bed occupancy rate:",
          round(occupied_beds / total_beds * 100, 2), "%")
else:
    print("Bed occupancy rate: Cannot calculate")

total_staff = resources["staff_allocated"].sum()
staff_on_duty = resources["staff_on_duty"].sum()

if total_staff > 0:
    print("Staff on-duty rate:",
          round(staff_on_duty / total_staff * 100, 2), "%")
else:
    print("Staff on-duty rate: Cannot calculate")

print("\nValidation completed.")
