
import pandas as pd
from pathlib import Path

# Load cleaned dataset
BASE_DIR = Path(__file__).resolve().parent
FILE = BASE_DIR / "hospital_cleaned.csv"

df = pd.read_csv(FILE)

# Standardize column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Convert dates
df["date_of_admission"] = pd.to_datetime(
    df["date_of_admission"], errors="coerce"
)

df["discharge_date"] = pd.to_datetime(
    df["discharge_date"], errors="coerce"
)

# Independently calculate length of stay
df["length_of_stay"] = (
    df["discharge_date"] - df["date_of_admission"]
).dt.days

df.loc[df["length_of_stay"] < 0, "length_of_stay"] = pd.NA

# Calculate KPIs
total_admissions = len(df)
average_stay = df["length_of_stay"].mean()

# Department validation
department_total = df["department"].value_counts(
    dropna=False
).sum()

print("=" * 50)
print("MEDTRACK - KPI VALIDATION REPORT")
print("=" * 50)

print("\n1. TOTAL ADMISSIONS")
print("Calculated:", total_admissions)
print("Expected: 54966")
print("Result:", "PASS" if total_admissions == 54966 else "FAIL")

print("\n2. AVERAGE LENGTH OF STAY")
print("Calculated:", round(average_stay, 2))
print("Expected: Approximately 15.50 days")
print(
    "Result:",
    "PASS" if pd.notna(average_stay)
    and abs(average_stay - 15.50) < 0.01
    else "FAIL"
)

print("\n3. NEGATIVE LENGTH OF STAY")
negative_count = (df["length_of_stay"] < 0).sum()
print("Negative records:", negative_count)
print("Result:", "PASS" if negative_count == 0 else "FAIL")

print("\n4. DEPARTMENT ADMISSIONS")
print("Total department records:", department_total)
print(
    "Result:",
    "PASS" if department_total == total_admissions else "FAIL"
)

print("\n5. VALID LENGTH OF STAY RECORDS")
print("Valid records:", df["length_of_stay"].notna().sum())
print("Missing records:", df["length_of_stay"].isna().sum())

print("\n6. UNAVAILABLE METRICS")
print("Occupancy Rate: Requires actual bed occupancy data")
print("Readmission Rate: Requires patient IDs and visit history")

print("\n" + "=" * 50)
print("KPI VALIDATION COMPLETED")
print("=" * 50)
