
from pathlib import Path
import pandas as pd
import numpy as np

# Find the project folder and input CSV
ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "data" / "hospital_dashboard_data.csv"
OUTPUT_FILE = ROOT / "data" / "hospital_dashboard_demo_data.csv"

# Load the original dataset
df = pd.read_csv(INPUT_FILE)

# Use a fixed seed so the demo values are reproducible
rng = np.random.default_rng(42)

rows = len(df)

# 1. Simulated department names
departments = [
    "Cardiology",
    "Neurology",
    "Orthopedics",
    "General Medicine",
    "Oncology",
    "Emergency"
]

df["demo_department"] = rng.choice(departments, size=rows)

# 2. Simulated bed information
df["demo_available_beds"] = rng.integers(100, 501, size=rows)

df["demo_occupied_beds"] = [
    rng.integers(0, beds + 1)
    for beds in df["demo_available_beds"]
]

df["demo_bed_occupancy_pct"] = (
    df["demo_occupied_beds"]
    / df["demo_available_beds"]
    * 100
).round(2)

# 3. Simulated staff information
df["demo_staff_count"] = rng.integers(10, 101, size=rows)

df["demo_staff_working_hours"] = (
    rng.integers(4, 13, size=rows)
)

# 4. Simulated equipment information
df["demo_equipment_available_count"] = rng.integers(
    5, 51, size=rows
)

df["demo_equipment_usage_hours"] = (
    rng.random(rows) * 24
).round(2)

# 5. Simulated patient transfer information
df["demo_transfer_count"] = rng.integers(0, 4, size=rows)

wards = [
    "ICU",
    "General Ward",
    "Surgical Ward",
    "Recovery Ward"
]

df["demo_transfer_destination"] = [
    rng.choice(wards) if count > 0 else "No transfer"
    for count in df["demo_transfer_count"]
]

# Clearly identify the added values as simulated
df["demo_data_note"] = "SIMULATED - NOT REAL HOSPITAL DATA"

# Save as a new file; preserve the original CSV
df.to_csv(OUTPUT_FILE, index=False)

print("Demo dataset created successfully!")
print("Output file:", OUTPUT_FILE)
print("Number of records:", len(df))
print("\nNew demo columns:")
print([
    "demo_department",
    "demo_available_beds",
    "demo_occupied_beds",
    "demo_bed_occupancy_pct",
    "demo_staff_count",
    "demo_staff_working_hours",
    "demo_equipment_available_count",
    "demo_equipment_usage_hours",
    "demo_transfer_count",
    "demo_transfer_destination",
    "demo_data_note"
])
