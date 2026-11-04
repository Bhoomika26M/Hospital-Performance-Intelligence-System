"""KPI Engine Module for Aegis.dv.

Contains pure, mathematically exact, tested functions for calculating hospital
operational, clinical, and patient flow KPIs.
Handles edge cases (division by zero, empty datasets, missing dates, mortality exclusions)
and returns None (rendered as '–' in Tableau) rather than misleading zeros.
"""

from __future__ import annotations

import logging
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd

logger = logging.getLogger("aegis.kpi.engine")


def calculate_total_admissions(
    df: pd.DataFrame, key_column: str = "encounter_id"
) -> int:
    """Calculate Total Admissions as distinct count of valid encounter identifiers.

    Formula: COUNT(DISTINCT encounter_id)
    Denominator: N/A (Volume count)
    Safeguard: Empty dataframe returns 0.
    """
    if df is None or len(df) == 0:
        return 0
    if key_column not in df.columns:
        raise KeyError(f"Key column '{key_column}' not found in dataframe.")
    return int(df[key_column].dropna().nunique())


def calculate_total_discharges(
    df: pd.DataFrame, key_column: str = "encounter_id"
) -> int:
    """Calculate Total Discharges as distinct count of completed hospital stays.

    Formula: COUNT(DISTINCT encounter_id) where stay is completed.
    In the Cerner inpatient dataset, every record represents a completed inpatient stay.
    Denominator: N/A (Volume count)
    """
    if df is None or len(df) == 0:
        return 0
    return int(df[key_column].dropna().nunique())


def calculate_average_length_of_stay(
    df: pd.DataFrame, los_column: str = "time_in_hospital"
) -> Optional[float]:
    """Calculate Average Length of Stay (ALOS) in days.

    Formula: SUM(time_in_hospital) / COUNT(valid_encounters)
    Denominator: Total count of discharged encounters with valid positive LOS.
    Safeguard: Returns None if dataset is empty or denominator is 0.
    """
    if df is None or len(df) == 0:
        return None
    valid_los = df[los_column].dropna()
    valid_los = valid_los[valid_los > 0]
    if len(valid_los) == 0:
        return None
    return round(float(valid_los.mean()), 2)


def calculate_median_length_of_stay(
    df: pd.DataFrame, los_column: str = "time_in_hospital"
) -> Optional[float]:
    """Calculate Median Length of Stay in days (robust to acute right-skew).

    Formula: MEDIAN(time_in_hospital)
    Safeguard: Returns None if dataset is empty.
    """
    if df is None or len(df) == 0:
        return None
    valid_los = df[los_column].dropna()
    valid_los = valid_los[valid_los > 0]
    if len(valid_los) == 0:
        return None
    return round(float(valid_los.median()), 2)


def calculate_los_percentiles(
    df: pd.DataFrame, los_column: str = "time_in_hospital"
) -> Dict[str, Optional[float]]:
    """Calculate 75th and 90th percentiles of Length of Stay.

    Formula: PERCENTILE(time_in_hospital, 0.75), PERCENTILE(time_in_hospital, 0.90)
    """
    if df is None or len(df) == 0:
        return {"p75": None, "p90": None}
    valid_los = df[los_column].dropna()
    valid_los = valid_los[valid_los > 0]
    if len(valid_los) == 0:
        return {"p75": None, "p90": None}
    return {
        "p75": round(float(valid_los.quantile(0.75)), 2),
        "p90": round(float(valid_los.quantile(0.90)), 2),
    }


def calculate_readmission_rate_30d(
    df: pd.DataFrame,
    readmit_column: str = "readmitted_30d_flag",
    eligible_column: str = "is_readmission_eligible",
) -> Optional[float]:
    """Calculate 30-Day Hospital Readmission Rate (CMS/NQF Compliant).

    Formula: (SUM(readmitted_30d_flag) / SUM(is_readmission_eligible)) * 100
    Eligibility: Excludes in-hospital mortality (discharge dispositions 11, 19, 20, 21).
    Denominator: Total eligible discharged patients surviving index stay.
    Safeguard: Returns None if eligible discharges == 0.
    """
    if df is None or len(df) == 0:
        return None
    
    # Filter to eligible discharges
    if eligible_column in df.columns:
        eligible_df = df[df[eligible_column] == 1]
    else:
        eligible_df = df

    denominator = len(eligible_df)
    if denominator == 0:
        return None

    numerator = int(eligible_df[readmit_column].sum())
    return round(float((numerator / denominator) * 100.0), 2)


def calculate_raw_readmission_rate(
    df: pd.DataFrame,
    readmit_column: str = "readmitted_30d_flag",
) -> Optional[float]:
    """Calculate unadjusted readmission rate over all encounters (without mortality exclusion).

    Formula: (COUNT(readmitted < 30) / COUNT(all_encounters)) * 100
    Used for methodology comparison in docs/kpi_dictionary.md.
    """
    if df is None or len(df) == 0:
        return None
    numerator = int(df[readmit_column].sum())
    denominator = len(df)
    if denominator == 0:
        return None
    return round(float((numerator / denominator) * 100.0), 2)


