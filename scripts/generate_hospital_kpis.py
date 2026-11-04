#!/usr/bin/env python3
"""CLI wrapper for generating hospital KPIs."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.kpi.generate_hospital_kpis import run_kpi_generation

if __name__ == "__main__":
    run_kpi_generation()

