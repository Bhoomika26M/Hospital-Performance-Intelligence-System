"""Synthetic Capacity Generator for Dashboard 4 (Resource Utilization).

Strictly adheres to Section 3's Missing-capability policy:
- File name carries the required 'synthetic_' prefix.
- Every record includes the mandatory column:
  'data_provenance' = 'Synthetic reference data – not real hospital figures'
- Uses a fixed reproducible seed (seed=42).
- Synthetic data never feeds KPIs presented as real clinical encounter figures.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Any
import numpy as np
import pandas as pd

logger = logging.getLogger("aegis.export.synthetic_capacity")


def generate_synthetic_capacity_data(
    output_path: Path | None = None,
    start_date: str = "2008-01-01",
    end_date: str = "2008-12-31",
    random_seed: int = 42,
) -> pd.DataFrame:
    """Generate reproducible daily unit capacity and staffing reference telemetry.

    Args:
        output_path: Destination path for CSV output.
        start_date: Start date for daily calendar.
        end_date: End date for daily calendar.
        random_seed: Seed for reproducibility.

    Returns:
        pd.DataFrame containing synthetic hospital capacity telemetry.
    """
    logger.info("Generating reproducible synthetic hospital capacity telemetry (Section 3 compliant)...")
    if output_path is None:
        output_path = (
            Path(__file__).resolve().parents[2] / "data" / "processed" / "synthetic_hospital_capacity.csv"
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(random_seed)
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    # Defined clinical units with realistic licensed bed allocations (Total = 650 beds)
    units = [
        {"unit": "Cardiology & Vascular", "licensed_beds": 85, "base_occ": 0.82, "nurse_ratio": 3.0},
        {"unit": "General & Internal Medicine", "licensed_beds": 140, "base_occ": 0.88, "nurse_ratio": 4.5},
        {"unit": "General Surgery", "licensed_beds": 90, "base_occ": 0.76, "nurse_ratio": 3.5},
        {"unit": "Emergency & Trauma", "licensed_beds": 60, "base_occ": 0.85, "nurse_ratio": 2.0},
        {"unit": "Orthopedics & Rehab", "licensed_beds": 70, "base_occ": 0.72, "nurse_ratio": 4.0},
        {"unit": "Nephrology & Urology", "licensed_beds": 45, "base_occ": 0.78, "nurse_ratio": 4.0},
        {"unit": "Oncology & Hematology", "licensed_beds": 50, "base_occ": 0.80, "nurse_ratio": 3.0},
        {"unit": "Neurology & Psychiatry", "licensed_beds": 40, "base_occ": 0.70, "nurse_ratio": 4.0},
        {"unit": "Pulmonology", "licensed_beds": 35, "base_occ": 0.84, "nurse_ratio": 3.5},
        {"unit": "Pediatrics", "licensed_beds": 35, "base_occ": 0.65, "nurse_ratio": 2.5},
    ]

    records = []
    for dt in dates:
        # Weekend census dip
        day_factor = 0.93 if dt.dayofweek in [5, 6] else 1.0
        # Seasonal winter surge (Jan-Feb and Nov-Dec)
        season_factor = 1.05 if dt.month in [1, 2, 11, 12] else 0.98

        for u in units:
            unit_name = u["unit"]
            total_beds = u["licensed_beds"]
            mean_occ = u["base_occ"] * day_factor * season_factor
            
            # Stochastic occupancy bounded [0.45, 0.98]
            occ_rate = float(np.clip(rng.normal(loc=mean_occ, scale=0.04), 0.45, 0.98))
            occupied_beds = int(round(total_beds * occ_rate))
            available_beds = total_beds - occupied_beds
            
            # Staffing: on-duty nurses determined by patient load and ratio
            target_nurses = int(round(occupied_beds / u["nurse_ratio"]))
            actual_nurses = max(1, target_nurses + int(rng.integers(-2, 3)))
            patient_to_nurse_ratio = round(occupied_beds / actual_nurses, 2)

            # Equipment utilization for relevant units
            equipment_rate = round(float(np.clip(rng.normal(0.74, 0.08), 0.35, 0.95)) * 100.0, 1)

            records.append({
                "date": dt.strftime("%Y-%m-%d"),
                "year": dt.year,
                "month": dt.month,
                "year_month": dt.strftime("%Y-%m"),
                "day_of_week": dt.day_name(),
                "clinical_unit": unit_name,
                "total_staffed_beds": total_beds,
                "occupied_beds": occupied_beds,
                "available_beds": available_beds,
                "bed_occupancy_rate_pct": round(occ_rate * 100.0, 2),
                "nurses_on_duty": actual_nurses,
                "patient_to_nurse_ratio": patient_to_nurse_ratio,
                "equipment_utilization_pct": equipment_rate,
                "capacity_threshold_status": (
                    "Critical (>90%)" if occ_rate >= 0.90
                    else "Normal (75-90%)" if occ_rate >= 0.75
                    else "Underutilized (<75%)"
                ),
                # MANDATORY SECTION 3 LABEL:
                "data_provenance": "Synthetic reference data – not real hospital figures",
            })

    df_cap = pd.DataFrame(records)
    df_cap.to_csv(output_path, index=False)
    logger.info(
        f"Synthetic hospital capacity generated: {len(df_cap):,} daily unit records "
        f"written to {output_path}."
    )
    return df_cap

