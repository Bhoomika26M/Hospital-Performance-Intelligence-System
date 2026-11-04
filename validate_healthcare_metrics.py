
import pandas as pd
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "milestone3_data"
validation_results = []

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    print(f"{name}: {status}")
    validation_results.append((name, bool(condition)))
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

# Convert numeric inputs safely so missing or malformed values do not crash
# KPI validation or silently enter aggregate denominators.
total_beds = pd.to_numeric(occupancy["total_beds"], errors="coerce")
occupied_beds = pd.to_numeric(occupancy["occupied_beds"], errors="coerce")
available_beds = pd.to_numeric(occupancy["available_beds"], errors="coerce")
occupancy_rate_values = pd.to_numeric(
    occupancy["occupancy_rate"], errors="coerce"
)

# Check bed calculations
bed_values_present = (
    total_beds.notna() & occupied_beds.notna() & available_beds.notna()
)
bed_check = (
    bed_values_present
    & total_beds.eq(occupied_beds + available_beds)
).all()

check("Total beds = Occupied + Available", bed_check)

# Check occupancy rate calculation
valid_bed_rows = (
    total_beds.notna()
    & occupied_beds.notna()
    & total_beds.gt(0)
    & occupied_beds.ge(0)
    & occupied_beds.le(total_beds)
)
calculated_rate = occupied_beds[valid_bed_rows] / total_beds[valid_bed_rows]
stored_rate = occupancy_rate_values[valid_bed_rows]

rate_check = (
    len(calculated_rate) == len(occupancy)
    and stored_rate.notna().all()
    and ((calculated_rate - stored_rate).abs() <= 0.00011).all()
)

check("Occupancy rate calculation", rate_check)

check(
    "No zero or negative total beds",
    total_beds.notna().all() and total_beds.gt(0).all()
)

check(
    "Occupied beds within total capacity",
    (
        occupied_beds.notna()
        & occupied_beds.ge(0)
        & occupied_beds.le(total_beds)
    ).all()
)

check(
    "Available beds are non-negative",
    available_beds.notna().all() and available_beds.ge(0).all()
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

weighted_denominator = float(total_beds[valid_bed_rows].sum())
weighted_occupancy = (
    float(occupied_beds[valid_bed_rows].sum()) / weighted_denominator * 100
    if weighted_denominator > 0
    else None
)
average_daily_rates = occupancy_rate_values.dropna()
average_daily_occupancy = (
    float(average_daily_rates.mean() * 100)
    if not average_daily_rates.empty
    else None
)

print("Valid bed rows in weighted occupancy denominator:",
      int(valid_bed_rows.sum()))
print("Weighted occupancy denominator (total beds):", weighted_denominator)
print(
    "Weighted occupancy numerator (occupied beds):",
    float(occupied_beds[valid_bed_rows].sum()),
)
print(
    "Weighted Bed Occupancy Rate (%):",
    round(weighted_occupancy, 2) if weighted_occupancy is not None else "N/A",
)
check(
    "Weighted Bed Occupancy Rate is approximately 69.87%",
    weighted_occupancy is not None and round(weighted_occupancy, 2) == 69.87,
)
print("Average daily occupancy denominator (valid rate rows):",
      len(average_daily_rates))
print(
    "Average Daily Occupancy Rate (%):",
    round(average_daily_occupancy, 2)
    if average_daily_occupancy is not None
    else "N/A",
)
check(
    "Average Daily Occupancy Rate is approximately 69.88%",
    average_daily_occupancy is not None
    and round(average_daily_occupancy, 2) == 69.88,
)

# ==========================================
# 2. READMISSION VALIDATION
# ==========================================

readmissions = pd.read_csv(
    DATA_DIR / "synthetic_patient_readmissions.csv"
)

print("\n2. READMISSION VALIDATION")

total_synthetic_admissions = len(readmissions)
print("Total records:", total_synthetic_admissions)

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
    "No missing readmission flags",
    readmissions["readmission_flag"].notna().all()
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

readmission_flags = pd.to_numeric(
    readmissions["readmission_flag"], errors="coerce"
)
valid_readmission_flags = (
    readmission_flags.notna() & readmission_flags.isin([0, 1])
)
readmission_flags_valid = bool(valid_readmission_flags.all())
readmission_count = (
    float(readmission_flags.sum()) if readmission_flags_valid else None
)
print(
    "Flagged readmissions:",
    int(readmission_count) if readmission_count is not None else "N/A",
)

overall_readmission_rate = (
    readmission_count / total_synthetic_admissions * 100
    if readmission_count is not None and total_synthetic_admissions > 0
    else None
)
print(
    "Overall Synthetic Readmission Rate denominator (all synthetic "
    "admission records):",
    total_synthetic_admissions,
)
print(
    "Overall Synthetic Readmission Rate (%):",
    round(overall_readmission_rate, 2)
    if overall_readmission_rate is not None
    else "N/A",
)
check(
    "Overall Synthetic Readmission Rate is approximately 12.12%",
    overall_readmission_rate is not None
    and round(overall_readmission_rate, 2) == 12.12,
)

previous_admission_mask = readmissions["previous_admission_date"].notna()
previous_admission_records = readmission_flags[previous_admission_mask]
previous_admission_flags_valid = (
    not previous_admission_records.empty
    and previous_admission_records.notna().all()
    and previous_admission_records.isin([0, 1]).all()
)
previous_admission_denominator = int(previous_admission_mask.sum())
previous_admission_flagged = (
    float(previous_admission_records.sum())
    if previous_admission_flags_valid
    else None
)
previous_admission_rate = (
    previous_admission_flagged / previous_admission_denominator * 100
    if previous_admission_flags_valid and previous_admission_denominator > 0
    else None
)
print(
    "Previous-admission subset flagged records:",
    int(previous_admission_flagged)
    if previous_admission_flagged is not None
    else "N/A",
)
print(
    "Readmission Percentage Among Records with Previous Admission "
    "denominator (non-null previous_admission_date):",
    previous_admission_denominator,
)
print(
    "Readmission Percentage Among Records with Previous Admission (%):",
    round(previous_admission_rate, 2)
    if previous_admission_rate is not None
    else "N/A",
)
check(
    "Previous-admission subset readmission percentage is approximately 36.01%",
    previous_admission_rate is not None
    and round(previous_admission_rate, 2) == 36.01,
)
print(
    "Note: The 12.12% overall rate and 36.01% previous-admission subset "
    "percentage use different denominators. Both are synthetic "
    "demonstrations, not clinically validated measures."
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
failed_checks = [name for name, passed in validation_results if not passed]
print(
    f"Validation summary: {len(validation_results) - len(failed_checks)} "
    f"passed, {len(failed_checks)} failed."
)
if failed_checks:
    print("Failed checks:", ", ".join(failed_checks))
sys.exit(1 if failed_checks else 0)
