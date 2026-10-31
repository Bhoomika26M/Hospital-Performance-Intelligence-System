"""Milestone 2 / Module 3 - Hospital KPI engineering (single source of truth).

Uses the SAME functions as the dashboard (scripts/kpi_utils.py), so the numbers
here and on the dashboard cannot disagree.

Input : data/processed/hospital_final.csv
        data/raw/department_resources.csv
Output (data/processed/):
        kpi_overall.csv, kpi_monthly.csv, kpi_department.csv, kpi_region.csv
        hospital_final_dataset.xlsx  (KPI sheets + full records)

Run from the repo root:  python scripts/generate_hospital_kpis.py
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kpi_utils import (load_dataset, load_resources, daily_inhouse, window_kpis,
                       warmup_end, department_table, efficiency_score)

ROOT = Path(__file__).resolve().parents[1]
PROC_DIR = ROOT / "data" / "processed"
RAW_DIR = ROOT / "data" / "raw"

# ------------------------------------------------------------------ load
df = load_dataset(PROC_DIR / "hospital_final.csv")
res = load_resources(RAW_DIR / "department_resources.csv")

capacity = int(res["Beds Allocated"].sum())      # same default as the dashboard sidebar
ih = daily_inhouse(df)
warm = warmup_end(df)
first = df["admit"].min().normalize()
last = df["admit"].max().normalize()

# ------------------------------------------------------------------ overall KPIs
k = window_kpis(df, ih, first, last, capacity, warm)
overall = pd.DataFrame({
    "KPI": ["Total admissions", "Occupancy rate", "Avg length of stay",
            "Readmission rate", "Bed utilization (peak)", "Discharges"],
    "Value": [k["adm"], round(k["occ"], 2), round(k["los"], 2),
              round(k["readm"], 3), round(k["bed"], 2), k["disc"]],
    "Unit": ["count", "%", "days", "%", "%", "count"],
})

# ------------------------------------------------------------------ monthly KPIs (full months only)
rows = []
for m in pd.date_range(first.to_period("M").to_timestamp(), last, freq="MS"):
    m_end = m + pd.offsets.MonthEnd(0)
    if m < first or m_end > last:                # skip partial first / last month
        continue
    r = window_kpis(df, ih, m, m_end, capacity, warm)
    if r is None:
        continue
    rows.append({"month": m.date(), "admissions": r["adm"], "occupancy_pct": round(r["occ"], 2),
                 "avg_los_days": round(r["los"], 2), "readmission_pct": round(r["readm"], 3),
                 "bed_utilization_peak_pct": round(r["bed"], 2), "discharges": r["disc"]})
monthly = pd.DataFrame(rows)

# ------------------------------------------------------------------ department KPIs
dep = department_table(df)
dep["efficiency_score"] = efficiency_score(dep, dep)
dep = dep.merge(res[["Department", "Beds Allocated", "Doctors"]]
                .rename(columns={"Department": "department", "Beds Allocated": "beds"}),
                on="department", how="left")
dep["admissions_per_bed"] = dep["admissions"] / dep["beds"]
dep["admissions_per_doctor"] = dep["admissions"] / dep["Doctors"]
dep = dep.rename(columns={"Doctors": "doctors"}).round(2).sort_values("efficiency_score", ascending=False)

# ------------------------------------------------------------------ region KPIs
region = (df.groupby("region")
            .agg(admissions=("los", "size"), avg_los=("los", "mean"), readmit_rate=("readmit", "mean"))
            .reset_index())
region["readmit_rate"] *= 100
region = region.round(2).sort_values("admissions", ascending=False)

# ------------------------------------------------------------------ save
PROC_DIR.mkdir(parents=True, exist_ok=True)
overall.to_csv(PROC_DIR / "kpi_overall.csv", index=False)
monthly.to_csv(PROC_DIR / "kpi_monthly.csv", index=False)
dep.to_csv(PROC_DIR / "kpi_department.csv", index=False)
region.to_csv(PROC_DIR / "kpi_region.csv", index=False)
print("Saved kpi_overall.csv, kpi_monthly.csv, kpi_department.csv, kpi_region.csv")

xlsx_path = PROC_DIR / "hospital_final_dataset.xlsx"
try:
    try:
        import xlsxwriter  # noqa: F401  (faster for the big sheet)
        engine = "xlsxwriter"
    except ImportError:
        import openpyxl  # noqa: F401
        engine = "openpyxl"
    print(f"Writing Excel file with {engine}... this can take a few minutes, please wait.")
    records = df.copy()
    for col in records.select_dtypes("datetime").columns:
        records[col] = records[col].dt.date
    with pd.ExcelWriter(xlsx_path, engine=engine) as xl:
        overall.to_excel(xl, sheet_name="KPI Summary", index=False)
        monthly.to_excel(xl, sheet_name="Monthly KPIs", index=False)
        dep.to_excel(xl, sheet_name="Department KPIs", index=False)
        region.to_excel(xl, sheet_name="Region KPIs", index=False)
        records.to_excel(xl, sheet_name="Hospital Data", index=False)   # biggest sheet last
    print("Saved hospital_final_dataset.xlsx")
except ImportError:
    print("Skipped Excel file: run  pip install openpyxl  and run this script again.")

# ------------------------------------------------------------------ printout (compare with dashboard Page 1)
print(f"\nCapacity used: {capacity} beds | range: {first:%d %b %Y} to {last:%d %b %Y}")
print("\n=== OVERALL KPIs ===")
print(overall.to_string(index=False))
print(f"\nRows: {len(monthly)} monthly, {len(dep)} departments, {len(region)} regions")