
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "milestone3_data"

files = [
    "daily_occupancy.csv",
    "synthetic_patient_readmissions.csv",
    "patient_transfers.csv"
]

for filename in files:

    file_path = DATA_DIR / filename

    print("\n" + "=" * 55)
    print("FILE:", filename)
    print("=" * 55)

    if file_path.exists():

        df = pd.read_csv(file_path)

        print("Dataset shape:", df.shape)

        print("\nColumn names:")
        print(df.columns.tolist())

        print("\nFirst 5 records:")
        print(df.head().to_string(index=False))

        print("\nMissing values:")
        print(df.isnull().sum().to_string())

    else:
        print("FILE NOT FOUND:", filename)

print("\nDATASET INSPECTION COMPLETED")

