import pandas as pd
import os

# ============================================================
# MedTrack DV
# Hospital Operations & Patient Analytics Dashboard
# Milestone 1 - Data Collection
# ============================================================


# ------------------------------------------------------------
# 1. Project directories
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


print("MedTrack DV - Data Collection")
print("=" * 60)


# ------------------------------------------------------------
# 2. Input file paths
# ------------------------------------------------------------

healthcare_file = os.path.join(
    DATA_DIR,
    "healthcare_data.csv"
)

patient_analysis_file = os.path.join(
    DATA_DIR,
    "hospital data analysis.csv"
)

resource_file = os.path.join(
    DATA_DIR,
    "hospital-resource-allocation-records.csv"
)


# ------------------------------------------------------------
# 3. Check that files exist
# ------------------------------------------------------------

print("\nChecking input files...")

if not os.path.exists(healthcare_file):
    print("ERROR: healthcare_data.csv not found!")
    exit()

if not os.path.exists(patient_analysis_file):
    print("ERROR: hospital data analysis.csv not found!")
    exit()

if not os.path.exists(resource_file):
    print("ERROR: hospital-resource-allocation-records.csv not found!")
    exit()

print("All input files found successfully!")


# ------------------------------------------------------------
# 4. Load datasets
# ------------------------------------------------------------

print("\nLoading datasets...")

healthcare_df = pd.read_csv(healthcare_file)

patient_analysis_df = pd.read_csv(patient_analysis_file)

resource_df = pd.read_csv(resource_file)

print("Datasets loaded successfully!")


# ------------------------------------------------------------
# 5. Standardize column names
# ------------------------------------------------------------

healthcare_df.columns = (
    healthcare_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

patient_analysis_df.columns = (
    patient_analysis_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

resource_df.columns = (
    resource_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# ------------------------------------------------------------
# 6. Display dataset information
# ------------------------------------------------------------

print("\n")
print("=" * 60)
print("DATASET INFORMATION")
print("=" * 60)


# Healthcare dataset
print("\n1. Healthcare Dataset")
print("-" * 40)

print("Rows:", healthcare_df.shape[0])
print("Columns:", healthcare_df.shape[1])

print(
    "Missing values:",
    healthcare_df.isnull().sum().sum()
)

print(
    "Duplicate rows:",
    healthcare_df.duplicated().sum()
)


# Patient analysis dataset
print("\n2. Hospital Patient Analysis Dataset")
print("-" * 40)

print("Rows:", patient_analysis_df.shape[0])
print("Columns:", patient_analysis_df.shape[1])

print(
    "Missing values:",
    patient_analysis_df.isnull().sum().sum()
)

print(
    "Duplicate rows:",
    patient_analysis_df.duplicated().sum()
)


# Resource dataset
print("\n3. Hospital Resource Allocation Dataset")
print("-" * 40)

print("Rows:", resource_df.shape[0])
print("Columns:", resource_df.shape[1])

print(
    "Missing values:",
    resource_df.isnull().sum().sum()
)

print(
    "Duplicate rows:",
    resource_df.duplicated().sum()
)


# ------------------------------------------------------------
# 7. Display column names
# ------------------------------------------------------------

print("\n")
print("=" * 60)
print("COLUMN NAMES")
print("=" * 60)

print("\nHealthcare Dataset:")
print(healthcare_df.columns.tolist())

print("\nHospital Patient Analysis Dataset:")
print(patient_analysis_df.columns.tolist())

print("\nHospital Resource Allocation Dataset:")
print(resource_df.columns.tolist())


# ------------------------------------------------------------
# 8. Convert date columns
# ------------------------------------------------------------

print("\n")
print("=" * 60)
print("DATE CONVERSION")
print("=" * 60)


# Healthcare dates
if "admission_date" in healthcare_df.columns:

    healthcare_df["admission_date"] = pd.to_datetime(
        healthcare_df["admission_date"],
        errors="coerce"
    )

if "discharge_date" in healthcare_df.columns:

    healthcare_df["discharge_date"] = pd.to_datetime(
        healthcare_df["discharge_date"],
        errors="coerce"
    )


# Resource allocation date
if "allocation_date" in resource_df.columns:

    resource_df["allocation_date"] = pd.to_datetime(
        resource_df["allocation_date"],
        errors="coerce"
    )


print("Date conversion completed.")


# ------------------------------------------------------------
# 9. Remove exact duplicate records
# ------------------------------------------------------------

print("\n")
print("=" * 60)
print("DUPLICATE RECORD REMOVAL")
print("=" * 60)


# Store original row counts
healthcare_before = len(healthcare_df)
patient_before = len(patient_analysis_df)
resource_before = len(resource_df)


# Remove duplicates
healthcare_df = healthcare_df.drop_duplicates()

patient_analysis_df = patient_analysis_df.drop_duplicates()

resource_df = resource_df.drop_duplicates()


# Calculate removed rows
healthcare_removed = (
    healthcare_before - len(healthcare_df)
)

patient_removed = (
    patient_before - len(patient_analysis_df)
)

resource_removed = (
    resource_before - len(resource_df)
)


print(
    "Healthcare duplicates removed:",
    healthcare_removed
)

print(
    "Patient analysis duplicates removed:",
    patient_removed
)

print(
    "Resource duplicates removed:",
    resource_removed
)


# ------------------------------------------------------------
# 10. Create output file paths
# ------------------------------------------------------------

hospital_raw_output = os.path.join(
    DATA_DIR,
    "hospital_raw_data.csv"
)

patient_analysis_output = os.path.join(
    DATA_DIR,
    "patient_analysis_raw.csv"
)

resource_raw_output = os.path.join(
    DATA_DIR,
    "hospital_resource_raw.csv"
)


# ------------------------------------------------------------
# 11. Save prepared datasets
# ------------------------------------------------------------

print("\n")
print("=" * 60)
print("SAVING PREPARED DATASETS")
print("=" * 60)


healthcare_df.to_csv(
    hospital_raw_output,
    index=False
)

patient_analysis_df.to_csv(
    patient_analysis_output,
    index=False
)

resource_df.to_csv(
    resource_raw_output,
    index=False
)


print(
    "Created:",
    "hospital_raw_data.csv"
)

print(
    "Created:",
    "patient_analysis_raw.csv"
)

print(
    "Created:",
    "hospital_resource_raw.csv"
)


# ------------------------------------------------------------
# 12. Final dataset summary
# ------------------------------------------------------------

print("\n")
print("=" * 60)
print("FINAL DATASET SUMMARY")
print("=" * 60)


print(
    "\nHospital Raw Data:",
    healthcare_df.shape[0],
    "rows x",
    healthcare_df.shape[1],
    "columns"
)

print(
    "Patient Analysis Data:",
    patient_analysis_df.shape[0],
    "rows x",
    patient_analysis_df.shape[1],
    "columns"
)

print(
    "Hospital Resource Data:",
    resource_df.shape[0],
    "rows x",
    resource_df.shape[1],
    "columns"
)


# ------------------------------------------------------------
# 13. Final status
# ------------------------------------------------------------

print("\n")
print("=" * 60)
print("DATA COLLECTION COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nMilestone 1 - Data Collection stage completed.")

print("\nPrepared files:")
print("1. hospital_raw_data.csv")
print("2. patient_analysis_raw.csv")
print("3. hospital_resource_raw.csv")

print("\nNext stage:")
print("Data Cleaning & Transformation")