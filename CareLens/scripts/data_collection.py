"""Milestone 1 / Module 1 - collect and integrate the raw datasets.

Reads every file in data/raw/, checks the columns and completeness, joins the
department mapping onto the admissions and writes data/hospital_raw_data.csv.
"""
import sys
import pandas as pd
from config import RAW, DATA, CONDITION_TO_DEPT

FILES = {
    "healthcare_dataset.csv": ["Name", "Age", "Gender", "Medical Condition", "Date of Admission",
                               "Discharge Date", "Admission Type", "Billing Amount", "Room Number"],
    "department_master.csv": ["department", "licensed_beds", "target_los_days"],
    "hospital_resource_raw.csv": ["month", "department", "staffed_beds", "nurses_on_duty"],
    "patient_feedback_raw.csv": ["month", "department", "avg_satisfaction", "avg_wait_minutes"],
}

print(f"{'file':32}{'rows':>9}{'completeness':>15}")
ok = True
for name, needed in FILES.items():
    df = pd.read_csv(RAW / name)
    missing_cols = [c for c in needed if c not in df.columns]
    if missing_cols:
        sys.exit(f"{name} is missing columns: {missing_cols}")
    complete = 100 * (1 - df.isna().sum().sum() / df.size)
    ok &= complete > 95
    print(f"{name:32}{len(df):>9}{complete:>14.2f}%")

adm = pd.read_csv(RAW / "healthcare_dataset.csv")
adm["Department"] = adm["Medical Condition"].map(CONDITION_TO_DEPT)
adm["Floor"] = adm["Room Number"] // 100              # rooms 101-500 -> floors 1-5
adm.to_csv(DATA / "hospital_raw_data.csv", index=False)
print(f"\nhospital_raw_data.csv written: {len(adm):,} rows")
print("Completeness above 95% for every file:", "YES" if ok else "NO")
