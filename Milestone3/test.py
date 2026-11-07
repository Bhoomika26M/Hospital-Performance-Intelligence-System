
import pandas as pd
import numpy as np
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

WEEKLY_PATH = DATA_DIR / "hospital_cleaned.csv"
ADMISSION_PATH = DATA_DIR / "hospital_admissions_cleaned.csv"

@pytest.fixture(scope="module")
def weekly_df():
    return pd.read_csv(WEEKLY_PATH)


@pytest.fixture(scope="module")
def admission_df():
    return pd.read_csv(ADMISSION_PATH)

def test_required_files_and_columns():

    assert (BASE_DIR / "app.py").exists()
    assert WEEKLY_PATH.exists()
    assert ADMISSION_PATH.exists()

    weekly = pd.read_csv(WEEKLY_PATH)
    admissions = pd.read_csv(ADMISSION_PATH)

    required_weekly = [
        "week", "service", "available_beds",
        "patients_admitted", "patient_count",
        "staff_present", "staff_count"
    ]

    required_admissions = [
        "admission_id", "admission_date",
        "department", "length_of_stay_days",
        "is_readmission_30d", "patient_satisfaction"
    ]

    assert set(required_weekly).issubset(weekly.columns)
    assert set(required_admissions).issubset(admissions.columns)

def test_admission_records_and_dates(admission_df):

    assert admission_df["admission_id"].notna().all()
    assert admission_df["admission_id"].is_unique

    dates = pd.to_datetime(
        admission_df["admission_date"],
        errors="coerce"
    )
    assert dates.notna().all()

def test_numeric_values_are_non_negative(weekly_df, admission_df):

    weekly_columns = [
        "available_beds",
        "patients_admitted",
        "patient_count",
        "staff_count"
    ]

    admission_columns = [
        "age",
        "length_of_stay_days",
        "billing_amount"
    ]

    for column in weekly_columns:
        assert (weekly_df[column] >= 0).all()

    for column in admission_columns:
        assert (admission_df[column] >= 0).all()

def test_satisfaction_scores_are_valid(admission_df):

    scores = admission_df["patient_satisfaction"].dropna()

    assert scores.between(1, 5).all()

def test_total_admissions(weekly_df):

    total = weekly_df["patients_admitted"].sum()

    assert total == 5851


def test_average_length_of_stay(admission_df):

    avg_los = admission_df["length_of_stay_days"].mean()

    assert avg_los == pytest.approx(4.5724408262)


def test_readmission_rate(admission_df):

    readmission_rate = (
        admission_df["is_readmission_30d"]
        .dropna()
        .astype(bool)
        .mean() * 100
    )

    assert readmission_rate == pytest.approx(10.5985225388)

def test_patient_satisfaction(admission_df):

    satisfaction = admission_df["patient_satisfaction"].mean()

    assert satisfaction == pytest.approx(3.7591268926)


def test_department_filtering(admission_df):

    departments = admission_df["department"].dropna().unique()

    selected = departments[0]

    filtered = admission_df[
        admission_df["department"] == selected
    ]

    assert not filtered.empty
    assert filtered["department"].eq(selected).all()


def test_resource_utilization(weekly_df):

    assert (weekly_df["available_beds"] > 0).all()

    bed_utilization = (
        weekly_df["patient_count"]
        * weekly_df["average_length_of_stay"]
        / (weekly_df["available_beds"] * 7)
        * 100
    )

    assert np.isfinite(bed_utilization).all()

    staff_coverage = (
        weekly_df["staff_present"]
        / weekly_df["staff_count"]
        * 100
    )

    assert np.isfinite(staff_coverage).all()


def generate_kpi_report():

    weekly_df = pd.read_csv(WEEKLY_PATH)
    admission_df = pd.read_csv(ADMISSION_PATH)

    print("\n" + "=" * 60)
    print("       HOSPITAL PERFORMANCE INTELLIGENCE")
    print("                  KPI REPORT")
    print("=" * 60)

    total_admissions = weekly_df["patients_admitted"].sum()

    avg_los = admission_df["length_of_stay_days"].mean()

    readmission_rate = (
        admission_df["is_readmission_30d"]
        .dropna()
        .astype(bool)
        .mean() * 100
    )

    satisfaction = admission_df["patient_satisfaction"].mean()

    bed_utilization = (
        weekly_df["patient_count"]
        * weekly_df["average_length_of_stay"]
        / (weekly_df["available_beds"] * 7)
        * 100
    ).mean()

    staff_coverage = (
        weekly_df["staff_present"]
        / weekly_df["staff_count"]
        * 100
    ).mean()

    print("\nKPI RESULTS")
    print(f"Total Admissions          : {total_admissions:,.0f}")
    print(f"Average Length of Stay    : {avg_los:.2f} days")
    print(f"Readmission Rate          : {readmission_rate:.2f}%")
    print(f"Patient Satisfaction      : {satisfaction:.2f} / 5")
    print(f"Average Bed Utilization   : {bed_utilization:.2f}%")
    print(f"Average Staff Coverage    : {staff_coverage:.2f}%")


    print("\nDEPARTMENT PERFORMANCE")
    department_stats = (
        admission_df.groupby("department")
        .agg(
            admissions=("admission_id", "count"),
            avg_los=("length_of_stay_days", "mean"),
            satisfaction=("patient_satisfaction", "mean")
        )
        .sort_values("avg_los")
    )

    print(department_stats.round(2).to_string())

    print("\nDATA QUALITY CHECK")

    print(f"Weekly Records            : {len(weekly_df):,}")
    print(f"Admission Records         : {len(admission_df):,}")
    print(f"Weekly Missing Values     : {weekly_df.isnull().sum().sum()}")
    print(f"Admission Missing Values  : {admission_df.isnull().sum().sum()}")

if __name__ == "__main__":
    generate_kpi_report()
