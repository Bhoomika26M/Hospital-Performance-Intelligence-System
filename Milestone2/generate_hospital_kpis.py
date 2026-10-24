import pandas as pd

df = pd.read_csv(
    r"C:\Users\HP\OneDrive\Desktop\Hospital_Analytics_project\Integrated dataset\hospital_cleaned.csv")

admissions = pd.read_csv(
    r"C:\Users\HP\OneDrive\Desktop\Hospital_Analytics_project\Hospital_admission dataset\hospital_admissions_cleaned.csv")

total_admissions = df["patients_admitted"].sum()

average_los = admissions["length_of_stay_days"].mean()

readmission_rate = (
    admissions["is_readmission_30d"].mean() * 100
)

df["admission_success"] = (
    df["patients_admitted"] / df["patients_request"]
).clip(0, 1) * 100

df["staff_coverage"] = (
    df["staff_present"] / df["staff_count"]
).clip(0, 1) * 100

df["satisfaction_score"] = (df["average_satisfaction"].clip(0, 100))

df["department_efficiency_score"] = (
    df["admission_success"] * 0.40
    + df["staff_coverage"] * 0.30
    + df["satisfaction_score"] * 0.30
)

df["estimated_bed_utilization"] = (
    df["patient_count"] * df["average_length_of_stay"]
    / (df["available_beds"] * 7)
) * 100

df["total_admissions"] = total_admissions
df["overall_average_los"] = average_los
df["readmission_rate"] = readmission_rate

df.to_excel("hospital_final_dataset.xlsx", index=False)

print("Total Admissions:", total_admissions)
print("Average Length of Stay:", round(average_los, 2))
print("Readmission Rate:", round(readmission_rate, 2), "%")
