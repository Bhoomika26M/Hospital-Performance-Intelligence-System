
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "milestone3_data"

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    print(f"{name}: {status}")
    return condition

print("=" * 55)
print("MEDTRACK - HEALTHCARE METRICS VALIDATION")
print("=" * 55)

# ==========================================
# 1. DAILY OCCUPANCY VALIDATION
# ==========================================

occupancy = pd.read_csv(DATA_DIR / "daily_occupancy.csv")

print("\n1. DAILY OCCUPANCY VALIDATION")

print("Total records:", len(occupancy))

check(
    "No missing occupancy values",
    occupancy.isnull().sum().sum() == 0
)

# Check bed calculations
bed_check = (
    occupancy["total_beds"]
    == occupancy["occupied_beds"] + occupancy["available_beds"]
).all()

check("Total beds = Occupied + Available", bed_check)

# Check occupancy rate calculation
calculated_rate = (
    occupancy["occupied_beds"] / occupancy["total_beds"]
)

rate_check = (
    (calculated_rate - occupancy["occupancy_rate"]).abs()
    <= 0.00011
).all()

check("Occupancy rate calculation", rate_check)

check(
    "No zero or negative total beds",
    (occupancy["total_beds"] > 0).all()
)

check(
    "Occupied beds within total capacity",
    (
        (occupancy["occupied_beds"] >= 0)
        & (occupancy["occupied_beds"] <= occupancy["total_beds"])
    ).all()
)

check(
    "Available beds are non-negative",
    (occupancy["available_beds"] >= 0).all()
)

# Check duplicate daily department records
duplicate_occupancy = occupancy.duplicated(
    subset=["date", "hospital", "department"]
).sum()

print("Duplicate occupancy records:", duplicate_occupancy)

check(
    "No duplicate date-hospital-department records",
    duplicate_occupancy == 0
)

print(
    "Average occupancy rate (%):",
    round(occupancy["occupancy_rate"].mean() * 100, 2)
)

# ==========================================
# 2. READMISSION VALIDATION
# ==========================================

readmissions = pd.read_csv(
    DATA_DIR / "synthetic_patient_readmissions.csv"
)

print("\n2. READMISSION VALIDATION")

print("Total records:", len(readmissions))

check(
    "No missing patient IDs",
    readmissions["patient_id"].notna().all()
)

check(
    "No missing admission IDs",
    readmissions["admission_id"].notna().all()
)

check(
    "Readmission flags contain only 0 and 1",
    set(readmissions["readmission_flag"].dropna().unique())
    .issubset({0, 1})
)

check(
    "No duplicate admission IDs",
    readmissions["admission_id"].is_unique
)

previous_missing = (
    readmissions["previous_admission_date"].isna()
)

days_missing = (
    readmissions["days_since_previous_discharge"].isna()
)

check(
    "Previous admission and interval missing together",
    (previous_missing == days_missing).all()
)

check(
    "No negative days since previous discharge",
    (
        readmissions["days_since_previous_discharge"].dropna() >= 0
    ).all()
)

readmission_count = readmissions["readmission_flag"].sum()

print("Flagged readmissions:", readmission_count)

print(
    "Flagged record percentage (%):",
    round(readmissions["readmission_flag"].mean() * 100, 2)
)

print(
    "Note: This is a synthetic flagged-record percentage, "
    "not yet a validated clinical readmission rate."
)

# ==========================================
# 3. PATIENT TRANSFER VALIDATION
# ==========================================

transfers = pd.read_csv(
    DATA_DIR / "patient_transfers.csv"
)

print("\n3. PATIENT TRANSFER VALIDATION")

print("Total transfers:", len(transfers))

check(
    "No missing transfer values",
    transfers.isnull().sum().sum() == 0
)

check(
    "No duplicate transfer records",
    transfers.duplicated().sum() == 0
)

check(
    "Source and destination departments differ",
    (
        transfers["from_department"]
        != transfers["to_department"]
    ).all()
)

check(
    "No duplicate transfer IDs by admission and date",
    ~transfers.duplicated(
        subset=["admission_id", "transfer_date"]
    ).any()
)

print("\nTransfers by destination department:")
print(
    transfers["to_department"]
    .value_counts()
    .to_string()
)




# ==========================================
# 4. TRANSFER LINKAGE VALIDATION
# ==========================================

print("\n4. TRANSFER LINKAGE VALIDATION")

# Match transfers with their synthetic admissions
linked = transfers.merge(
    readmissions[
        ["admission_id", "patient_id", "hospital",
         "department", "admission_date", "discharge_date"]
    ],
    on="admission_id",
    how="left",
    suffixes=("_transfer", "_admission"),
    indicator=True
)

# Check whether every transfer has a matching admission
check(
    "All transfers linked to synthetic admissions",
    (linked["_merge"] == "both").all()
)

# Check patient ID consistency
check(
    "Transfer patient IDs match admissions",
    (
        linked["patient_id_transfer"]
        == linked["patient_id_admission"]
    ).all()
)

# Check hospital consistency
check(
    "Transfer hospital matches admission",
    (
        linked["hospital_transfer"]
        == linked["hospital_admission"]
    ).all()
)

# Check source department
check(
    "Source department matches admission department",
    (
        linked["from_department"]
        == linked["department"]
    ).all()
)

# Convert dates
linked["transfer_date"] = pd.to_datetime(
    linked["transfer_date"], errors="coerce"
)

linked["admission_date"] = pd.to_datetime(
    linked["admission_date"], errors="coerce"
)

linked["discharge_date"] = pd.to_datetime(
    linked["discharge_date"], errors="coerce"
)

# Check transfer date falls within admission period
check(
    "Transfer dates fall within admission period",
    (
        (linked["transfer_date"] >= linked["admission_date"])
        & (linked["transfer_date"] <= linked["discharge_date"])
    ).all()
)


# ==========================================
# 4. FINAL SUMMARY
# ==========================================

print("\n" + "=" * 55)
print("HEALTHCARE METRICS VALIDATION FINISHED")
print("=" * 55)

