"""Data Loader Module for Aegis.dv.

Loads raw clinical encounters and code ID mapping tables from data/raw/.
"""

from __future__ import annotations

import io
import logging
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd

logger = logging.getLogger("aegis.preprocessing.loader")


def load_raw_data(raw_dir: Path | None = None) -> pd.DataFrame:
    """Load raw hospital encounter data from CSV.

    Args:
        raw_dir: Optional path to data/raw directory.

    Returns:
        pd.DataFrame containing raw encounter records.
    """
    if raw_dir is None:
        raw_dir = Path(__file__).resolve().parents[2] / "data" / "raw"
    csv_path = raw_dir / "hospital_raw_data.csv"
    if not csv_path.exists():
        csv_path = raw_dir / "diabetic_data.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Raw encounter data not found in {raw_dir}")

    logger.info(f"Loading raw encounters from {csv_path}...")
    df = pd.read_csv(csv_path, low_memory=False)
    logger.info(f"Loaded {len(df):,} records with {len(df.columns)} columns.")
    return df


def load_id_mappings(raw_dir: Path | None = None) -> Tuple[Dict[int, str], Dict[int, str], Dict[int, str]]:
    """Parse IDs_mapping.csv into admission type, discharge disposition, and admission source dicts.

    Args:
        raw_dir: Optional path to data/raw directory.

    Returns:
        Tuple of (admission_type_map, discharge_disposition_map, admission_source_map).
    """
    if raw_dir is None:
        raw_dir = Path(__file__).resolve().parents[2] / "data" / "raw"
    mapping_path = raw_dir / "IDs_mapping.csv"
    if not mapping_path.exists():
        raise FileNotFoundError(f"Mapping file not found at {mapping_path}")

    with open(mapping_path, "r", encoding="utf-8") as f:
        text = f.read()

    # IDs_mapping has three sections separated by "\n,\n"
    sections = text.split("\n,\n")
    if len(sections) < 3:
        # Fallback split
        sections = text.split(",\n")

    def _parse_section(section_str: str) -> Dict[int, str]:
        lines = [line.strip() for line in section_str.strip().split("\n") if line.strip()]
        if not lines:
            return {}
        csv_data = "\n".join(lines)
        df_sec = pd.read_csv(io.StringIO(csv_data))
        id_col = df_sec.columns[0]
        desc_col = df_sec.columns[1]
        res = {}
        for _, row in df_sec.iterrows():
            try:
                k = int(row[id_col])
                v = str(row[desc_col]).strip()
                res[k] = v
            except (ValueError, TypeError):
                continue
        return res

    admission_type_map = _parse_section(sections[0])
    discharge_disposition_map = _parse_section(sections[1])
    admission_source_map = _parse_section(sections[2])

    logger.info(
        f"Parsed ID mappings: {len(admission_type_map)} admission types, "
        f"{len(discharge_disposition_map)} discharge dispositions, "
        f"{len(admission_source_map)} admission sources."
    )
    return admission_type_map, discharge_disposition_map, admission_source_map

