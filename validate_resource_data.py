from pathlib import Path
import sys

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "milestone3_data"
OCCUPANCY_FILE = DATA_DIR / "daily_occupancy.csv"

STAFF_FILE = DATA_DIR / "synthetic_staff_allocation.csv"
STAFF_COLUMNS = [
    "date",
    "hospital",
    "department",
    "shift",
    "staff_role",
    "allocated_staff",
    "required_staff",
    "available_staff",
    "absent_staff",
]
STAFF_COUNT_COLUMNS = [
    "allocated_staff",
    "required_staff",
    "available_staff",
    "absent_staff",
]
STAFF_KEY = ["date", "hospital", "department", "shift", "staff_role"]
SHIFTS = {"Morning", "Evening", "Night"}
STAFF_ROLES = {"Doctors", "Nurses", "Technicians", "Support Staff"}

EQUIPMENT_FILE = DATA_DIR / "synthetic_equipment_utilization.csv"
EQUIPMENT_COLUMNS = [
    "date",
    "hospital",
    "department",
    "equipment_type",
    "total_units",
    "in_use_units",
    "available_units",
    "maintenance_units",
    "utilization_rate",
]
EQUIPMENT_COUNT_COLUMNS = [
    "total_units",
    "in_use_units",
    "available_units",
    "maintenance_units",
]
EQUIPMENT_KEY = ["date", "hospital", "department", "equipment_type"]
EQUIPMENT_TYPES = {
    "Ventilators",
    "Patient Monitors",
    "Infusion Pumps",
    "ECG Machines",
    "Ultrasound Machines",
    "X-Ray Machines",
    "Dialysis Machines",
    "Defibrillators",
}


def report_dataset(
    name: str,
    data: pd.DataFrame,
    required_columns: list[str],
    key_columns: list[str],
) -> tuple[bool, int]:
    missing_columns = set(required_columns) - set(data.columns)
    if missing_columns:
        raise ValueError(
            f"{name} is missing columns: {', '.join(sorted(missing_columns))}"
        )

    missing_values = int(data[required_columns].isna().sum().sum())
    duplicate_records = int(data.duplicated(subset=key_columns).sum())
    print(f"\nDataset: {name}")
    print(f"Records: {len(data):,}")
    print(f"Columns: {len(data.columns)}")
    print(f"Missing values: {missing_values:,}")
    print(f"Duplicate records: {duplicate_records:,}")
    return missing_values == 0, duplicate_records


def check(results: list[tuple[str, bool]], label: str, valid: bool) -> None:
    results.append((label, bool(valid)))
    print(f"  {label}: {'PASS' if valid else 'FAIL'}")


def validate_common(
    data: pd.DataFrame,
    results: list[tuple[str, bool]],
    hospitals: set[str],
    departments: set[str],
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
) -> None:
    dates = pd.to_datetime(data["date"], errors="coerce")
    check(results, "Dates are valid and within occupancy date range",
          dates.notna().all()
          and dates.between(start_date, end_date).all())
    check(results, "Hospital names match daily_occupancy.csv",
          data["hospital"].isin(hospitals).all())
    check(results, "Department names match daily_occupancy.csv",
          data["department"].isin(departments).all())


def validate_staff(
    hospitals: set[str],
    departments: set[str],
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
) -> list[tuple[str, bool]]:
    data = pd.read_csv(STAFF_FILE)
    results: list[tuple[str, bool]] = []
    no_missing, _ = report_dataset(
        STAFF_FILE.name, data, STAFF_COLUMNS, STAFF_KEY
    )
    check(results, "No missing required values", no_missing)
    check(results, "Required columns are present",
          set(STAFF_COLUMNS).issubset(data.columns))
    check(results, "Count columns contain numeric integer values",
          all(
              pd.api.types.is_numeric_dtype(data[column])
              and np.isfinite(data[column]).all()
              and np.equal(data[column], np.floor(data[column])).all()
              for column in STAFF_COUNT_COLUMNS
          ))
    check(results, "Staff counts are non-negative",
          data[STAFF_COUNT_COLUMNS].ge(0).all().all())
    check(results, "Available staff equals allocated minus absent",
          data["available_staff"].eq(
              data["allocated_staff"] - data["absent_staff"]
          ).all())
    check(results, "Absent staff does not exceed allocated staff",
          data["absent_staff"].le(data["allocated_staff"]).all())
    check(results, "Shift categories are valid",
          set(data["shift"].dropna()).issubset(SHIFTS))
    check(results, "Staff role categories are valid",
          set(data["staff_role"].dropna()).issubset(STAFF_ROLES))
    validate_common(
        data, results, hospitals, departments, start_date, end_date
    )
    check(results, "No duplicate staff key records",
          not data.duplicated(subset=STAFF_KEY).any())
    return results


