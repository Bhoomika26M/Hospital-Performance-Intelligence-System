
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
file_path = ROOT / "data" / "hospital_dashboard_demo_data.csv"

df = pd.read_csv(file_path)

df["length_of_stay_days_for_kpi"] = pd.to_numeric(
    df["length_of_stay_days_for_kpi"], errors="coerce"
)

df["billing_amount"] = pd.to_numeric(
    df["billing_amount"], errors="coerce"
)

print("\n===== HOSPITAL KPI VERIFICATION =====")

print("Total Admissions:", len(df))

print(
    "Average Stay:",
    round(df["length_of_stay_days_for_kpi"].mean(), 2)
)

print(
    "Total Billing:",
    round(df["billing_amount"].sum(), 2)
)

print(
    "Average Billing:",
    round(df["billing_amount"].mean(), 2)
)

print("\n===== DATA CHECK =====")

print(
    "Missing Stay Values:",
    df["length_of_stay_days_for_kpi"].isna().sum()
)

print(
    "Missing Billing Values:",
    df["billing_amount"].isna().sum()
)

print(
    "Negative Billing Values:",
    (df["billing_amount"] < 0).sum()
)
