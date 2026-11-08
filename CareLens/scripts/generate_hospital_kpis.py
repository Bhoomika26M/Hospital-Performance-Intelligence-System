"""Milestone 2 / Module 3 - KPI engineering.

Output: data/hospital_final_dataset.xlsx  (also data/monthly_kpis.csv for Tableau)
KPI formulas are explained in docs/KPI_Documentation.md.
"""
import numpy as np
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from config import DATA, WINDOW_START, WINDOW_END, OCCUPANCY_TARGET
from utils import daily_census, MONTH_OF_DAY

adm = pd.read_csv(DATA / "hospital_cleaned.csv", parse_dates=["admission_date", "discharge_date"])
res = pd.read_csv(DATA / "resource_cleaned.csv", parse_dates=["month"])
fb = pd.read_csv(DATA / "feedback_cleaned.csv", parse_dates=["month"])
master = pd.read_csv(DATA.parent / "data" / "raw" / "department_master.csv")

months = pd.period_range(WINDOW_START, WINDOW_END, freq="M")
adm["m_in"] = adm["admission_date"].dt.to_period("M")
adm["m_out"] = adm["discharge_date"].dt.to_period("M")

rows = []
for _, d in master.iterrows():
    sub = adm[adm["department"] == d["department"]]
    census = daily_census(sub["admission_date"], sub["discharge_date"])
    for m in months:
        day_mask = (MONTH_OF_DAY == m)
        days = int(day_mask.sum())
        admitted = sub[sub["m_in"] == m]
        rows.append({
            "month": m.to_timestamp(), "department": d["department"],
            "admissions": len(admitted),
            "discharges": int((sub["m_out"] == m).sum()),
            "patient_days": int(census[day_mask].sum()),
            "peak_census": int(census[day_mask].max()),
            "days_in_month": days,
            "licensed_beds": d["licensed_beds"],
            "avg_los_days": round(admitted["los_days"].mean(), 2),
            "readmissions_30d": int(admitted["readmit_30d"].sum()),
            "billing_total": round(admitted["billing_amount"].sum(), 2),
            "target_los_days": d["target_los_days"],
        })
k = pd.DataFrame(rows)
k = k.merge(res, on=["month", "department"], how="left").merge(
    fb.drop(columns=[]), on=["month", "department"], how="left")

# ---- the six project KPIs ----------------------------------------------------
k["avg_daily_census"] = (k["patient_days"] / k["days_in_month"]).round(1)
k["occupancy_rate"] = (k["patient_days"] / (k["licensed_beds"] * k["days_in_month"])).round(4)
k["bed_utilization_rate"] = (k["patient_days"] / (k["staffed_beds"] * k["days_in_month"])).round(4)
k["readmission_rate"] = (k["readmissions_30d"] / k["admissions"]).round(4)
k["equipment_utilization"] = (k["equipment_hours_used"] / k["equipment_hours_available"]).round(4)

# Department Efficiency Score (0-100): 40% length of stay vs target,
# 30% how close bed utilization is to the 85% target, 30% patient satisfaction.
los_score = np.minimum(100, k["target_los_days"] / k["avg_los_days"] * 100)
util_score = np.maximum(0, 100 - abs(k["bed_utilization_rate"] - OCCUPANCY_TARGET) * 400)
sat_score = k["avg_satisfaction"] / 5 * 100
k["efficiency_score"] = (0.4 * los_score + 0.3 * util_score + 0.3 * sat_score).round(1)
k["month"] = k["month"].dt.strftime("%Y-%m-%d")
k.to_csv(DATA / "monthly_kpis.csv", index=False)

# ---- department summary over the whole window --------------------------------
g = k.groupby("department")
summary = pd.DataFrame({
    "admissions": g["admissions"].sum(),
    "avg_los_days": (g.apply(lambda x: (x["avg_los_days"] * x["admissions"]).sum() / x["admissions"].sum())).round(2),
    "readmission_rate": (g["readmissions_30d"].sum() / g["admissions"].sum()).round(4),
    "occupancy_rate": (g["patient_days"].sum() / g.apply(lambda x: (x["licensed_beds"] * x["days_in_month"]).sum())).round(4),
    "bed_utilization_rate": (g["patient_days"].sum() / g.apply(lambda x: (x["staffed_beds"] * x["days_in_month"]).sum())).round(4),
    "equipment_utilization": (g["equipment_hours_used"].sum() / g["equipment_hours_available"].sum()).round(4),
    "avg_satisfaction": g.apply(lambda x: (x["avg_satisfaction"] * x["responses"]).sum() / x["responses"].sum()).round(2),
    "avg_efficiency_score": g["efficiency_score"].mean().round(1),
}).reset_index()

definitions = pd.DataFrame([
    ["Total Admissions", "Count of admissions in the period"],
    ["Occupancy Rate", "Patient-days / (licensed beds x days in period)"],
    ["Average Length of Stay", "Mean of (discharge date - admission date) for patients admitted in the period"],
    ["Readmission Rate", "Admissions that came within 30 days of the same patient's last discharge / all admissions"],
    ["Bed Utilization Rate", "Patient-days / (staffed beds x days in period)"],
    ["Department Efficiency Score", "40% LOS vs target + 30% closeness of bed utilization to 85% + 30% satisfaction (0-100)"],
], columns=["KPI", "Formula"])

# ---- write the workbook -------------------------------------------------------
cols = ["patient_name", "age", "age_group", "gender", "condition", "department", "admission_type",
        "admission_date", "discharge_date", "los_days", "admit_month", "admit_weekday", "doctor",
        "insurance_provider", "billing_amount", "room_number", "floor", "test_results", "readmit_30d"]
out = DATA / "hospital_final_dataset.xlsx"
with pd.ExcelWriter(out, engine="openpyxl", datetime_format="yyyy-mm-dd") as xw:
    adm[cols].to_excel(xw, sheet_name="Admissions", index=False)
    k.to_excel(xw, sheet_name="Monthly_KPIs", index=False)
    summary.to_excel(xw, sheet_name="Department_Summary", index=False)
    definitions.to_excel(xw, sheet_name="KPI_Definitions", index=False)
    for ws in xw.book.worksheets:
        ws.freeze_panes = "A2"
        for c in ws[1]:
            c.font = Font(name="Arial", bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="2A6F5B")
            c.alignment = Alignment(horizontal="left")
        for col in ws.columns:
            width = min(36, max(len(str(col[0].value)), 12) + 2)
            ws.column_dimensions[col[0].column_letter].width = width

print(summary.to_string(index=False))
print("\nWorkbook saved:", out.name, "| monthly rows:", len(k))