def validate_equipment(
    hospitals: set[str],
    departments: set[str],
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
) -> list[tuple[str, bool]]:
    data = pd.read_csv(EQUIPMENT_FILE)
    results: list[tuple[str, bool]] = []
    no_missing, _ = report_dataset(
        EQUIPMENT_FILE.name, data, EQUIPMENT_COLUMNS, EQUIPMENT_KEY
    )
    check(results, "No missing required values", no_missing)
    check(results, "Required columns are present",
          set(EQUIPMENT_COLUMNS).issubset(data.columns))
    check(results, "Equipment count columns contain numeric integer values",
          all(
              pd.api.types.is_numeric_dtype(data[column])
              and np.isfinite(data[column]).all()
              and np.equal(data[column], np.floor(data[column])).all()
              for column in EQUIPMENT_COUNT_COLUMNS
          ))
    check(results, "Equipment counts are non-negative",
          data[EQUIPMENT_COUNT_COLUMNS].ge(0).all().all())
    check(results, "Equipment counts sum to total units",
          data["in_use_units"]
          .add(data["available_units"])
          .add(data["maintenance_units"])
          .eq(data["total_units"])
          .all())
    operational_units = data["total_units"] - data["maintenance_units"]
    expected_rate = np.divide(
        data["in_use_units"].to_numpy(dtype=float),
        operational_units.to_numpy(dtype=float),
        out=np.zeros(len(data), dtype=float),
        where=operational_units.to_numpy() != 0,
    ) * 100
    check(results, "Utilization rate matches formula (zero operational units => 0%)",
          np.isclose(
              data["utilization_rate"].to_numpy(dtype=float),
              expected_rate,
              atol=0.0051,
              rtol=0,
          ).all())
    check(results, "Utilization rate is between 0 and 100",
          data["utilization_rate"].between(0, 100).all())
    check(results, "Equipment categories are valid",
          set(data["equipment_type"].dropna()).issubset(EQUIPMENT_TYPES))
    validate_common(
        data, results, hospitals, departments, start_date, end_date
    )
    check(results, "No duplicate equipment key records",
          not data.duplicated(subset=EQUIPMENT_KEY).any())
    return results


def main() -> int:
    occupancy = pd.read_csv(OCCUPANCY_FILE)
    occupancy_dates = pd.to_datetime(occupancy["date"], errors="coerce")
    hospitals = set(occupancy["hospital"].dropna().astype(str))
    departments = set(occupancy["department"].dropna().astype(str))
    start_date = occupancy_dates.min()
    end_date = occupancy_dates.max()

    print("=" * 72)
    print("MEDTRACK - SYNTHETIC RESOURCE DATA VALIDATION")
    print("=" * 72)
    print(
        "Reference labels and date range: "
        f"{len(hospitals)} hospitals, {len(departments)} departments, "
        f"{start_date.date()} through {end_date.date()}"
    )

    results = validate_staff(
        hospitals, departments, start_date, end_date
    ) + validate_equipment(
        hospitals, departments, start_date, end_date
    )
    passed = sum(valid for _, valid in results)
    failed = len(results) - passed
    print("\n" + "=" * 72)
    print(f"Validation checks: {passed} passed, {failed} failed")
    print("Overall result:", "PASS" if failed == 0 else "FAIL")
    print("=" * 72)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
