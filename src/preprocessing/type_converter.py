"""Data Type Conversion Module for Aegis.dv.

Enforces strict Python/Pandas dtypes for memory optimization, numerical precision,
and Tableau-ready schema stability.
"""

from __future__ import annotations

import logging
from typing import Dict, Any, Tuple
import pandas as pd

logger = logging.getLogger("aegis.preprocessing.types")

NUMERIC_COLUMNS = [
    "encounter_id",
    "patient_nbr",
    "admission_type_id",
    "discharge_disposition_id",
    "admission_source_id",
    "time_in_hospital",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "number_diagnoses",
]


def convert_data_types(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Convert and enforce optimal schema data types.

    Args:
        df: Input dataframe.

    Returns:
        Tuple of (typed_dataframe, audit_report).
    """
    logger.info("Enforcing strict column data types...")
    df_out = df.copy()

    conversions = {}

    # Numeric conversion
    for col in NUMERIC_COLUMNS:
        if col in df_out.columns:
            df_out[col] = pd.to_numeric(df_out[col], errors="coerce").fillna(0).astype(int)
            conversions[col] = "int64"

    # String / Categorical columns
    str_cols = [
        "race",
        "gender",
        "age",
        "payer_code",
        "medical_specialty",
        "department",
        "diag_1",
        "diag_2",
        "diag_3",
        "readmitted",
        "change",
        "diabetesMed",
        "timeline_type",
    ]
    for col in str_cols:
        if col in df_out.columns:
            df_out[col] = df_out[col].astype(str)
            conversions[col] = "string"

    audit_report = {
        "columns_converted": len(conversions),
        "conversions": conversions,
    }

    logger.info(f"Type conversions complete across {len(conversions)} columns.")
    return df_out, audit_report

