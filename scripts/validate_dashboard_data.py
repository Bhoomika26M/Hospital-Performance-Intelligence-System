
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

file_path = ROOT / "data" / "hospital_dashboard_demo_data.csv"

df = pd.read_csv(file_path)

print("\n===== DATA VALIDATION REPORT =====")

# 1. Dataset dimensions
print("\n1. Dataset Shape")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 2. Missing values
print("\n2. Missing Values")
print(df.isnull().sum()[df.isnull().sum() > 0])

# 3. Duplicate records
print("\n3. Duplicate Records")
print("Duplicates:", df.duplicated().sum())

# 4. Date validation
df["date_of_admission"] = pd.to_datetime(
    df["date_of_admission"], errors="coerce"
)

df["discharge_date"] = pd.to_datetime(
    df["discharge_date"], errors="coerce"
)

invalid_dates = (
    df["date_of_admission"].isna()
    | (df["discharge_date"].notna()
       & (df["discharge_date"] < df["date_of_admission"]))
)

print("\n4. Invalid Dates")
print("Invalid date records:", invalid_dates.sum())

# 5. Negative billing
billing = pd.to_numeric(df["billing_amount"], errors="coerce")

print("\n5. Billing Validation")
print("Negative billing records:", (billing < 0).sum())

# 6. Negative length of stay
stay = pd.to_numeric(
    df["length_of_stay_days_for_kpi"], errors="coerce"
)

print("\n6. Length of Stay Validation")
print("Negative stay records:", (stay < 0).sum())

print("\n===== VALIDATION COMPLETED =====")
