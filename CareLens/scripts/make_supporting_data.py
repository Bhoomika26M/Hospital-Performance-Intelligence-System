"""Step 0 - build the supporting datasets.

The Kaggle admissions file has no beds, staff, equipment or feedback data, but the
project needs them (Resource Utilization dashboard). I could not find one public file
with all of that, so these three files are SIMULATED. They are tied to the real
admissions (e.g. equipment use goes up when the ward is busier) and use a fixed
random seed so the results are the same every run.

If you download real files (see docs/Dataset_Sources.md), put them in data/raw/ with
the same column names and skip this script.
"""
import numpy as np
import pandas as pd
from config import RAW, CONDITION_TO_DEPT
from utils import daily_census, MONTH_OF_DAY

rng = np.random.default_rng(42)

adm = pd.read_csv(RAW / "healthcare_dataset.csv").drop_duplicates()
adm["dept"] = adm["Medical Condition"].map(CONDITION_TO_DEPT)

# ---- 1. department master ---------------------------------------------------
master = pd.DataFrame({
    "department":      ["Cardiology", "Endocrinology", "Oncology", "Pulmonology", "Rheumatology"],
    "licensed_beds":   [90, 180, 90, 90, 90],
    "doctors":         [14, 24, 16, 12, 10],
    "target_los_days": [14, 15, 16, 14, 14],
    "equipment_name":  ["ECG / Echo units", "Lab analyzers", "Infusion pumps", "Ventilators", "Imaging units"],
    "equipment_units": [12, 10, 20, 15, 8],
})
master.to_csv(RAW / "department_master.csv", index=False)

# ---- 2 + 3. monthly resources and feedback ----------------------------------
months = pd.period_range("2019-07", "2024-04", freq="M")
res_rows, fb_rows = [], []
for _, d in master.iterrows():
    sub = adm[adm["dept"] == d["department"]]
    census = daily_census(sub["Date of Admission"], sub["Discharge Date"])
    discharged = pd.to_datetime(sub["Discharge Date"]).dt.to_period("M").value_counts()
    for m in months:
        in_month = (MONTH_OF_DAY == m)
        days = int(in_month.sum())
        occ = census[in_month].sum() / (d["licensed_beds"] * days)

        staffed = round(d["licensed_beds"] * rng.uniform(0.90, 0.98))
        units_ok = d["equipment_units"] - int(rng.integers(0, 3))
        hrs_avail = units_ok * days * 12                      # 12 usable hours a day
        hrs_used = round(hrs_avail * float(np.clip(occ * 0.85 + rng.normal(0, 0.04), 0.4, 0.98)))
        res_rows.append({
            "month": m.strftime("%Y-%m-01"), "department": d["department"],
            "staffed_beds": staffed,
            "nurses_on_duty": round(staffed * rng.uniform(0.42, 0.55)),
            "doctors_on_roster": int(d["doctors"] + rng.integers(-1, 2)),
            "equipment_units_available": units_ok,
            "equipment_hours_available": hrs_avail,
            "equipment_hours_used": hrs_used,
        })

        n_dis = int(discharged.get(m, 0))
        name = d["department"]
        r = rng.random()           # make the names messy on purpose (cleaned later)
        if r < 0.05: name = name.upper()
        elif r < 0.10: name = name.lower() + " "
        fb_rows.append({
            "month": m.strftime("%Y-%m-01"), "department": name,
            "responses": round(n_dis * rng.uniform(0.15, 0.25)),
            "avg_satisfaction": round(float(np.clip(4.3 - 1.2 * max(0, occ - 0.8) + rng.normal(0, 0.12), 3, 4.9)), 2),
            "avg_wait_minutes": round(30 + 80 * max(0, occ - 0.7) + rng.normal(0, 5)),
        })

res = pd.DataFrame(res_rows)
blank = rng.choice(res.index, size=int(len(res) * 0.01), replace=False)
res.loc[blank, "nurses_on_duty"] = np.nan                    # ~1% missing on purpose
res.to_csv(RAW / "hospital_resource_raw.csv", index=False)
pd.DataFrame(fb_rows).to_csv(RAW / "patient_feedback_raw.csv", index=False)
print("saved department_master, hospital_resource_raw, patient_feedback_raw")
