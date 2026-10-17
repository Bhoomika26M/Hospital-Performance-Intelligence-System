
import pandas as pd

patient_path = "data/hospital data analysis.csv"
resource_path = "data/hospital-resource-allocation-records.csv"

# Patient analysis
patient_df = pd.read_csv(patient_path)

print("\n--- PATIENT ANALYSIS ---")

for col in ["Readmission", "Length_of_Stay", "Cost", "Outcome"]:
    print(f"\n{col}:")

    if col in patient_df.columns:
        print(patient_df[col].value_counts(dropna=False).head(15))
        if pd.api.types.is_numeric_dtype(patient_df[col]):
            print("\nStatistics:")
            print(patient_df[col].describe())
    else:
        print("Column not found")

# Resource allocation
resource_df = pd.read_csv(resource_path)

print("\n--- RESOURCE ALLOCATION ---")

for col in [
    "beds_allocated",
    "beds_occupied",
    "staff_allocated",
    "staff_on_duty",
]:
    print(f"\n{col}:")
    print(resource_df[col].describe())
    print("Missing values:", resource_df[col].isna().sum())

print("\nInspection completed.")
