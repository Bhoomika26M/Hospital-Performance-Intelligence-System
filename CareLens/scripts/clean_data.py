"""Milestone 1 / Module 2 - cleaning.

Input : data/hospital_raw_data.csv + the resource and feedback files
Output: data/hospital_cleaned.csv, data/resource_cleaned.csv, data/feedback_cleaned.csv
The same steps, with explanations, are in notebooks/hospital_cleaning.ipynb.
"""
import numpy as np
import pandas as pd
from config import RAW, DATA

df = pd.read_csv(DATA / "hospital_raw_data.csv")
start_rows = len(df)

# 1. Text columns: names had random capital letters ("DaNnY sMitH")
for col in ["Name", "Doctor", "Hospital"]:
    df[col] = df[col].str.strip().str.title()

# 2. Remove duplicate rows (checked after fixing the capitals)
df = df.drop_duplicates().reset_index(drop=True)
dupes_removed = start_rows - len(df)

# 3. Dates and length of stay
df["Date of Admission"] = pd.to_datetime(df["Date of Admission"])
df["Discharge Date"] = pd.to_datetime(df["Discharge Date"])
df["los_days"] = (df["Discharge Date"] - df["Date of Admission"]).dt.days

# 4. Negative billing amounts are not possible -> treat as missing and fill with the
#    median of the same condition + admission type. Keep a flag so nothing is hidden.
bad = df["Billing Amount"] < 0
df["billing_fixed"] = bad
df.loc[bad, "Billing Amount"] = np.nan
df["Billing Amount"] = df["Billing Amount"].fillna(
    df.groupby(["Medical Condition", "Admission Type"])["Billing Amount"].transform("median"))
df["Billing Amount"] = df["Billing Amount"].round(2)

# 5. Extra columns the dashboard needs
df["age_group"] = pd.cut(df["Age"], [0, 17, 34, 49, 64, 120],
                         labels=["0-17", "18-34", "35-49", "50-64", "65+"]).astype(str)
df["admit_year"] = df["Date of Admission"].dt.year
df["admit_month"] = df["Date of Admission"].dt.to_period("M").astype(str)
df["admit_weekday"] = df["Date of Admission"].dt.day_name()

# 6. 30-day readmission. There is no patient ID in this dataset, so I treat
#    same name + gender + blood type as the same patient (limitation - see Methodology.md).
key = ["Name", "Gender", "Blood Type"]
df = df.sort_values(key + ["Date of Admission"])
prev_discharge = df.groupby(key)["Discharge Date"].shift()
gap = (df["Date of Admission"] - prev_discharge).dt.days
df["readmit_30d"] = gap.between(0, 30)
df = df.sort_index()

# 7. Tidy column names (lower_case with underscores - easier in Tableau and pandas)
df.columns = [c.lower().replace(" ", "_") for c in df.columns]
df = df.rename(columns={"date_of_admission": "admission_date", "name": "patient_name",
                        "medical_condition": "condition"})
df.to_csv(DATA / "hospital_cleaned.csv", index=False)

# 8. Resource + feedback files: standardise department names, fill small gaps
res = pd.read_csv(RAW / "hospital_resource_raw.csv")
res = res.sort_values(["department", "month"])
res["nurses_on_duty"] = res.groupby("department")["nurses_on_duty"].transform(
    lambda s: s.interpolate().bfill().ffill()).round()
res.to_csv(DATA / "resource_cleaned.csv", index=False)

fb = pd.read_csv(RAW / "patient_feedback_raw.csv")
fb["department"] = fb["department"].str.strip().str.title()
fb.to_csv(DATA / "feedback_cleaned.csv", index=False)

print(f"rows in: {start_rows:,}   duplicates removed: {dupes_removed}   rows out: {len(df):,}")
print(f"negative billing amounts fixed: {int(bad.sum())}")
print(f"30-day readmissions found: {int(df['readmit_30d'].sum())}")
print(f"missing values left in cleaned admissions: {100*df.isna().sum().sum()/df.size:.3f}%")
