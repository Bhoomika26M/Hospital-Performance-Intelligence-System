

import pandas as pd

# ==========================================
# MODULE 2: DATA CLEANING AND TRANSFORMATION
# ==========================================

# 1. Load the original dataset
df = pd.read_csv("healthcare_dataset.csv")

print("Original dataset shape:", df.shape)

# 2. Remove duplicate records
duplicates = df.duplicated().sum()
print("\nDuplicate records found:", duplicates)

df = df.drop_duplicates().copy()

print("Duplicates removed:", duplicates)
print("Shape after removing duplicates:", df.shape)

# 3. Standardize column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)

print("\nColumn names standardized.")

# Standardize patient names
if "name" in df.columns:
    df["name"] = df["name"].str.strip().str.title()

print("Patient names standardized.")
# 4. Check and handle missing values
print("\nMissing values before cleaning:")
print(df.isnull().sum())

# Fill missing numerical values with the median
numeric_cols = df.select_dtypes(include="number").columns

for col in numeric_cols:
    if df[col].isnull().any():
        median_value = df[col].median()

        if pd.notna(median_value):
            df[col] = df[col].fillna(median_value)

# Fill missing categorical values with the mode
categorical_cols = df.select_dtypes(
    include=["object", "string", "category"]
).columns

for col in categorical_cols:
    if df[col].isnull().any():
        mode_values = df[col].mode()

        if not mode_values.empty:
            df[col] = df[col].fillna(mode_values[0])

print("\nMissing values after handling:")
print(df.isnull().sum())

# 5. Standardize department names
department_mapping = {
    "Cancer": "Oncology",
    "Obesity": "General Medicine",
    "Diabetes": "Endocrinology",
    "Asthma": "Pulmonology",
    "Hypertension": "Cardiology",
    "Arthritis": "Rheumatology"
}

if "medical_condition" in df.columns:
    df["department"] = (
        df["medical_condition"].map(department_mapping)
    )
    df["department"] = df["department"].fillna("Other")

print("\nDepartment information added.")

# 6. Convert dates and calculate length of stay
date_columns = ["date_of_admission", "discharge_date"]

for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

if all(col in df.columns for col in date_columns):
    df["length_of_stay"] = (
        df["discharge_date"] - df["date_of_admission"]
    ).dt.days

    # Invalid negative stays are marked as missing
    df.loc[df["length_of_stay"] < 0, "length_of_stay"] = pd.NA

print("\nDate conversion and length-of-stay calculation completed.")

# 7. Normalize numerical indicators using Min-Max scaling
numeric_cols = df.select_dtypes(include="number").columns.tolist()

# Room numbers are identifiers, not measurable indicators
numeric_cols = [
    col for col in numeric_cols
    if col != "room_number"
]

for col in numeric_cols:
    minimum = df[col].min()
    maximum = df[col].max()

    if pd.notna(minimum) and pd.notna(maximum):
        normalized_col = col + "_normalized"

        if maximum != minimum:
            df[normalized_col] = (
                (df[col] - minimum) / (maximum - minimum)
            )
        else:
            df[normalized_col] = 0.0

print("\nNumerical indicators normalized using Min-Max scaling.")

# 8. Validate the cleaned dataset
print("\n========== DATA VALIDATION ==========")

missing_total = df.isnull().sum().sum()
duplicate_total = df.duplicated().sum()
completeness = 100 * df.notna().sum().sum() / df.size

print("Final missing values:", missing_total)
print("Duplicate rows remaining:", duplicate_total)
print(f"Data completeness: {completeness:.2f}%")

# 9. Save the cleaned dataset
output_file = "hospital_cleaned.csv"
df.to_csv(output_file, index=False)

print("\nCleaned dataset saved as:", output_file)
print("Final dataset shape:", df.shape)
print("\nModule 2 processing completed!")
# Verify the saved cleaned dataset
check_df = pd.read_csv("hospital_cleaned.csv")

print("\nNormalized columns:")
print([
    col for col in check_df.columns
    if col.endswith("_normalized")
])

print("\nSaved dataset shape:", check_df.shape)
print("\nFirst 5 rows:")
print(check_df.head())


# ==========================================
# 10. Prepare Tableau-ready dataset
# ==========================================

# Load the cleaned dataset
tableau_df = pd.read_csv("hospital_cleaned.csv")

# Create a separate dataset for visualization
tableau_df.to_csv("hospital_tableau_ready.csv", index=False)

print("\nTableau-ready dataset created: hospital_tableau_ready.csv")
print("Tableau dataset shape:", tableau_df.shape)
print("\nTableau dataset columns:")
print(tableau_df.columns.tolist())
