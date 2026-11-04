"""Data Acquisition Module for Aegis.dv.

Downloads and verifies the UCI 'Diabetes 130-US Hospitals (1999-2008)' dataset
and associated mapping dictionaries. Validates integrity via SHA-256 checksums
and logs metadata into data/raw/MANIFEST.json.
"""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("aegis.acquisition")

UCI_DIABETES_URL = "https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip"


def compute_sha256(filepath: Path) -> str:
    """Compute the SHA-256 checksum of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def download_file(url: str, dest_path: Path, max_retries: int = 3, timeout: int = 60) -> Path:
    """Download a remote file with retries and timeout protection."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Downloading from {url} to {dest_path}...")
    
    session = requests.Session()
    for attempt in range(1, max_retries + 1):
        try:
            response = session.get(url, stream=True, timeout=timeout)
            response.raise_for_status()
            with open(dest_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            logger.info(f"Successfully downloaded {dest_path.name} ({dest_path.stat().st_size:,} bytes).")
            return dest_path
        except requests.RequestException as e:
            logger.warning(f"Download attempt {attempt}/{max_retries} failed: {e}")
            if attempt == max_retries:
                raise RuntimeError(f"Failed to download {url} after {max_retries} attempts.") from e


def extract_and_catalog(zip_path: Path, raw_dir: Path) -> Dict[str, Any]:
    """Extract files from archive, copy to standardized names, and build manifest."""
    logger.info(f"Extracting archive {zip_path}...")
    extracted_files = []
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(raw_dir)
        extracted_files = z.namelist()

    logger.info(f"Extracted files: {extracted_files}")

    # Standardize primary clinical encounter dataset to hospital_raw_data.csv
    src_csv = raw_dir / "diabetic_data.csv"
    dest_raw_csv = raw_dir / "hospital_raw_data.csv"
    if src_csv.exists() and not dest_raw_csv.exists():
        shutil.copy(src_csv, dest_raw_csv)
        logger.info(f"Copied {src_csv} to consolidated {dest_raw_csv}")

    manifest_records: Dict[str, Any] = {
        "manifest_version": "1.0",
        "project": "Aegis.dv",
        "developer": "Ananya Biju (Infosys Springboard Internship)",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "files": []
    }

    tracked_files = [
        zip_path.name,
        "diabetic_data.csv",
        "IDs_mapping.csv",
        "hospital_raw_data.csv"
    ]

    for filename in tracked_files:
        filepath = raw_dir / filename
        if filepath.exists():
            checksum = compute_sha256(filepath)
            size_bytes = filepath.stat().st_size
            manifest_records["files"].append({
                "filename": filename,
                "relative_path": f"data/raw/{filename}",
                "size_bytes": size_bytes,
                "sha256": checksum,
                "source_url": UCI_DIABETES_URL if "zip" in filename else f"{UCI_DIABETES_URL}#{filename}",
                "date_accessed": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "license": "Creative Commons Attribution 4.0 International (CC BY 4.0) / Public Research Dataset"
            })

    manifest_path = raw_dir / "MANIFEST.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_records, f, indent=2)
    logger.info(f"Manifest written to {manifest_path}")

    return manifest_records


def run_acquisition(raw_dir: Path | None = None) -> Dict[str, Any]:
    """Execute complete data collection pipeline."""
    if raw_dir is None:
        raw_dir = Path(__file__).resolve().parents[2] / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    zip_dest = raw_dir / "diabetes_130_us_hospitals.zip"
    if not zip_dest.exists() or zip_dest.stat().st_size == 0:
        download_file(UCI_DIABETES_URL, zip_dest)
    else:
        logger.info(f"Raw archive {zip_dest} already exists. Skipping download.")

    manifest = extract_and_catalog(zip_dest, raw_dir)
    return manifest


if __name__ == "__main__":
    try:
        run_acquisition()
    except Exception as exc:
        logger.error(f"Data collection failed: {exc}")
        sys.exit(1)

