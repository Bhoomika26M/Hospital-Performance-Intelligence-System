
import pandas as pd

patients = pd.read_csv("patients.csv")
services = pd.read_csv("services_weekly.csv")
staff = pd.read_csv("staff.csv")
schedule = pd.read_csv("staff_schedule.csv")


patients["arrival_date"] = pd.to_datetime(patients["arrival_date"])
patients["departure_date"] = pd.to_datetime(patients["departure_date"])


patients["length_of_stay"] = (
    patients["departure_date"] - patients["arrival_date"]
).dt.days


patients["week"] = (
    patients["arrival_date"].dt.isocalendar().week.astype(int)
)


patient_summary = patients.groupby(
    ["week", "service"]
).agg(
    patient_count=("patient_id", "count"),
    average_age=("age", "mean"),
    average_length_of_stay=("length_of_stay", "mean"),
    average_satisfaction=("satisfaction", "mean")
).reset_index()


staff_summary = staff.groupby("service").agg(
    staff_count=("staff_id", "nunique")
).reset_index()


staff_weekly = schedule.groupby(
    ["week", "service"]
).agg(
    staff_present=("present", "sum")
).reset_index()


hospital_raw = services.merge(
    patient_summary,
    on=["week", "service"],
    how="left"
)

hospital_raw = hospital_raw.merge(
    staff_weekly,
    on=["week", "service"],
    how="left"
)

hospital_raw = hospital_raw.merge(
    staff_summary,
    on="service",
    how="left"
)


hospital_raw.to_csv("hospital_raw_data.csv", index=False)
print("Integrated dataset shape:", hospital_raw.shape)
