"""Schema Validator Module for Aegis.dv.

Validates that incoming dataframes satisfy structural, column, and range contracts.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Any
import pandas as pd

logger = logging.getLogger("aegis.validation.schema")

REQUIRED_RAW_COLUMNS = [
    "encounter_id",
    "patient_nbr",
    "race",
    "gender",
    "age",
    "admission_type_id",
    "discharge_disposition_id",
    "admission_source_id",
    "time_in_hospital",
    "medical_specialty",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "number_diagnoses",
    "readmitted",
]

ALLOWED_READMISSION_VALUES = {"NO", ">30", "<30"}


def validate_raw_schema(df: pd.DataFrame) -> Dict[str, Any]:
    """Validate that the raw dataframe contains mandatory columns and expected values.

    Args:
        df: Raw dataframe.

    Returns:
        Validation report dictionary.

    Raises:
        ValueError: If mandatory columns or value domains are invalid.
    """
    logger.info("Validating raw encounter schema...")
    report: Dict[str, Any] = {
        "status": "PASS",
        "row_count": len(df),
        "column_count": len(df.columns),
        "missing_mandatory_columns": [],
        "invalid_readmission_values": [],
        "invalid_los_records": 0,
    }

    # 1. Mandatory columns check
    missing_cols = [col for col in REQUIRED_RAW_COLUMNS if col not in df.columns]
    if missing_cols:
        report["status"] = "FAIL"
        report["missing_mandatory_columns"] = missing_cols
        raise ValueError(f"Schema Validation Failed: Missing mandatory columns: {missing_cols}")

    # 2. Check readmitted domain values
    unique_readmit = set(df["readmitted"].dropna().unique())
    invalid_readmit = unique_readmit - ALLOWED_READMISSION_VALUES
    if invalid_readmit:
        report["status"] = "FAIL"
        report["invalid_readmission_values"] = list(invalid_readmit)
        raise ValueError(f"Schema Validation Failed: Unexpected readmitted values: {invalid_readmit}")

    # 3. Check time_in_hospital is positive numeric
    invalid_los = (df["time_in_hospital"] <= 0) | (df["time_in_hospital"] > 365)
    invalid_los_count = int(invalid_los.sum())
    report["invalid_los_records"] = invalid_los_count
    if invalid_los_count > 0:
        report["status"] = "FAIL"
        raise ValueError(f"Schema Validation Failed: Found {invalid_los_count} rows with invalid LOS <= 0 or > 365")

    logger.info(f"Schema validation passed successfully for {len(df):,} records.")
    return report

