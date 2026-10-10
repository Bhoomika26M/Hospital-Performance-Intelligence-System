
from pathlib import Path
import shutil
import pandas as pd

# Project directories
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

# Input and output files
SOURCE_FILE = RAW_DIR / "healthcare_dataset (1).csv"
OUTPUT_FILE = RAW_DIR / "hospital_raw_data.csv"


def collect_hospital_data():
    """Validate, copy, and report the raw hospital dataset."""

    if not SOURCE_FILE.exists():
        raise FileNotFoundError(
            f"Source dataset not found: {SOURCE_FILE}"
        )

    # Read the source dataset to validate that it is usable
    df = pd.read_csv(SOURCE_FILE)

    if df.empty:
        raise ValueError("The source dataset is empty.")

    # Preserve the original file and create the project deliverable
    shutil.copy2(SOURCE_FILE, OUTPUT_FILE)

    print("Data collection completed successfully!")
    print(f"Source file: {SOURCE_FILE}")
    print(f"Collected file: {OUTPUT_FILE}")
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")


if __name__ == "__main__":
    collect_hospital_data()