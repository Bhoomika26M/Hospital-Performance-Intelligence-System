"""
MedTrack_DV - Hospital KPI Engineering
Run in Google Colab or locally after uploading hospital_cleaned.csv.

Output: hospital_final_dataset.xlsx
Install if needed: pip install pandas openpyxl
"""
import pandas as pd

INPUT_FILE = "hospital_cleaned.csv"
OUTPUT_FILE = "hospital_final_dataset.xlsx"

def main():
    df = pd.read_csv(INPUT_FILE)
    df["date_of_admission"] = pd.to_datetime(df["date_of_admission"], errors="coerce")
    df["discharge_date"] = pd.to_datetime(df["discharge_date"], errors="coerce")
    df["length_of_stay_days"] = pd.to_numeric(df["length_of_stay_days"], errors="coerce")

    total_admissions = len(df)
    average_los = df["length_of_stay_days"].mean()

    # Only calculate KPIs supported by the available fields.
    kpis = pd.DataFrame([
        ["Total Admissions", total_admissions, "COUNT of admission records", "Available"],
        ["Average Length of Stay (days)", round(average_los, 2),
         "AVERAGE(discharge_date - date_of_admission)", "Available"],
        ["Occupancy Rate", None, "(Occupied bed-days / Available bed-days) * 100",
         "Needs occupied bed-days and available bed-days"],
        ["Readmission Rate", None,
         "(Readmitted patients / discharged patients) * 100",
         "Needs unique patient ID and defined readmission window"],
        ["Bed Utilization Rate", None, "(Used bed-days / Available bed-days) * 100",
         "Needs bed inventory/capacity and occupied bed-days"],
        ["Department Efficiency Score", None, "Department-level agreed score",
         "Needs department, staffing, capacity and outcome data"],
    ], columns=["KPI", "Value", "Formula", "Status"])

    monthly_admissions = (
        df.dropna(subset=["date_of_admission"])
          .assign(month=lambda x: x["date_of_admission"].dt.to_period("M").astype(str))
          .groupby("month").size().rename("admissions")
    )
    monthly_discharges = (
        df.dropna(subset=["discharge_date"])
          .assign(month=lambda x: x["discharge_date"].dt.to_period("M").astype(str))
          .groupby("month").size().rename("discharges")
    )
    monthly = pd.concat([monthly_admissions, monthly_discharges], axis=1).fillna(0).astype(int).reset_index()

    hospital_summary = df.groupby("hospital").agg(
        admissions=("name", "size"),
        average_length_of_stay=("length_of_stay_days", "mean"),
        total_billing=("billing_amount", "sum")
    ).reset_index()

    condition_summary = df.groupby("medical_condition").agg(
        admissions=("name", "size"),
        average_length_of_stay=("length_of_stay_days", "mean"),
        average_billing=("billing_amount", "mean")
    ).reset_index()

    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Admissions_Data", index=False)
        kpis.to_excel(writer, sheet_name="KPI_Summary", index=False)
        monthly.to_excel(writer, sheet_name="Monthly_Trends", index=False)
        hospital_summary.to_excel(writer, sheet_name="Hospital_Summary", index=False)
        condition_summary.to_excel(writer, sheet_name="Condition_Summary", index=False)

    print("KPI workbook created:", OUTPUT_FILE)
    print("Total admissions:", total_admissions)
    print("Average length of stay:", round(average_los, 2), "days")
    print("Other KPIs are marked as requiring additional operational data.")

if __name__ == "__main__":
    main()
