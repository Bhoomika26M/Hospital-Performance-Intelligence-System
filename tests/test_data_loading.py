"""Unit tests for dataset loading, schema validation, and mapping parsing."""

import pytest
import pandas as pd
from pathlib import Path

from src.preprocessing.data_loader import load_raw_data, load_id_mappings
from src.validation.schema_validator import validate_raw_schema, REQUIRED_RAW_COLUMNS


def test_load_id_mappings():
    """Verify that IDs_mapping.csv parses into 3 non-empty dictionaries."""
    adm_map, disch_map, src_map = load_id_mappings()
    assert len(adm_map) >= 8
    assert len(disch_map) >= 25
    assert len(src_map) >= 20
    assert adm_map[1] == "Emergency"
    assert "Expired" in disch_map[11]


def test_schema_validator_valid():
    """Verify schema validator passes on valid sample schema."""
    df_sample = pd.DataFrame({
        "encounter_id": [101, 102],
        "patient_nbr": [1, 2],
        "race": ["Caucasian", "AfricanAmerican"],
        "gender": ["Female", "Male"],
        "age": ["[50-60)", "[60-70)"],
        "admission_type_id": [1, 2],
        "discharge_disposition_id": [1, 1],
        "admission_source_id": [7, 1],
        "time_in_hospital": [3, 4],
        "medical_specialty": ["Cardiology", "InternalMedicine"],
        "num_lab_procedures": [40, 50],
        "num_procedures": [1, 2],
        "num_medications": [10, 15],
        "number_outpatient": [0, 0],
        "number_emergency": [0, 1],
        "number_inpatient": [0, 0],
        "number_diagnoses": [5, 7],
        "readmitted": ["NO", "<30"],
    })
    report = validate_raw_schema(df_sample)
    assert report["status"] == "PASS"


def test_schema_validator_missing_column():
    """Verify schema validator raises ValueError when a mandatory column is missing."""
    df_invalid = pd.DataFrame({"encounter_id": [1], "patient_nbr": [1]})
    with pytest.raises(ValueError, match="Missing mandatory columns"):
        validate_raw_schema(df_invalid)


def test_schema_validator_invalid_readmitted():
    """Verify schema validator detects unexpected target values."""
    df_invalid = pd.DataFrame({col: [1] for col in REQUIRED_RAW_COLUMNS})
    df_invalid["readmitted"] = "INVALID_TOKEN"
    with pytest.raises(ValueError, match="Unexpected readmitted values"):
        validate_raw_schema(df_invalid)

