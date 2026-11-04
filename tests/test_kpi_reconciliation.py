"""Reconciliation test comparing primary KPI engine against an independent second implementation."""

from pathlib import Path
import csv
import statistics
import pandas as pd
import pytest

from src.kpi.kpi_engine import compute_headline_kpis

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_independent_reconciliation_headline_kpis():
    """Reconcile KPI values against a completely independent procedural CSV accumulator.
    
    This fulfills Section 11 requirement:
    'A reconciliation test that recomputes headline KPIs independently
     (a second, differently written implementation) and compares them.'
    """
    csv_path = PROJECT_ROOT / "data" / "processed" / "hospital_cleaned.csv"
    assert csv_path.exists()

    # Implementation 1: Primary Pipeline Pandas KPI Engine
    df = pd.read_csv(csv_path, low_memory=False)
    kpis_primary = compute_headline_kpis(df)

    # Implementation 2: Pure Procedural CSV Reader (Independent Logic)
    unique_encounters = set()
    total_stays = 0
    total_days = 0
    los_values = []
    eligible_count = 0
    readmit_30d_count = 0
    emergency_count = 0

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            enc_id = row["encounter_id"]
            unique_encounters.add(enc_id)
            total_stays += 1
            
            los = int(row["time_in_hospital"])
            total_days += los
            los_values.append(los)

            is_eligible = int(row["is_readmission_eligible"])
            readmit_30 = int(row["readmitted_30d_flag"])
            if is_eligible == 1:
                eligible_count += 1
                if readmit_30 == 1:
                    readmit_30d_count += 1

            if int(row["is_emergency_admission"]) == 1:
                emergency_count += 1

    reconciled_admissions = len(unique_encounters)
    reconciled_discharges = total_stays
    reconciled_alos = round(total_days / total_stays, 2)
    reconciled_median_los = round(statistics.median(los_values), 2)
    reconciled_readmission_rate = round((readmit_30d_count / eligible_count) * 100.0, 2)
    reconciled_emergency_rate = round((emergency_count / total_stays) * 100.0, 2)

    # Compare Both Independent Implementations
    assert kpis_primary["total_admissions"] == reconciled_admissions == 101766
    assert kpis_primary["total_discharges"] == reconciled_discharges == 101766
    assert kpis_primary["total_patient_days"] == total_days == 447362
    assert kpis_primary["average_los_days"] == reconciled_alos == 4.40
    assert kpis_primary["median_los_days"] == reconciled_median_los == 4.00
    assert kpis_primary["readmission_rate_30d_pct"] == reconciled_readmission_rate == 11.34
    assert kpis_primary["emergency_admission_rate_pct"] == reconciled_emergency_rate == 53.07
    print("\n[RECONCILIATION AUDIT: 100% PERFECT MATCH ACROSS ALL METRICS]")

