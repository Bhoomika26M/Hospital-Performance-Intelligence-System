"""SIMULATED monthly equipment hours per department -> data/raw/equipment_utilization.csv"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kpi_utils import load_dataset, load_resources

ROOT = Path(__file__).resolve().parents[1]
df = load_dataset(ROOT / "data" / "processed" / "hospital_final.csv")
res = load_resources(ROOT / "data" / "raw" / "department_resources.csv")

months = pd.date_range(df["admit"].min().to_period("M").to_timestamp(), df["admit"].max(), freq="MS")
rng = np.random.default_rng(42)
rows = []
for dept in res["Department"].unique():
    for m in months:
        avail = int(rng.integers(300, 600))
        rows.append({"department": dept, "month": m.date(), "available_hours": avail,
                     "used_hours": int(avail * rng.uniform(0.45, 0.95))})
pd.DataFrame(rows).to_csv(ROOT / "data" / "raw" / "equipment_utilization.csv", index=False)
print("Saved equipment_utilization.csv:", len(rows), "rows")
