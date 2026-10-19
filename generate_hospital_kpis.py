import pandas as pd
from pathlib import Path

# ==========================================
# 1. Load the cleaned hospital dataset
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "hospital_cleaned.csv"

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        "hospital_cleaned.csv was not found. "
        "Make sure it is in the same folder as this script."
    )

df = pd.read_csv(INPUT_FILE)

print("=" * 50)
print("HOSPITAL KPI ENGINEERING")
print("=" * 50)

print("\nDataset loaded successfully.")
print("Dataset shape:", df.shape)


# ==========================================
# 2. Prepare the data
# ==========================================

# Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Convert date columns
date_columns = ["date_of_admission", "discharge_date"]

for column in date_columns:
    if column in df.columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

# Calculate length of stay in days
if (
    "date_of_admission" in df.columns
    and "discharge_date" in df.columns
):
    df["length_of_stay"] = (
        df["discharge_date"] - df["date_of_admission"]
    ).dt.days

    # Negative stays are invalid
    df.loc[
        df["length_of_stay"] < 0,
        "length_of_stay"
    ] = pd.NA

elif "length_of_stay" not in df.columns:
    df["length_of_stay"] = pd.NA

# Convert relevant numeric columns
for column in ["age", "billing_amount", "length_of_stay"]:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ==========================================
# 3. Calculate hospital-level KPIs
# ==========================================

# Total admissions represented by the dataset.
# This is a count of records, not necessarily unique patients.
total_admissions = len(df)

# Average length of stay
average_length_of_stay = df["length_of_stay"].mean()

# Occupancy rate cannot be calculated without bed occupancy
# and available-bed information.
occupancy_rate = None

# Readmission rate cannot be calculated reliably without
# stable patient IDs and visit history.
readmission_rate = None

# Bed utilization rate requires bed capacity and occupancy data.
bed_utilization_rate = None

kpi_summary = pd.DataFrame([
    {
        "KPI": "Total Admissions",
        "Value": total_admissions,
        "Status": "Calculated from dataset records"
    },
    {
        "KPI": "Average Length of Stay (Days)",
        "Value": (
            round(average_length_of_stay, 2)
            if pd.notna(average_length_of_stay)
            else None
        ),
        "Status": "Calculated from admission and discharge dates"
    },
    {
        "KPI": "Occupancy Rate (%)",
        "Value": occupancy_rate,
        "Status": "Unavailable: bed occupancy data required"
    },
    {
        "KPI": "Readmission Rate (%)",
        "Value": readmission_rate,
        "Status": "Unavailable: patient IDs and visit history required"
    },
    {
        "KPI": "Bed Utilization Rate (%)",
        "Value": bed_utilization_rate,
        "Status": "Unavailable: bed capacity and occupancy data required"
    }
])


# ==========================================
# 4. Department analytics and efficiency score
# ==========================================

# Use department if it already exists; otherwise map
# medical conditions to broad departments.
if "department" not in df.columns:
    if "medical_condition" in df.columns:
        department_mapping = {
            "Cancer": "Oncology",
            "Obesity": "General Medicine",
            "Diabetes": "Endocrinology",
            "Asthma": "Pulmonology",
            "Hypertension": "Cardiology",
            "Arthritis": "Rheumatology"
        }

        df["department"] = (
            df["medical_condition"]
            .astype("string")
            .str.strip()
            .str.title()
            .map(department_mapping)
            .fillna("Other")
        )
    else:
        df["department"] = "Unknown"

# Build the department summary
department_summary = (
    df.groupby("department", dropna=False)
    .agg(
        total_admissions=("department", "size"),
        average_length_of_stay=("length_of_stay", "mean")
    )
    .reset_index()
)

# Add average billing when the column is available
if "billing_amount" in df.columns:
    billing_summary = (
        df.groupby("department", dropna=False)["billing_amount"]
        .mean()
        .reset_index(name="average_billing_amount")
    )

    department_summary = department_summary.merge(
        billing_summary,
        on="department",
        how="left"
    )

# Add unique doctor count when doctor data is available
if "doctor" in df.columns:
    doctor_summary = (
        df.groupby("department", dropna=False)["doctor"]
        .nunique()
        .reset_index(name="unique_doctors")
    )

    department_summary = department_summary.merge(
        doctor_summary,
        on="department",
        how="left"
    )
else:
    department_summary["unique_doctors"] = pd.NA

# Calculate admissions per doctor where possible
department_summary["admissions_per_doctor"] = (
    department_summary["total_admissions"]
    / department_summary["unique_doctors"].replace(0, pd.NA)
)

# Min-Max normalization helper
def min_max_score(series):
    values = pd.to_numeric(series, errors="coerce")
    minimum = values.min()
    maximum = values.max()

    if pd.isna(minimum) or pd.isna(maximum):
        return pd.Series(0.0, index=series.index)

    if maximum == minimum:
        return pd.Series(50.0, index=series.index)

    return ((values - minimum) / (maximum - minimum)) * 100


# This is a provisional, data-based score—not a validated
# clinical or operational efficiency measure.
department_summary["admissions_score"] = min_max_score(
    department_summary["admissions_per_doctor"]
)

# Shorter stays receive a higher score.
department_summary["stay_score"] = (
    100 - min_max_score(
        department_summary["average_length_of_stay"]
    )
)

department_summary["department_efficiency_score"] = (
    (
        department_summary["admissions_score"]
        + department_summary["stay_score"]
    ) / 2
).round(2)

department_summary["efficiency_score_note"] = (
    "Provisional score based on admissions per listed doctor "
    "and length of stay; not clinically validated"
)


# ==========================================
# 5. Save outputs as CSV files
# ==========================================

patient_output = BASE_DIR / "hospital_final_patient_data.csv"
kpi_output = BASE_DIR / "hospital_kpi_summary.csv"
department_output = BASE_DIR / "hospital_department_analytics.csv"

df.to_csv(patient_output, index=False)
kpi_summary.to_csv(kpi_output, index=False)
department_summary.to_csv(department_output, index=False)


# ==========================================
# 6. Display results
# ==========================================

print("\n" + "=" * 50)
print("HOSPITAL KPI SUMMARY")
print("=" * 50)

print(kpi_summary.to_string(index=False))

print("\n" + "=" * 50)
print("DEPARTMENT ANALYTICS")
print("=" * 50)

print(department_summary.to_string(index=False))

print("\n" + "=" * 50)
print("FILES CREATED SUCCESSFULLY")
print("=" * 50)

print("1. hospital_final_patient_data.csv")
print("2. hospital_kpi_summary.csv")
print("3. hospital_department_analytics.csv")

print("\nModule 3 processing completed.")
print("All files are saved in:", BASE_DIR)

