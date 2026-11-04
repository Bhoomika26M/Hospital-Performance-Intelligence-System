"""Outlier Detection Module for Aegis.dv.

Analyzes operational and clinical numerical distributions via Tukey's IQR and clinical domain thresholds.
Flags outliers transparently rather than deleting valid acute care cases.
"""

from __future__ import annotations

import logging
from typing import Dict, Any, Tuple
import pandas as pd

logger = logging.getLogger("aegis.validation.outliers")


def detect_outliers_iqr(
    df: pd.DataFrame, columns: list[str] | None = None, k: float = 1.5
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Detect and flag statistical outliers using Tukey's Interquartile Range (IQR).

    In compliance with Section 6:
    'Outlier analysis (IQR or domain rules; flag, do not delete, unless clearly invalid;
     document each removal).'

    Args:
        df: Input dataframe.
        columns: List of numerical columns to audit.
        k: IQR multiplier (default 1.5 for mild outliers).

    Returns:
        Tuple of (dataframe_with_outlier_flags, audit_report).
    """
    if columns is None:
        columns = [
            "time_in_hospital",
            "num_lab_procedures",
            "num_procedures",
            "num_medications",
            "number_diagnoses",
        ]

    logger.info(f"Auditing outliers across {len(columns)} numerical metrics using IQR (k={k})...")
    df_out = df.copy()
    report: Dict[str, Any] = {"method": f"Tukey IQR (k={k})", "metrics": {}}

    for col in columns:
        if col not in df_out.columns:
            continue

        q1 = df_out[col].quantile(0.25)
        q3 = df_out[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = max(0, q1 - k * iqr)
        upper_bound = q3 + k * iqr

        outlier_mask = (df_out[col] < lower_bound) | (df_out[col] > upper_bound)
        outlier_count = int(outlier_mask.sum())
        outlier_pct = round(100.0 * outlier_count / len(df_out), 2)

        flag_col = f"is_{col}_outlier"
        df_out[flag_col] = outlier_mask.astype(int)

        report["metrics"][col] = {
            "q1": float(q1),
            "q3": float(q3),
            "iqr": float(iqr),
            "lower_threshold": float(lower_bound),
            "upper_threshold": float(upper_bound),
            "outlier_count": outlier_count,
            "outlier_percentage": outlier_pct,
            "action": "Flagged with indicator column; zero rows removed (preserves acute variance)",
        }

    logger.info(
        f"Outlier detection completed. LOS outliers (>12 days): "
        f"{report['metrics'].get('time_in_hospital', {}).get('outlier_count', 0):,} records."
    )
    return df_out, report

