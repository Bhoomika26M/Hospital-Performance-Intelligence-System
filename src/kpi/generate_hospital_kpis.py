"""Script entry point for computing and displaying hospital operational KPIs."""

from __future__ import annotations

import json
import logging
from pathlib import Path
import pandas as pd

from src.kpi.kpi_engine import compute_headline_kpis, calculate_department_summary

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("aegis.kpi.generator")


def run_kpi_generation(processed_dir: Path | None = None) -> dict:
    """Generate and display headline KPIs from processed hospital dataset."""
    if processed_dir is None:
        processed_dir = Path(__file__).resolve().parents[2] / "data" / "processed"
    
    csv_path = processed_dir / "hospital_cleaned.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Cleaned dataset not found at {csv_path}. Run pipeline first.")

    logger.info(f"Loading cleaned dataset from {csv_path}...")
    df = pd.read_csv(csv_path, low_memory=False)

    headline = compute_headline_kpis(df)
    dept_summary = calculate_department_summary(df)

    logger.info("=== AEGIS.DV HOSPITAL OPERATIONAL HEADLINE SCORECARD ===")
    for k, v in headline.items():
        logger.info(f"  {k:30s}: {v}")

    # Save summary json
    summary_path = processed_dir / "hospital_kpi_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(headline, f, indent=2)
    logger.info(f"KPI summary written to {summary_path}")

    dept_csv_path = processed_dir / "department_kpi_summary.csv"
    dept_summary.to_csv(dept_csv_path, index=False)
    logger.info(f"Department summary ({len(dept_summary)} depts) written to {dept_csv_path}")

    return headline


if __name__ == "__main__":
    run_kpi_generation()

