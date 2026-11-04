"""Unit tests for preprocessing modules: deduplication, missing values, departments, timeline."""

import pytest
import pandas as pd
from pathlib import Path

from src.preprocessing.deduplication import deduplicate_encounters
from src.preprocessing.missing_values import replace_placeholder_tokens, analyze_missing_values
from src.preprocessing.missing_handler import handle_missing_values
from src.preprocessing.department_standardizer import standardize_departments
from src.preprocessing.timeline_normalizer import normalize_encounter_timeline


def test_deduplicate_encounters():
    """Verify deduplication removes duplicate encounters while preserving unique ones."""
    df = pd.DataFrame({
        "encounter_id": [1, 2, 2, 3],
        "patient_nbr": [10, 20, 20, 30],
        "time_in_hospital": [2, 3, 3, 4],
    })
    deduped, audit = deduplicate_encounters(df, key_column="encounter_id")
    assert len(deduped) == 3
    assert audit["duplicates_detected"] == 1
    assert audit["final_row_count"] == 3


def test_missing_values_placeholder_replacement():
    """Verify '?' tokens are converted to NaN and analyzed."""
    df = pd.DataFrame({
        "race": ["Caucasian", "?", "Other"],
        "weight": ["?", "?", "[50-75)"],
    })
    df_clean = replace_placeholder_tokens(df)
    assert df_clean["race"].isna().sum() == 1
    assert df_clean["weight"].isna().sum() == 2


def test_missing_handler_clinical_rules():
    """Verify principled handling of missing attributes."""
    df = pd.DataFrame({
        "medical_specialty": [None, "Cardiology"],
        "race": [None, "Caucasian"],
        "gender": ["Unknown/Invalid", "Female"],
        "payer_code": [None, "MC"],
        "diag_1": [None, "250.0"],
        "diag_2": ["401", None],
        "diag_3": [None, None],
        "weight": [None, "[50-75)"],
    })
    treated, audit = handle_missing_values(df)
    assert treated["medical_specialty"].iloc[0] == "?"
    assert treated["is_specialty_unspecified"].iloc[0] == 1
    assert treated["race"].iloc[0] == "Unknown / Not Reported"
    assert treated["gender"].iloc[0] == "Not Specified"
    assert treated["payer_code"].iloc[0] == "Not Disclosed"
    assert treated["diag_1"].iloc[0] == "000.0"


def test_department_standardizer():
    """Verify specialty mapping to standardized department."""
    df = pd.DataFrame({
        "medical_specialty": ["Cardiology", "InternalMedicine", "Emergency/Trauma", "UNKNOWN_SPECIALTY_TEST"]
    })
    df_dept, audit = standardize_departments(df)
    assert df_dept.loc[0, "department"] == "Cardiology & Vascular"
    assert df_dept.loc[1, "department"] == "General & Internal Medicine"
    assert df_dept.loc[2, "department"] == "Emergency & Trauma"
    # Unmapped defaults cleanly
    assert df_dept.loc[3, "department"] == "General Inpatient / Unspecified"


def test_timeline_normalizer_sequence():
    """Verify discharge date is always greater than or equal to admission date."""
    df = pd.DataFrame({
        "encounter_id": [101, 102, 103],
        "time_in_hospital": [1, 5, 14],
    })
    df_time, audit = normalize_encounter_timeline(df)
    assert audit["timeline_label"] == "Reference timeline (synthetic)"
    
    adm_dt = pd.to_datetime(df_time["admission_date"])
    disch_dt = pd.to_datetime(df_time["discharge_date"])
    
    # Assert valid chronological sequence
    assert (disch_dt >= adm_dt).all()
    # Stay difference equals time_in_hospital
    diff_days = (disch_dt - adm_dt).dt.days
    assert (diff_days == df_time["time_in_hospital"]).all()