def calculate_emergency_admission_rate(
    df: pd.DataFrame,
    emergency_column: str = "is_emergency_admission",
) -> Optional[float]:
    """Calculate percentage of admissions entering via Emergency / Trauma.

    Formula: (COUNT(emergency_admissions) / COUNT(total_admissions)) * 100
    """
    if df is None or len(df) == 0:
        return None
    numerator = int(df[emergency_column].sum())
    denominator = len(df)
    if denominator == 0:
        return None
    return round(float((numerator / denominator) * 100.0), 2)


def calculate_total_patient_days(
    df: pd.DataFrame, los_column: str = "time_in_hospital"
) -> int:
    """Calculate Total Patient-Days as the authentic workload proxy.

    Formula: SUM(time_in_hospital) across all stays in period.
    Per Section 4/5: Authentic workload proxy in absence of physical bed telemetry.
    """
    if df is None or len(df) == 0:
        return 0
    return int(df[los_column].dropna().sum())


def calculate_bed_occupancy_rate(
    df: pd.DataFrame,
    occupied_bed_days: Optional[float] = None,
    available_bed_days: Optional[float] = None,
) -> Optional[float]:
    """Calculate Bed Occupancy Rate.

    Formula: (occupied_bed_days / available_bed_days) * 100
    Per Section 3 & 5 Policy:
    Returns None if capacity data is unavailable in the primary dataset.
    """
    if occupied_bed_days is None or available_bed_days is None or available_bed_days <= 0:
        # Strictly enforces Missing-capability policy
        return None
    return round(float((occupied_bed_days / available_bed_days) * 100.0), 2)


def calculate_department_summary(
    df: pd.DataFrame, min_sample_size: int = 30
) -> pd.DataFrame:
    """Generate department-level operational performance table.

    Fair comparison rules (Section 4):
    - Suppresses or flags departments with sample size < min_sample_size (default n=30).
    - Normalizes metrics: ALOS, Readmission Rate, Emergency Rate, Patient Share.

    Args:
        df: Input dataframe.
        min_sample_size: Minimum discharge count threshold.

    Returns:
        pd.DataFrame containing department-level operational KPIs.
    """
    if df is None or len(df) == 0:
        return pd.DataFrame()

    total_encounters = len(df)
    records = []

    for dept, group in df.groupby("department"):
        n_admissions = len(group)
        n_discharges = n_admissions
        alos = round(float(group["time_in_hospital"].mean()), 2)
        med_los = round(float(group["time_in_hospital"].median()), 2)
        
        # Readmission rate on eligible patients
        eligible_group = group[group["is_readmission_eligible"] == 1]
        n_eligible = len(eligible_group)
        if n_eligible > 0:
            readmit_rate = round(float((eligible_group["readmitted_30d_flag"].sum() / n_eligible) * 100.0), 2)
        else:
            readmit_rate = None

        emer_rate = round(float((group["is_emergency_admission"].sum() / n_admissions) * 100.0), 2)
        tot_patient_days = int(group["time_in_hospital"].sum())
        vol_share = round(float((n_admissions / total_encounters) * 100.0), 2)
        mean_intensity = round(float(group["clinical_intensity_index"].mean()), 2)

        # Flag small sample size
        is_statistically_robust = int(n_admissions >= min_sample_size)
        sample_warning = "Robust Sample" if is_statistically_robust else f"Low Sample (n={n_admissions} < {min_sample_size})"

        records.append({
            "department": dept,
            "total_admissions": n_admissions,
            "total_discharges": n_discharges,
            "volume_share_pct": vol_share,
            "average_los_days": alos,
            "median_los_days": med_los,
            "readmission_rate_30d_pct": readmit_rate,
            "emergency_admission_rate_pct": emer_rate,
            "total_patient_days": tot_patient_days,
            "mean_clinical_intensity": mean_intensity,
            "is_statistically_robust": is_statistically_robust,
            "sample_warning": sample_warning,
        })

    summary_df = pd.DataFrame(records).sort_values(by="total_admissions", ascending=False).reset_index(drop=True)
    return summary_df


def compute_headline_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Compute executive headline scorecard KPIs for Dashboard 1 (Hospital Overview)."""
    percentiles = calculate_los_percentiles(df)
    return {
        "total_admissions": calculate_total_admissions(df),
        "total_discharges": calculate_total_discharges(df),
        "average_los_days": calculate_average_length_of_stay(df),
        "median_los_days": calculate_median_length_of_stay(df),
        "los_p75_days": percentiles["p75"],
        "los_p90_days": percentiles["p90"],
        "readmission_rate_30d_pct": calculate_readmission_rate_30d(df),
        "raw_readmission_rate_pct": calculate_raw_readmission_rate(df),
        "emergency_admission_rate_pct": calculate_emergency_admission_rate(df),
        "total_patient_days": calculate_total_patient_days(df),
        "total_departments": int(df["department"].nunique()) if "department" in df.columns else 0,
        "bed_occupancy_rate_real": calculate_bed_occupancy_rate(df),  # Returns None (Unavailable per Sec 3)
    }

