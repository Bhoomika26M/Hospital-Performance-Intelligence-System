
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
file_path = base_dir / "data" / "hospital-resource-allocation-records.csv"

df = pd.read_csv(file_path)

print("\n--- BED ALLOCATION ISSUES ---")
bed_issues = df[df["beds_allocated"] <= 0]
print(bed_issues[
    ["hospital_name", "allocation_date",
     "beds_allocated", "beds_occupied", "bed_type"]
].to_string(index=False))

print("\n--- STAFF ALLOCATION ISSUES ---")
staff_issues = df[df["staff_allocated"] <= 0]
print(staff_issues[
    ["hospital_name", "allocation_date",
     "staff_type", "staff_allocated", "staff_on_duty"]
].to_string(index=False))

print("\nInspection completed.")
