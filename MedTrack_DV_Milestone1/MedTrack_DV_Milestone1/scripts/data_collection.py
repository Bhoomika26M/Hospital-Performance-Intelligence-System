"""
MedTrack_DV - Milestone 1 data collection and cleaning
Run:
python scripts/data_collection.py --patient "data/raw/patient_admissions_raw.csv" --infrastructure "data/raw/pmc_infrastructure_raw.csv"
"""
from pathlib import Path
import argparse
import pandas as pd

def clean_patient(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("string").str.strip()
    df["Date of Admission"] = pd.to_datetime(df["Date of Admission"], errors="coerce")
    df["Discharge Date"] = pd.to_datetime(df["Discharge Date"], errors="coerce")
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Billing Amount"] = pd.to_numeric(df["Billing Amount"], errors="coerce")
    df["Length of Stay (Days)"] = (df["Discharge Date"] - df["Date of Admission"]).dt.days
    df = df.drop_duplicates().copy()
    df["Admission Month"] = df["Date of Admission"].dt.to_period("M").astype("string")
    df["Admission Year"] = df["Date of Admission"].dt.year.astype("Int64")
    return df

def clean_infrastructure(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("string").str.strip()
    for col in ["Class : (Public / Private)", "Pharmacy Available : Yes/No", "Ambulance Service Available"]:
        if col in df.columns:
            df[col] = df[col].str.title()
    for col in ["Pharmacy Available : Yes/No", "Ambulance Service Available"]:
        if col in df.columns:
            df[col] = df[col].replace({"N.A.": "Not Specified", "Na": "Not Specified"})
    if "Ward No." in df.columns and df["Ward No."].isna().all():
        df = df.drop(columns=["Ward No."])
    numeric_cols = [
        "Zone No.", "Number of Beds in Emergency Wards",
        "Number of Beds in facility type", "Number of Doctors / Physicians",
        "Number of Nurses", "Number of Midwives Professional",
        "Average Monthly Patient Footfall", "Count of Ambulance"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].replace({"N.A.": pd.NA, "NA": pd.NA, "": pd.NA}), errors="coerce")
    for col in ["Zone Name", "Ward Name"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--patient", required=True)
    parser.add_argument("--infrastructure", required=True)
    parser.add_argument("--output", default="data/processed")
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    clean_patient(args.patient).to_csv(out / "patient_admissions_cleaned.csv", index=False)
    clean_infrastructure(args.infrastructure).to_csv(out / "pmc_infrastructure_cleaned.csv", index=False)
    print("Cleaning complete. Two datasets were kept separate; no unsupported join was performed.")

if __name__ == "__main__":
    main()
