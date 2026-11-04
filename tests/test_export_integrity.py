"""Integration tests for production dataset export integrity."""

from pathlib import Path
import pandas as pd
import openpyxl

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_processed_csv_integrity():
    """Verify hospital_cleaned.csv is present, non-empty, and has expected scale."""
    csv_path = PROJECT_ROOT / "data" / "processed" / "hospital_cleaned.csv"
    assert csv_path.exists(), "hospital_cleaned.csv must exist."
    
    df = pd.read_csv(csv_path, nrows=100)
    assert len(df) == 100
    assert "encounter_id" in df.columns
    assert "department" in df.columns
    assert "is_readmission_eligible" in df.columns
    assert "timeline_type" in df.columns


def test_processed_excel_sheets():
    """Verify hospital_final_dataset.xlsx contains all expected tabs."""
    xlsx_path = PROJECT_ROOT / "data" / "processed" / "hospital_final_dataset.xlsx"
    assert xlsx_path.exists(), "hospital_final_dataset.xlsx must exist."
    
    wb = openpyxl.load_workbook(xlsx_path, read_only=True)
    expected_sheets = {"Inpatient_Encounters", "Department_Analytics", "Synthetic_Capacity_D4", "Data_Dictionary"}
    assert expected_sheets.issubset(set(wb.sheetnames))
    wb.close()


def test_synthetic_capacity_provenance_label():
    """Verify synthetic hospital capacity file contains Section 3 mandatory labeling."""
    cap_path = PROJECT_ROOT / "data" / "processed" / "synthetic_hospital_capacity.csv"
    assert cap_path.exists(), "synthetic_hospital_capacity.csv must exist."
    
    df_cap = pd.read_csv(cap_path)
    assert len(df_cap) > 0
    assert "data_provenance" in df_cap.columns
    # Verify every record carries the mandatory label
    assert (df_cap["data_provenance"] == "Synthetic reference data – not real hospital figures").all()


def test_hyper_extract_exists():
    """Verify native Tableau Hyper extract exists and is non-empty."""
    hyper_path = PROJECT_ROOT / "data" / "processed" / "Aegis_Hospital_Extract.hyper"
    assert hyper_path.exists(), "Aegis_Hospital_Extract.hyper must exist."
    assert hyper_path.stat().st_size > 1_000_000, "Hyper extract must exceed 1MB."


def test_tableau_workbook_integrity():
    """Verify Aegis.dv.twb XML is well-formed and defines all 4 dashboards."""
    import xml.etree.ElementTree as ET

    twb_path = PROJECT_ROOT / "Aegis.dv.twb"
    assert twb_path.exists(), "Aegis.dv.twb must exist at project root."
    tree = ET.parse(twb_path)
    root = tree.getroot()
    assert root.tag == "workbook", "Root tag must be workbook."
    
    dashboards = [d.get("name") for d in root.findall(".//dashboard")]
    expected_dashboards = {
        "1. Hospital Overview",
        "2. Patient Flow",
        "3. Department Analytics",
        "4. Resource Utilization",
    }
    assert expected_dashboards.issubset(set(dashboards)), f"Missing dashboards: {expected_dashboards - set(dashboards)}"


def test_packaged_twbx_integrity():
    """Verify Aegis.dv.twbx is a valid zip archive containing twb and embedded data."""
    import zipfile

    twbx_path = PROJECT_ROOT / "Aegis.dv.twbx"
    assert twbx_path.exists(), "Aegis.dv.twbx must exist at project root."
    assert twbx_path.stat().st_size > 5_000_000, "TWBX must exceed 5MB."

    with zipfile.ZipFile(twbx_path, "r") as z:
        namelist = z.namelist()
        assert "Aegis.dv.twb" in namelist
        assert "Data/Aegis_Hospital/hospital_final_dataset.xlsx" in namelist
        assert "Data/Aegis_Hospital/synthetic_hospital_capacity.csv" in namelist


