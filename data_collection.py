"""
MedTrack_DV - Milestone 1: Data Collection
-----------------------------------------
Collects the hospital admissions CSV from a local file or a user-supplied URL.

Examples:
    python data_collection.py --input healthcare_dataset.csv
    python data_collection.py --input healthcare_dataset.csv --output hospital_raw_data.csv
    python data_collection.py --url "https://example.com/dataset.csv" --output hospital_raw_data.csv

Note:
    No dataset URL is hard-coded because the project files do not identify
    a verified original download URL. Supply a trusted CSV URL only if needed.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.request import urlopen
import pandas as pd

REQUIRED_COLUMNS = {
    "Name", "Age", "Gender", "Blood Type", "Medical Condition",
    "Date of Admission", "Doctor", "Hospital", "Insurance Provider",
    "Billing Amount", "Room Number", "Admission Type", "Discharge Date",
    "Medication", "Test Results",
}

def load_dataset(input_path: str | None, url: str | None) -> pd.DataFrame:
    """Load a CSV from a local path or an explicitly supplied URL."""
    if input_path:
        path = Path(input_path).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"Input CSV not found: {path}")
        return pd.read_csv(path)

    if url:
        # pandas can read a public CSV URL directly.
        return pd.read_csv(url)

    raise ValueError("Provide either --input PATH or --url URL.")

def validate_dataset(df: pd.DataFrame) -> None:
    """Check that the expected hospital dataset fields are present."""
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(
            "The input file is missing required columns: "
            + ", ".join(sorted(missing))
        )
    if df.empty:
        raise ValueError("The input dataset contains no records.")

def main() -> None:
    parser = argparse.ArgumentParser(description="Collect MedTrack_DV hospital data.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", help="Path to the downloaded source CSV.")
    source.add_argument("--url", help="Trusted direct URL to a CSV file.")
    parser.add_argument(
        "--output",
        default="hospital_raw_data.csv",
        help="Output filename (default: hospital_raw_data.csv).",
    )
    args = parser.parse_args()

    df = load_dataset(args.input, args.url)
    validate_dataset(df)

    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print("Data collection completed successfully.")
    print(f"Source records: {len(df):,}")
    print(f"Columns collected: {len(df.columns)}")
    print(f"Output file: {output_path.resolve()}")
    print(f"Duplicate rows detected (not removed at this stage): {df.duplicated().sum():,}")

if __name__ == "__main__":
    main()
