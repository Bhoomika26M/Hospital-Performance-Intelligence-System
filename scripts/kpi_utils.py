"""Shared data + KPI logic for the dashboard, the KPI script and the tests."""
import numpy as np
import pandas as pd

WARMUP_DAYS = 30  # first days of the data have no "already in hospital" patients
DEPT_MAP = {"cancer": "Oncology", "diabetes": "Endocrinology", "hypertension": "General Medicine",
            "obesity": "General Medicine", "arthritis": "Orthopedics", "asthma": "Pulmonology"}


def norm(s):
    return "".join(ch for ch in str(s).lower() if ch.isalnum())


def pick(df, *cands):
    lookup = {norm(c): c for c in df.columns}
    for c in cands:
        if norm(c) in lookup:
            return lookup[norm(c)]
    return None


def build_dataset(raw):
    out = pd.DataFrame()
    out["admit"] = pd.to_datetime(raw[pick(raw, "Date of Admission", "admission_date", "admit_date")])
    out["discharge"] = pd.to_datetime(raw[pick(raw, "Discharge Date", "discharge_date")])
    c = pick(raw, "Region")
    out["region"] = raw[c].astype(str).str.strip() if c else "Unknown"
    c = pick(raw, "Hospital", "hospital_name")
    out["hospital"] = raw[c].astype(str).str.strip() if c else "Hospital"
    c = pick(raw, "Admission Type", "admission_type", "patient_type")
    out["admission_type"] = raw[c].astype(str) if c else "Unknown"
    c = pick(raw, "Name", "patient_name", "patient_id")
    out["patient"] = raw[c].astype(str).str.strip().str.lower() if c else np.arange(len(raw)).astype(str)
    c = pick(raw, "Length of Stay", "los", "length_of_stay", "stay_days")
    out["los"] = pd.to_numeric(raw[c], errors="coerce") if c else (out["discharge"] - out["admit"]).dt.days
    c = pick(raw, "Department", "dept")
    if c:
        out["department"] = raw[c].astype(str).str.strip()
    else:
        mc = pick(raw, "Medical Condition")
        out["department"] = raw[mc].str.lower().map(DEPT_MAP).fillna("General Medicine") if mc else "General"
    c = pick(raw, "Readmitted 30d", "Readmission", "readmitted", "readmission_flag", "is_readmission")
    if c:
        out["readmit"] = raw[c].astype(str).str.lower().isin(
            ["1", "true", "yes", "y", "<30", "readmitted"]).astype(int)
    else:
        t = out.sort_values(["patient", "admit"])
        gap = (t["admit"] - t.groupby("patient")["discharge"].shift()).dt.days
        out["readmit"] = ((gap >= 0) & (gap <= 30)).reindex(out.index).astype(int)
    out = out.dropna(subset=["admit", "discharge"]).reset_index(drop=True)
    out["month"] = out["admit"].dt.to_period("M").dt.to_timestamp()
    return out


def load_dataset(path):
    return build_dataset(pd.read_csv(path))


def load_resources(path):
    r = pd.read_csv(path)
    r.columns = [c.strip() for c in r.columns]
    r["Department"] = r["Department"].str.strip()
    r["Staff"] = r["Doctors"] + r["Nurses"] + r["Technicians"]
    return r

def daily_inhouse(d):
    """Patients in hospital per day (admit day up to, not including, discharge day)."""
    if d.empty:
        return pd.Series(dtype=float)
    idx = pd.date_range(d["admit"].min().normalize(), d["discharge"].max().normalize())
    a = d.groupby(d["admit"].dt.normalize()).size().reindex(idx, fill_value=0)
    o = d.groupby(d["discharge"].dt.normalize()).size().reindex(idx, fill_value=0)
    return (a - o).cumsum()
def warmup_end(df):
    return df["admit"].min().normalize() + pd.Timedelta(days=WARMUP_DAYS)


def window_kpis(base, ih, s, e, cap, warm_from=None):
    """KPIs for admissions in [s, e]. Occupancy ignores the warm-up period when possible."""
    a = base["admit"].dt.normalize()
    w = base[(a >= s) & (a <= e)]
    if w.empty:
        return None
    s_occ = max(s, warm_from) if warm_from is not None else s
    if s_occ > e:
        s_occ = s
    sl = ih.loc[s_occ:e]
    dn = base["discharge"].dt.normalize()
    return dict(adm=len(w), occ=sl.mean() / cap * 100 if len(sl) else np.nan,
                los=w["los"].mean(), readm=w["readmit"].mean() * 100,
                bed=sl.max() / cap * 100 if len(sl) else np.nan,
                disc=int(((dn >= s) & (dn <= e)).sum()))


def department_table(f):
    dep = (f.groupby("department")
             .agg(admissions=("los", "size"), avg_los=("los", "mean"), readmit_rate=("readmit", "mean"))
             .reset_index())
    dep["readmit_rate"] *= 100
    return dep


def efficiency_score(dep, ref):
    """0-100, higher = shorter stay + fewer readmissions.
    Normalised against `ref` (the full-data department table) so the score does not
    change when filters are applied, and does not collapse to 100 for one department."""
    def mm(x, r):
        rng = r.max() - r.min()
        return (x - r.min()) / rng if rng > 0 else x * 0
    s = 100 * (1 - (mm(dep["avg_los"], ref["avg_los"]) + mm(dep["readmit_rate"], ref["readmit_rate"])) / 2)
    return s.clip(0, 100).round(1)