"""Unit tests for pure KPI calculation functions and edge-case safeguards."""

import pytest
import pandas as pd
import numpy as np

from src.kpi.kpi_engine import (
    calculate_total_admissions,
    calculate_total_discharges,
    calculate_average_length_of_stay,
    calculate_median_length_of_stay,
    calculate_los_percentiles,
    calculate_readmission_rate_30d,
    calculate_raw_readmission_rate,
    calculate_emergency_admission_rate,
    calculate_total_patient_days,
    calculate_bed_occupancy_rate,
    calculate_department_summary,
    compute_headline_kpis,
)


@pytest.fixture
def sample_hospital_df():
    """Hand-computed 5-patient test fixture.
    
    Patient 1: LOS 2 days, Discharged Home (disp 1), Readmitted <30
    Patient 2: LOS 4 days, Discharged Home (disp 1), Not readmitted (NO)
    Patient 3: LOS 6 days, Transferred (disp 2), Readmitted >30
    Patient 4: LOS 3 days, Expired (disp 11 - mortality), NO (Ineligible for readmission!)
    Patient 5: LOS 5 days, Emergency (type 1), Discharged Home (disp 1), Readmitted <30
    
    Expected hand-computed metrics:
    - Total Admissions: 5
    - Total Discharges: 5
    - Total Patient-Days: 2 + 4 + 6 + 3 + 5 = 20
    - Mean LOS: 20 / 5 = 4.00 days
    - Median LOS: 4.00 days (sorted: 2, 3, 4, 5, 6)
    - P75 LOS: 5.00 days, P90: 5.60 days
    - Expired: 1 (Patient 4)
    - Eligible Survivors: 4 (Patients 1, 2, 3, 5)
    - Readmitted <30 among survivors: 2 (Patients 1, 5)
    - CMS 30-Day Readmission Rate: (2 / 4) * 100 = 50.00%
    - Raw Readmission Rate: (2 / 5) * 100 = 40.00%
    - Emergency Admissions: 1 (Patient 5) -> Emergency Rate: (1 / 5) * 100 = 20.00%
    """
    return pd.DataFrame({
        "encounter_id": [101, 102, 103, 104, 105],
        "patient_nbr": [1, 2, 3, 4, 5],
        "time_in_hospital": [2, 4, 6, 3, 5],
        "discharge_disposition_id": [1, 1, 2, 11, 1],
        "is_in_hospital_death": [0, 0, 0, 1, 0],
        "is_readmission_eligible": [1, 1, 1, 0, 1],
        "readmitted_30d_flag": [1, 0, 0, 0, 1],
        "readmitted": ["<30", "NO", ">30", "NO", "<30"],
        "is_emergency_admission": [0, 0, 0, 0, 1],
        "department": ["Cardiology", "Cardiology", "InternalMed", "InternalMed", "Emergency"],
        "clinical_intensity_index": [20.0, 22.0, 18.0, 15.0, 25.0],
    })


def test_hand_computed_kpis(sample_hospital_df):
    """Verify exact hand-computed values match pure KPI functions."""
    assert calculate_total_admissions(sample_hospital_df) == 5
    assert calculate_total_discharges(sample_hospital_df) == 5
    assert calculate_total_patient_days(sample_hospital_df) == 20
    assert calculate_average_length_of_stay(sample_hospital_df) == 4.00
    assert calculate_median_length_of_stay(sample_hospital_df) == 4.00
    
    pcts = calculate_los_percentiles(sample_hospital_df)
    assert pcts["p75"] == 5.00

    # CMS Readmission excludes patient 4 (in-hospital death)
    assert calculate_readmission_rate_30d(sample_hospital_df) == 50.00
    # Raw includes all 5
    assert calculate_raw_readmission_rate(sample_hospital_df) == 40.00
    assert calculate_emergency_admission_rate(sample_hospital_df) == 20.00


def test_empty_dataset_safeguard():
    """Verify empty dataframe returns 0 or None rather than crashing or returning NaN."""
    empty_df = pd.DataFrame()
    assert calculate_total_admissions(empty_df) == 0
    assert calculate_total_discharges(empty_df) == 0
    assert calculate_average_length_of_stay(empty_df) is None
    assert calculate_median_length_of_stay(empty_df) is None
    assert calculate_readmission_rate_30d(empty_df) is None
    assert calculate_total_patient_days(empty_df) == 0


def test_division_by_zero_safeguard():
    """Verify zero-denominator cases return None (Tableau '-') instead of inf or zero."""
    # Stays with zero positive LOS
    df_zero_los = pd.DataFrame({"encounter_id": [1], "time_in_hospital": [0]})
    assert calculate_average_length_of_stay(df_zero_los) is None

    # Stays where 100% of patients died (0 eligible survivors)
    df_all_expired = pd.DataFrame({
        "encounter_id": [1, 2],
        "is_readmission_eligible": [0, 0],
        "readmitted_30d_flag": [0, 0],
    })
    assert calculate_readmission_rate_30d(df_all_expired) is None


def test_single_record_fixture():
    """Verify KPI engine handles single record edge cases."""
    df_single = pd.DataFrame({
        "encounter_id": [999],
        "time_in_hospital": [7],
        "is_readmission_eligible": [1],
        "readmitted_30d_flag": [1],
        "is_emergency_admission": [1],
    })
    assert calculate_total_admissions(df_single) == 1
    assert calculate_average_length_of_stay(df_single) == 7.00
    assert calculate_median_length_of_stay(df_single) == 7.00
    assert calculate_readmission_rate_30d(df_single) == 100.00
    assert calculate_emergency_admission_rate(df_single) == 100.00


def test_bed_occupancy_safeguard():
    """Verify bed occupancy returns None when capacity telemetry is absent (Section 3)."""
    df = pd.DataFrame({"encounter_id": [1, 2], "time_in_hospital": [3, 4]})
    assert calculate_bed_occupancy_rate(df) is None
    # If valid telemetry is supplied
    assert calculate_bed_occupancy_rate(df, occupied_bed_days=80, available_bed_days=100) == 80.00


def test_department_summary_sample_suppression(sample_hospital_df):
    """Verify department summary applies min_sample_size flag."""
    # Min sample size 3: Cardiology has 2, InternalMed has 2, Emergency has 1 -> all low sample
    summary_df = calculate_department_summary(sample_hospital_df, min_sample_size=3)
    assert len(summary_df) == 3
    assert (summary_df["is_statistically_robust"] == 0).all()

    # Min sample size 2: Cardiology (2) and InternalMed (2) robust
    summary_df2 = calculate_department_summary(sample_hospital_df, min_sample_size=2)
    cardio_row = summary_df2[summary_df2["department"] == "Cardiology"].iloc[0]
    assert cardio_row["is_statistically_robust"] == 1
    assert cardio_row["sample_warning"] == "Robust Sample"

