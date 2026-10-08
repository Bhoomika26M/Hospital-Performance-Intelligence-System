from pathlib import Path

import pandas as pd

# ==========================================
# 1. LOAD DATASET
# ==========================================

project_dir = Path(__file__).resolve().parent
input_file = project_dir / "healthcare_dataset.csv"
output_file = project_dir / "hospital_raw_data.csv"
cleaned_output_file = project_dir / "hospital_cleaned.csv"

df = pd.read_csv(input_file)

print("Original dataset shape:", df.shape)


# ==========================================
# 2. REMOVE DUPLICATES
# ==========================================

duplicates = df.duplicated().sum()
print("Duplicate records found:", duplicates)

df = df.drop_duplicates()

print("Shape after removing duplicates:", df.shape)


# ==========================================
# 3. STANDARDIZE COLUMN NAMES
# ==========================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", "_", regex=True)
)

for column in df.columns:
    if pd.api.types.is_string_dtype(df[column].dtype):
        df[column] = df[column].str.strip().replace("", pd.NA)

for column in ("age", "billing_amount", "room_number"):
    df[column] = pd.to_numeric(df[column], errors="coerce")

print("\nStandardized columns:")
print(df.columns.tolist())


# ==========================================
# 4. CONVERT DATE COLUMNS
# ==========================================

df["date_of_admission"] = pd.to_datetime(
    df["date_of_admission"],
    errors="coerce"
)

df["discharge_date"] = pd.to_datetime(
    df["discharge_date"],
    errors="coerce"
)


# ==========================================
# 5. CREATE LENGTH OF STAY
# ==========================================

df["length_of_stay"] = (
    df["discharge_date"] - df["date_of_admission"]
).dt.days

print("\nLength of stay calculated.")


# ==========================================
# 6. CREATE DEPARTMENT INFORMATION
# ==========================================

department_mapping = {
    "Cancer": "Oncology",
    "Obesity": "General Medicine",
    "Diabetes": "Endocrinology",
    "Asthma": "Pulmonology",
    "Hypertension": "Cardiology",
    "Arthritis": "Rheumatology"
}

df["department"] = df["medical_condition"].map(department_mapping)

print("\nDepartment information added.")


# ==========================================
# 7. CREATE HOSPITAL OPERATIONAL DATA
# ==========================================

hospital_operations = (
    df.groupby("hospital")
    .agg(
        total_patients=("name", "count"),
        total_doctors=("doctor", "nunique"),
        total_rooms_used=("room_number", "nunique"),
        average_billing=("billing_amount", "mean")
    )
    .reset_index()
)

print("\nHospital operational data created:")
print(hospital_operations.head())


# ==========================================
# 8. CREATE DEPARTMENT RESOURCE DATA
# ==========================================

department_resources = (
    df.groupby("department")
    .agg(
        patient_count=("name", "count"),
        doctors_available=("doctor", "nunique"),
        rooms_used=("room_number", "nunique"),
        average_billing=("billing_amount", "mean")
    )
    .reset_index()
)

print("\nDepartment resource data created:")
print(department_resources)


# ==========================================
# 9. INTEGRATE HOSPITAL OPERATIONAL DATA
# ==========================================

df = df.merge(
    hospital_operations,
    on="hospital",
    how="left"
)


# ==========================================
# 10. INTEGRATE DEPARTMENT RESOURCE DATA
# ==========================================

df = df.merge(
    department_resources,
    on="department",
    how="left",
    suffixes=("", "_department")
)


# ==========================================
# 11. CHECK MISSING VALUES
# ==========================================

missing_values = df.isnull().sum().sum()

print("\nTotal missing values:", missing_values)


# ==========================================
# 12. CHECK DUPLICATES
# ==========================================

print("Duplicate rows after integration:", df.duplicated().sum())


# ==========================================
# 13. CALCULATE DATA COMPLETENESS
# ==========================================

total_cells = df.shape[0] * df.shape[1]

completeness = (
    (total_cells - missing_values) / total_cells
) * 100

print(f"Data completeness: {completeness:.2f}%")

missing_percentage = (missing_values / total_cells) * 100
if completeness <= 95:
    raise ValueError(f"Dataset completeness is below the 95% target: {completeness:.2f}%")
if missing_percentage >= 2:
    raise ValueError(f"Missing values meet or exceed the 2% limit: {missing_percentage:.2f}%")
if df.duplicated().any():
    raise ValueError("Duplicate rows remain after integration")


# ==========================================
# 14. SAVE FINAL DATASET
# ==========================================

df.to_csv(output_file, index=False)
df.to_csv(cleaned_output_file, index=False)

print("\nFinal integrated dataset saved as:")
print(output_file)
print("Tableau-ready cleaned dataset saved as:")
print(cleaned_output_file)

print("Final dataset shape:", df.shape)