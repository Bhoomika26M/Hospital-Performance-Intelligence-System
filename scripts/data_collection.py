
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

SOURCE_FILE = DATA_DIR / "healthcare_dataset.csv"
OUTPUT_FILE = DATA_DIR / "hospital_raw_data.csv"


def main():
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(
            f"Source dataset not found: {SOURCE_FILE}"
        )

    df = pd.read_csv(SOURCE_FILE)

    if df.empty:
        raise ValueError("The source dataset is empty.")

    df.columns = df.columns.str.strip()

    df.to_csv(OUTPUT_FILE, index=False)

    print("Data collection completed.")
    print(f"Source: {SOURCE_FILE.name}")
    print(f"Output: {OUTPUT_FILE.name}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print(f"Missing cells: {df.isna().sum().sum()}")
    print("\nColumn names:")
    print(df.columns.tolist())


if __name__ == "__main__":
    main()