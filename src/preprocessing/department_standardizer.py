"""Department Standardization Module for Aegis.dv.

Standardizes granular clinical specialties into hospital operational departments
using a version-controlled taxonomy mapping table.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd

logger = logging.getLogger("aegis.preprocessing.departments")


def standardize_departments(
    df: pd.DataFrame, mapping_path: Path | None = None
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Standardize medical_specialty into clinical operational departments.

    Args:
        df: Input dataframe containing 'medical_specialty'.
        mapping_path: Optional path to specialty_mapping.csv.

    Returns:
        Tuple of (dataframe_with_department, audit_report).
    """
    if mapping_path is None:
        mapping_path = Path(__file__).resolve().parents[2] / "data" / "interim" / "specialty_mapping.csv"

    if not mapping_path.exists():
        raise FileNotFoundError(f"Department mapping file not found at {mapping_path}")

    logger.info(f"Loading department taxonomy from {mapping_path}...")
    map_df = pd.read_csv(mapping_path)
    mapping_dict = dict(zip(map_df["raw_medical_specialty"], map_df["standardized_department"]))

    df_out = df.copy()
    raw_specialties = df_out["medical_specialty"].astype(str)
    
    # Apply mapping
    df_out["department"] = raw_specialties.map(mapping_dict)

    # Detect any unmapped values
    unmapped_mask = df_out["department"].isna()
    unmapped_count = int(unmapped_mask.sum())
    unmapped_specialties = list(df_out.loc[unmapped_mask, "medical_specialty"].unique())

    if unmapped_count > 0:
        logger.warning(
            f"Found {unmapped_count:,} records with unmapped specialty: {unmapped_specialties}. "
            "Defaulting them to 'General Inpatient / Unspecified'."
        )
        df_out["department"] = df_out["department"].fillna("General Inpatient / Unspecified")
    else:
        logger.info(f"100% of specialties successfully mapped to {df_out['department'].nunique()} clinical departments.")

    dept_counts = df_out["department"].value_counts().to_dict()

    audit_report: Dict[str, Any] = {
        "unique_raw_specialties": len(mapping_dict),
        "standardized_departments_count": df_out["department"].nunique(),
        "unmapped_records": unmapped_count,
        "unmapped_specialties": unmapped_specialties,
        "department_distribution": dept_counts,
    }

    return df_out, audit_report

