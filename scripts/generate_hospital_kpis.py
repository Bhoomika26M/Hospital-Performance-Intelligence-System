
import pandas as pd
from pathlib import Path

# ==================================================
# 1. PROJECT PATHS
# ==================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

patient_path = DATA_DIR / "hospital data analysis.csv"
resource_path = DATA_DIR / "hospital-resource-allocation-records.csv"
output_path = DATA_DIR / "hospital_final_dataset.xlsx"


# ==================================================
# 2. LOAD DATASETS
# ==================================================
patients = pd.read_csv(patient_path)
resources = pd.read_csv(resource_path)

required_patient_cols = [
    "Readmission", "Length_of_Stay", "Cost", "Outcome"
]
required_resource_cols = [
    "beds_allocated", "beds_occupied",
    "staff_allocated", "staff_on_duty"
]

for col in required_patient_cols:
    if col not in patients.columns:
        raise ValueError(f"Missing patient column: {col}")

for col in required_resource_cols:
    if col not in resources.columns:
        raise ValueError(f"Missing resource column: {col}")

print("Datasets loaded successfully.")
print("Patient records:", len(patients))
print("Resource records:", len(resources))


# ==================================================
# 3. DATA VALIDATION
# ==================================================
readmission = (
    patients["Readmission"]
    .astype("string")
    .str.strip()
    .str.lower()
)

invalid_readmission = ~readmission.isin(["yes", "no"])

if invalid_readmission.any():
    raise ValueError(
        "Readmission contains missing or unrecognized values. "
        "Check the source data before calculating the KPI."
    )

patients["Readmission_Flag"] = readmission.map({
    "yes": 1,
    "no": 0
})

if patients["Length_of_Stay"].isna().any():
    raise ValueError("Length of stay contains missing values.")

if patients["Cost"].isna().any():
    raise ValueError("Patient cost contains missing values.")

if (patients["Length_of_Stay"] <= 0).any():
    raise ValueError("Non-positive length-of-stay values found.")

if (resources[required_resource_cols] < 0).any().any():
    raise ValueError(
        "Negative resource values found. Review the source data."
    )

if (resources["beds_occupied"] >
        resources["beds_allocated"]).any():
    raise ValueError(
        "Some records have more occupied than allocated beds."
    )

print("Validation checks passed.")


# ==================================================
# 4. PATIENT KPI ENGINEERING
# ==================================================
total_admissions = len(patients)

avg_length_of_stay = patients["Length_of_Stay"].mean()

readmission_rate = (
    patients["Readmission_Flag"].mean() * 100
)

avg_patient_cost = patients["Cost"].mean()

recovery_rate = (
    patients["Outcome"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("recovered")
    .mean() * 100
)


# ==================================================
# 5. RESOURCE KPI ENGINEERING
# ==================================================
# Individual record rates; zero allocations produce NaN.
resources["Bed_Occupancy_Rate"] = (
    resources["beds_occupied"]
    .div(
        resources["beds_allocated"].where(
            resources["beds_allocated"] > 0
        )
    ) * 100
)

resources["Staff_On_Duty_Rate"] = (
    resources["staff_on_duty"]
    .div(
        resources["staff_allocated"].where(
            resources["staff_allocated"] > 0
        )
    ) * 100
)

total_beds_allocated = resources["beds_allocated"].sum()
total_beds_occupied = resources["beds_occupied"].sum()

bed_occupancy_rate = (
    total_beds_occupied / total_beds_allocated * 100
    if total_beds_allocated > 0
    else float("nan")
)

total_staff_allocated = resources["staff_allocated"].sum()
total_staff_on_duty = resources["staff_on_duty"].sum()

staff_on_duty_rate = (
    total_staff_on_duty / total_staff_allocated * 100
    if total_staff_allocated > 0
    else float("nan")
)


# ==================================================
# 6. KPI SUMMARY
# ==================================================
kpis = pd.DataFrame({
    "KPI": [
        "Total Admissions",
        "Average Length of Stay",
        "Readmission Rate (%)",
        "Average Patient Cost",
        "Recovery Rate (%)",
        "Bed Occupancy Rate (%)",
        "Staff On-Duty Rate (%)"
    ],
    "Value": [
        total_admissions,
        avg_length_of_stay,
        readmission_rate,
        avg_patient_cost,
        recovery_rate,
        bed_occupancy_rate,
        staff_on_duty_rate
    ]
})


# ==================================================
# 7. KPI DEFINITIONS
# ==================================================
definitions = pd.DataFrame({
    "KPI": [
        "Total Admissions",
        "Average Length of Stay",
        "Readmission Rate (%)",
        "Average Patient Cost",
        "Recovery Rate (%)",
        "Bed Occupancy Rate (%)",
        "Staff On-Duty Rate (%)"
    ],
    "Definition": [
        "Number of patient records in the dataset.",
        "Mean of Length_of_Stay across patient records.",
        "Patients marked Yes for readmission / valid patient records × 100.",
        "Mean of Cost across patient records.",
        "Patients with outcome Recovered / patient records × 100.",
        "Total beds occupied / total beds allocated × 100.",
        "Total staff on duty / total staff allocated × 100."
    ],
    "Source": [
        "Patient Data",
        "Patient Data",
        "Patient Data",
        "Patient Data",
        "Patient Data",
        "Resource Data",
        "Resource Data"
    ]
})


# ==================================================
# 8. EXPORT TO EXCEL
# ==================================================
with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    patients.to_excel(
        writer, sheet_name="Patient Data", index=False
    )
    resources.to_excel(
        writer, sheet_name="Resource Data", index=False
    )
    kpis.to_excel(
        writer, sheet_name="KPI Summary", index=False
    )
    definitions.to_excel(
        writer, sheet_name="KPI Definitions", index=False
    )

print("\n" + "=" * 45)
print("KPI ENGINEERING COMPLETED")
print("=" * 45)
print(kpis.to_string(index=False))
print("\nKPI definitions added to the workbook.")
print("Created:", output_path)
