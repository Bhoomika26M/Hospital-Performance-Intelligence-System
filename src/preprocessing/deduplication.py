"""Deduplication Module for Aegis.dv.

Identifies and removes duplicate records using primary encounter keys.
"""

from __future__ import annotations

import logging
from typing import Dict, Any, Tuple
import pandas as pd

logger = logging.getLogger("aegis.preprocessing.deduplication")


def deduplicate_encounters(
    df: pd.DataFrame, key_column: str = "encounter_id"
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Deduplicate records based on primary encounter identifier.

    Args:
        df: Input dataframe.
        key_column: Column name serving as unique encounter key.

    Returns:
        Tuple of (deduplicated_dataframe, deduplication_report).
    """
    logger.info(f"Checking duplicates on key column: '{key_column}'...")
    initial_count = len(df)
    duplicate_mask = df.duplicated(subset=[key_column], keep="first")
    num_duplicates = int(duplicate_mask.sum())

    deduped_df = df[~duplicate_mask].copy()

    report: Dict[str, Any] = {
        "key_column": key_column,
        "initial_row_count": initial_count,
        "duplicates_detected": num_duplicates,
        "final_row_count": len(deduped_df),
        "unique_patients": int(deduped_df["patient_nbr"].nunique()) if "patient_nbr" in deduped_df.columns else None,
        "encounter_to_patient_ratio": round(len(deduped_df) / deduped_df["patient_nbr"].nunique(), 3)
        if "patient_nbr" in deduped_df.columns and deduped_df["patient_nbr"].nunique() > 0
        else 1.0,
    }

    if num_duplicates > 0:
        logger.warning(f"Removed {num_duplicates:,} duplicate rows on {key_column}.")
    else:
        logger.info(f"Zero duplicate records found on {key_column}. Data key is strictly unique.")

    return deduped_df, report

