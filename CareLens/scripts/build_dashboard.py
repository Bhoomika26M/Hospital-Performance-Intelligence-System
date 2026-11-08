"""Milestone 3 - build the dashboard.

Packs the cleaned data into dashboard/index.html (one file, no internet needed).
Open the file in any browser, or turn on GitHub Pages to share it as a link.
"""
import json
import pandas as pd
from config import DATA, DASH, RAW, WINDOW_START, WINDOW_END
from utils import day_index, N_DAYS

adm = pd.read_csv(DATA / "hospital_cleaned.csv", parse_dates=["admission_date", "discharge_date"])
res = pd.read_csv(DATA / "resource_cleaned.csv")
fb = pd.read_csv(DATA / "feedback_cleaned.csv")
master = pd.read_csv(RAW / "department_master.csv")

depts = master["department"].tolist()
atypes = ["Elective", "Emergency", "Urgent"]
ages = ["0-17", "18-34", "35-49", "50-64", "65+"]
results = ["Normal", "Abnormal", "Inconclusive"]
months = [str(m) for m in pd.period_range(WINDOW_START, WINDOW_END, freq="M")]

r = res.merge(fb, on=["month", "department"])
R = []
for d in depts:
    x = r[r["department"] == d].sort_values("month")
    R.append(x[["staffed_beds", "nurses_on_duty", "doctors_on_roster", "equipment_units_available",
                "equipment_hours_available", "equipment_hours_used", "avg_satisfaction",
                "responses", "avg_wait_minutes"]].round(2).values.tolist())

payload = {
    "ndays": N_DAYS, "months": months, "depts": depts, "atypes": atypes, "ages": ages, "results": results,
    "master": [{"lic": int(a), "target": float(b)} for a, b in zip(master["licensed_beds"], master["target_los_days"])],
    "d": day_index(adm["admission_date"]).tolist(),
    "l": adm["los_days"].tolist(),
    "p": adm["department"].map(depts.index).tolist(),
    "t": adm["admission_type"].map(atypes.index).tolist(),
    "g": adm["age_group"].map(ages.index).tolist(),
    "r": adm["test_results"].map(results.index).tolist(),
    "x": adm["readmit_30d"].astype(int).tolist(),
    "R": R,
}
html = (DASH / "template.html").read_text(encoding="utf-8").replace("__DATA__", json.dumps(payload, separators=(",", ":")))
(DASH / "index.html").write_text(html, encoding="utf-8")
print(f"dashboard/index.html written ({len(html)/1e6:.2f} MB)")
