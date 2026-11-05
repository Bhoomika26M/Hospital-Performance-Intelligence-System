import pandas as pd
import os

# Create output folder
os.makedirs("cleaned_data", exist_ok=True)

# -----------------------------
# DATASET 1: HEALTHCARE
# -----------------------------

healthcare = pd.read_csv("data/healthcare_dataset.csv")

print("Healthcare before cleaning:", healthcare.shape)

# Remove duplicate rows
healthcare = healthcare.drop_duplicates()

# Convert admission and discharge dates
healthcare["Date of Admission"] = pd.to_datetime(
    healthcare["Date of Admission"], errors="coerce"
)

healthcare["Discharge Date"] = pd.to_datetime(
    healthcare["Discharge Date"], errors="coerce"
)

# Calculate length of stay
healthcare["Length of Stay"] = (
    healthcare["Discharge Date"] -
    healthcare["Date of Admission"]
).dt.days

# Save cleaned dataset
healthcare.to_csv(
    "cleaned_data/healthcare_cleaned.csv",
    index=False
)

print("Healthcare after cleaning:", healthcare.shape)
print("Healthcare duplicates:", healthcare.duplicated().sum())


# -----------------------------
# DATASET 2: HDHI ADMISSION
# -----------------------------

hdhi = pd.read_csv("data/HDHI Admission data.csv")

print("\nHDHI before cleaning:", hdhi.shape)

# Convert empty text values into missing values
hdhi = hdhi.replace(r"^\s*EMPTY\s*$", pd.NA, regex=True)
hdhi = hdhi.replace(r"^\s*$", pd.NA, regex=True)

# Medical test columns
medical_columns = [
    "HB", "TLC", "PLATELETS", "GLUCOSE",
    "UREA", "CREATININE", "BNP", "EF"
]

# Convert medical test columns into numeric format
for col in medical_columns:
    hdhi[col] = pd.to_numeric(hdhi[col], errors="coerce")

# Save cleaned dataset
hdhi.to_csv(
    "cleaned_data/hdhi_cleaned.csv",
    index=False
)

print("HDHI after cleaning:", hdhi.shape)
print("HDHI missing values:", hdhi.isnull().sum().sum())
print("HDHI duplicates:", hdhi.duplicated().sum())

print("\nCLEANING COMPLETED SUCCESSFULLY!")
