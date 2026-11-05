
import pandas as pd
import os

os.makedirs("cleaned_data", exist_ok=True)

# Load cleaned datasets
healthcare = pd.read_csv("cleaned_data/healthcare_cleaned.csv")
hdhi = pd.read_csv("cleaned_data/hdhi_cleaned.csv")

# -----------------------------
# 1. HEALTHCARE KPIs
# -----------------------------

healthcare_kpis = {
    "Total Admissions": len(healthcare),
    "Average Length of Stay": round(
        healthcare["Length of Stay"].mean(), 2
    ),
    "Median Length of Stay": round(
        healthcare["Length of Stay"].median(), 2
    ),
    "Total Medical Conditions": healthcare[
        "Medical Condition"
    ].nunique()
}

print("\n===== HEALTHCARE KPIs =====")

for name, value in healthcare_kpis.items():
    print(name, ":", value)

pd.DataFrame(
    list(healthcare_kpis.items()),
    columns=["KPI", "Value"]
).to_csv("cleaned_data/healthcare_kpis.csv", index=False)

# Monthly admission trends
healthcare["Date of Admission"] = pd.to_datetime(
    healthcare["Date of Admission"]
)

monthly = (
    healthcare.groupby(
        healthcare["Date of Admission"].dt.to_period("M")
    ).size().reset_index(name="Admissions")
)

monthly["Month"] = monthly["Date of Admission"].astype(str)
monthly.drop(columns=["Date of Admission"]).to_csv(
    "cleaned_data/monthly_admissions.csv", index=False
)

# Admissions by type
healthcare.groupby("Admission Type").size().reset_index(
    name="Admissions"
).to_csv("cleaned_data/admissions_by_type.csv", index=False)


# -----------------------------
# 2. HDHI ADMISSION KPIs
# -----------------------------

hdhi["DURATION OF STAY"] = pd.to_numeric(
    hdhi["DURATION OF STAY"], errors="coerce"
)

hdhi["duration of intensive unit stay"] = pd.to_numeric(
    hdhi["duration of intensive unit stay"],
    errors="coerce"
)

hdhi_kpis = {
    "Total Admissions": len(hdhi),
    "Average Duration of Stay": round(
        hdhi["DURATION OF STAY"].mean(), 2
    ),
    "Average ICU Stay": round(
        hdhi["duration of intensive unit stay"].mean(), 2
    ),
    "Unique Patients": hdhi["MRD No."].nunique()
}

# Repeat-admission patients
patient_counts = hdhi.groupby("MRD No.").size()

repeat_patients = (patient_counts > 1).sum()

hdhi_kpis["Patients With Multiple Records"] = int(repeat_patients)

hdhi_kpis["Repeat-Record Patient Percentage"] = round(
    repeat_patients / len(patient_counts) * 100, 2
)

print("\n===== HDHI KPIs =====")

for name, value in hdhi_kpis.items():
    print(name, ":", value)

pd.DataFrame(
    list(hdhi_kpis.items()),
    columns=["KPI", "Value"]
).to_csv("cleaned_data/hdhi_kpis.csv", index=False)

# Outcome analysis
hdhi.groupby("OUTCOME").size().reset_index(
    name="Admissions"
).to_csv("cleaned_data/outcome_analysis.csv", index=False)

# Admission type analysis
hdhi.groupby("TYPE OF ADMISSION-EMERGENCY/OPD").size().reset_index(
    name="Admissions"
).to_csv("cleaned_data/hdhi_admission_types.csv", index=False)

print("\nKPI GENERATION COMPLETED SUCCESSFULLY!")
