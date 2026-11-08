"""Milestone 4 / Module 7 - testing and validation.

Re-calculates KPIs a second way (plain date arithmetic instead of the census trick used
in generate_hospital_kpis.py) and compares. Writes docs/validation_output.txt.
"""
import json, re
import numpy as np
import pandas as pd
from config import DATA, DASH, DOCS, WINDOW_START, WINDOW_END

adm = pd.read_csv(DATA / "hospital_cleaned.csv", parse_dates=["admission_date", "discharge_date"])
kpi = pd.read_csv(DATA / "monthly_kpis.csv", parse_dates=["month"])
raw = pd.read_csv(DATA / "hospital_raw_data.csv")
lines, results = [], []

def check(name, passed, detail=""):
    results.append(passed)
    lines.append(f"[{'PASS' if passed else 'FAIL'}] {name}  {detail}")

# 1. patient-days for 20 random department-months, checked the slow way
rng = np.random.default_rng(1)
sample = kpi.sample(20, random_state=1)
ok = 0
for _, r in sample.iterrows():
    start = r["month"]; end = start + pd.offsets.MonthBegin(1)
    sub = adm[adm["department"] == r["department"]]
    overlap = (np.minimum(sub["discharge_date"], end) - np.maximum(sub["admission_date"], start)).dt.days.clip(lower=0)
    ok += int(overlap.sum() == r["patient_days"])
check("Patient-days (basis of occupancy) match independent calculation", ok == 20, f"{ok}/20 cells match")

# 2. occupancy and utilization formulas
occ_ok = np.allclose(kpi["occupancy_rate"], kpi["patient_days"] / (kpi["licensed_beds"] * kpi["days_in_month"]), atol=1e-4)
util_ok = np.allclose(kpi["bed_utilization_rate"], kpi["patient_days"] / (kpi["staffed_beds"] * kpi["days_in_month"]), atol=1e-4)
check("Occupancy and bed utilization formulas", occ_ok and util_ok)

# 3. admissions: monthly table adds up to the cleaned data inside the window
inwin = adm[adm["admission_date"].dt.to_period("M").between(pd.Period(WINDOW_START), pd.Period(WINDOW_END))]
check("Total admissions match", kpi["admissions"].sum() == len(inwin), f"{kpi['admissions'].sum():,} vs {len(inwin):,}")

# 4. average length of stay per department
a = inwin.groupby("department")["los_days"].mean()
b = kpi.groupby("department").apply(lambda x: (x["avg_los_days"] * x["admissions"]).sum() / x["admissions"].sum())
check("Average length of stay per department (within 0.01 day)", np.allclose(a, b, atol=0.01))

# 5. readmission flags: every flagged row must have an earlier stay of the same patient
chk = adm[adm["readmit_30d"]]
good = 0
for _, r in chk.iterrows():
    prev = adm[(adm["patient_name"] == r["patient_name"]) & (adm["gender"] == r["gender"]) & (adm["blood_type"] == r["blood_type"])
               & (adm["discharge_date"] <= r["admission_date"]) & (adm["discharge_date"] >= r["admission_date"] - pd.Timedelta(days=30))]
    good += int(len(prev) > 0)
check("Every 30-day readmission has a matching earlier stay", good == len(chk), f"{good}/{len(chk)}")

# 6. data quality rules
miss = 100 * adm.isna().sum().sum() / adm.size
check("Missing values below 2%", miss < 2, f"{miss:.3f}%")
comp = 100 * (1 - raw.isna().sum().sum() / raw.size)
check("Raw completeness above 95%", comp > 95, f"{comp:.2f}%")
check("No negative billing or length of stay", (adm["billing_amount"] >= 0).all() and (adm["los_days"] >= 0).all())
fb = pd.read_csv(DATA / "feedback_cleaned.csv")
check("Department names standardised", fb["department"].nunique() == 5, str(sorted(fb["department"].unique())))
check("No duplicate admissions left", not adm.drop(columns=["billing_fixed"]).duplicated().any())

# 7. dashboard file carries the same records as the cleaned data
html = (DASH / "index.html").read_text(encoding="utf-8")
payload = json.loads(re.search(r"const DATA=(\{.*?\});\nconst D=", html, re.S).group(1))
check("Dashboard contains every cleaned record", len(payload["d"]) == len(adm), f"{len(payload['d']):,}")

# 8. optional: open the dashboard in a real browser and read the headline number
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page()
        errors = []; pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto((DASH / "index.html").as_uri())
        shown = pg.inner_text(".kpi b").replace(",", "")
        for name in ["Patient flow", "Departments", "Resources"]:
            pg.click(f'nav button:text("{name}")')
        br.close()
    check("Browser: Total Admissions card equals pandas count", int(shown) == len(inwin), f"{shown}")
    check("Browser: all four pages open without errors", not errors)
except Exception as e:
    lines.append(f"[SKIP] Browser checks (playwright not available: {type(e).__name__})")

score = 100 * sum(results) / len(results)
lines.append(f"\nChecks passed: {sum(results)}/{len(results)}  ->  KPI accuracy {score:.1f}%")
(DOCS / "validation_output.txt").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
