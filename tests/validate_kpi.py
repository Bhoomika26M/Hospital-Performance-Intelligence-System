"""Step 5 - independent validation of the KPI outputs.

Recomputes the KPIs straight from data/processed/hospital_final.csv WITHOUT importing
kpi_utils.py, then compares them with the files written by generate_hospital_kpis.py.
Also writes every PASS/FAIL result to docs/kpi_validation.csv as testing evidence.

Run from the repo root (after generate_hospital_kpis.py):
    python tests/validate_kpi.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC, RAW = ROOT / "data" / "processed", ROOT / "data" / "raw"
WARMUP_DAYS = 30
failures = []
results = []


def check(name, got, want, tol=0.011):
    ok = abs(float(got) - float(want)) <= tol
    print(f"{'PASS' if ok else 'FAIL'}  {name}: script={got} independent={round(float(want), 4)}")
    results.append({"check": name, "status": "PASS" if ok else "FAIL",
                    "script_value": got, "independent_value": round(float(want), 4)})
    if not ok:
        failures.append(name)


def check_true(name, cond, detail=""):
    print(f"{'PASS' if cond else 'FAIL'}  {name} {detail}")
    results.append({"check": name, "status": "PASS" if cond else "FAIL",
                    "script_value": "", "independent_value": detail})
    if not cond:
        failures.append(name)


# ---------------------------------------------------------------- independent recomputation
raw = pd.read_csv(PROC / "hospital_final.csv",
                  usecols=["Date of Admission", "Discharge Date", "Length of Stay",
                           "Readmitted 30d", "Department", "Region"])
adm = pd.to_datetime(raw["Date of Admission"]).dt.normalize()
dis = pd.to_datetime(raw["Discharge Date"]).dt.normalize()
los = pd.to_numeric(raw["Length of Stay"], errors="coerce")
readm = raw["Readmitted 30d"].astype(str).str.lower().isin(["true", "1"]).astype(int)

res = pd.read_csv(RAW / "department_resources.csv")
res.columns = [c.strip() for c in res.columns]
cap = int(res["Beds Allocated"].sum())

first, last = adm.min(), adm.max()
n_days = (dis.max() - first).days + 1
diff = np.zeros(n_days + 1)
np.add.at(diff, (adm - first).dt.days.to_numpy(), 1)      # +1 on admission day
np.add.at(diff, (dis - first).dt.days.to_numpy(), -1)     # -1 on discharge day (not counted that day)
census = np.cumsum(diff)[:n_days]
hi = (last - first).days


def occ_between(s_idx, e_idx):
    s_idx = max(s_idx, WARMUP_DAYS) if max(s_idx, WARMUP_DAYS) <= e_idx else s_idx
    return census[s_idx:e_idx + 1]


# ---------------------------------------------------------------- 1. overall KPIs
print("\n== Overall ==")
ov = pd.read_csv(PROC / "kpi_overall.csv").set_index("KPI")["Value"]
steady = occ_between(0, hi)
check("Total admissions", ov["Total admissions"], len(raw), tol=0)
check("Avg length of stay", ov["Avg length of stay"], los.mean())
check("Readmission rate %", ov["Readmission rate"], readm.mean() * 100, tol=0.001)
check("Discharges", ov["Discharges"], ((dis >= first) & (dis <= last)).sum(), tol=0)
check("Occupancy %", ov["Occupancy rate"], steady.mean() / cap * 100)
check("Peak bed utilization %", ov["Bed utilization (peak)"], steady.max() / cap * 100)

# ---------------------------------------------------------------- 2. monthly KPIs (full months only)
print("\n== Monthly ==")
mo = pd.read_csv(PROC / "kpi_monthly.csv", parse_dates=["month"])
expected = []
for m in pd.date_range(first.to_period("M").to_timestamp(), last, freq="MS"):
    m_end = m + pd.offsets.MonthEnd(0)
    if m < first or m_end > last:
        continue
    inm = (adm >= m) & (adm <= m_end)
    expected.append({"month": m, "admissions": int(inm.sum()), "avg_los_days": los[inm].mean(),
                     "readmission_pct": readm[inm].mean() * 100,
                     "occupancy_pct": occ_between((m - first).days, (m_end - first).days).mean() / cap * 100})
exp = pd.DataFrame(expected)
check_true("Monthly row count", len(mo) == len(exp), f"(script {len(mo)}, independent {len(exp)})")
check_true("No partial months", mo["month"].min() > first and (mo["month"].max() + pd.offsets.MonthEnd(0)) <= last)
mm = exp.merge(mo, on="month", suffixes=("_i", "_s"))
check_true("Monthly months match", len(mm) == len(exp))
for col in ["admissions", "avg_los_days", "readmission_pct", "occupancy_pct"]:
    worst = (mm[f"{col}_i"] - mm[f"{col}_s"]).abs().max()
    check(f"Monthly {col} (largest gap)", worst, 0, tol=0.011 if col != "readmission_pct" else 0.001)

# ---------------------------------------------------------------- 3. department and region tables
for label, col, path in [("Department", "Department", "kpi_department.csv"), ("Region", "Region", "kpi_region.csv")]:
    print(f"\n== {label} ==")
    t = pd.read_csv(PROC / path)
    key = label.lower()
    g = pd.DataFrame({key: raw[col].astype(str).str.strip(), "los": los, "readm": readm}) \
        .groupby(key).agg(adm=("los", "size"), los=("los", "mean"), readm=("readm", "mean")).reset_index()
    j = g.merge(t, on=key)
    check_true(f"{label} names match", len(j) == len(g) == len(t), f"(independent {len(g)}, script {len(t)})")
    check("Admissions sum", t["admissions"].sum(), len(raw), tol=0)
    check("Admissions (largest gap)", (j["adm"] - j["admissions"]).abs().max(), 0, tol=0)
    check("Avg LOS (largest gap)", (j["los"] - j["avg_los"]).abs().max(), 0)
    rcol = "readmit_rate"
    check("Readmission % (largest gap)", (j["readm"] * 100 - j[rcol]).abs().max(), 0)

dep = pd.read_csv(PROC / "kpi_department.csv")
check_true("Every department has beds and doctors (names match resources file)",
           dep[["beds", "doctors"]].notna().all().all())
check_true("Efficiency scores within 0-100", dep["efficiency_score"].between(0, 100).all())

# ---------------------------------------------------------------- save results as evidence
(ROOT / "docs").mkdir(exist_ok=True)
pd.DataFrame(results).to_csv(ROOT / "docs" / "kpi_validation.csv", index=False)
print("\nWrote docs/kpi_validation.csv")

# ---------------------------------------------------------------- result
print()
if failures:
    print(f"{len(failures)} check(s) FAILED: {failures}")
    sys.exit(1)
print("All checks passed.")