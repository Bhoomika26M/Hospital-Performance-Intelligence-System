"""Feature Engineering Module for Aegis.dv.

Derives clinical, operational, and demographic attributes for dashboard visuals,
including admission source groupings, disposition categories, readmission eligibility,
LOS stay cohorts, ICD-9 diagnostic chapters, and workload intensity proxies.
"""

from __future__ import annotations

import logging
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd

from src.preprocessing.data_loader import load_id_mappings

logger = logging.getLogger("aegis.features.builder")


def categorize_icd9(code: str) -> str:
    """Group ICD-9 code into high-level diagnostic chapters."""
    if not isinstance(code, str) or code in ["?", "000.0", ""]:
        return "Other Conditions"
    
    # Handle V and E supplementary codes
    if code.startswith("V") or code.startswith("E"):
        return "Supplementary & External Factors"
        
    try:
        val = float(code)
    except ValueError:
        return "Other Conditions"

    if 390 <= val <= 459 or val == 785:
        return "Circulatory System"
    elif 460 <= val <= 519 or val == 786:
        return "Respiratory System"
    elif 520 <= val <= 579 or val == 787:
        return "Digestive System"
    elif int(val) == 250:
        return "Diabetes & Endocrine"
    elif 800 <= val <= 999:
        return "Injury & Poisoning"
    elif 710 <= val <= 739:
        return "Musculoskeletal & Connective"
    elif 580 <= val <= 629 or val == 788:
        return "Genitourinary System"
    elif 140 <= val <= 239:
        return "Neoplasms (Oncology)"
    elif 240 <= val <= 279:
        return "Endocrine, Nutritional & Metabolic"
    elif 290 <= val <= 319:
        return "Mental Disorders"
    elif 680 <= val <= 709:
        return "Skin & Subcutaneous Tissue"
    else:
        return "Other Conditions"


def build_derived_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Generate all analytical and visual attributes required by Aegis.dv dashboards.

    Args:
        df: Cleaned dataframe.

    Returns:
        Tuple of (feature_rich_dataframe, feature_generation_report).
    """
    logger.info("Engineering derived clinical and operational attributes...")
    df_out = df.copy()

    # 1. Load official mapping dictionaries
    adm_type_map, disch_disp_map, adm_source_map = load_id_mappings()

    # 2. Map textual descriptions
    df_out["admission_type_desc"] = df_out["admission_type_id"].map(adm_type_map).fillna("Unknown/Other")
    df_out["discharge_disposition_desc"] = (
        df_out["discharge_disposition_id"].map(disch_disp_map).fillna("Unknown/Other")
    )
    df_out["admission_source_desc"] = df_out["admission_source_id"].map(adm_source_map).fillna("Unknown/Other")

    # 3. High-Level Admission Type Grouping
    def _group_admission_type(type_id: int) -> str:
        if type_id in [1, 7]:
            return "Emergency"
        elif type_id == 2:
            return "Urgent"
        elif type_id == 3:
            return "Elective"
        elif type_id == 4:
            return "Newborn"
        else:
            return "Other / Unknown"

    df_out["admission_type_group"] = df_out["admission_type_id"].apply(_group_admission_type)
    df_out["is_emergency_admission"] = (df_out["admission_type_group"] == "Emergency").astype(int)

    # 4. High-Level Discharge Disposition Grouping & Mortality Exclusion
    def _group_discharge_disposition(disp_id: int) -> str:
        if disp_id in [11, 19, 20, 21]:
            return "Expired (In-Hospital Mortality)"
        elif disp_id in [1, 6, 8]:
            return "Routine Discharge Home"
        elif disp_id in [2, 3, 4, 5, 22, 23, 24, 30]:
            return "Transferred to Care Facility"
        elif disp_id in [13, 14]:
            return "Hospice Care"
        elif disp_id == 7:
            return "Left Against Medical Advice (AMA)"
        else:
            return "Other / Uncategorized"

    df_out["discharge_disposition_group"] = df_out["discharge_disposition_id"].apply(_group_discharge_disposition)
    df_out["is_in_hospital_death"] = (
        df_out["discharge_disposition_group"] == "Expired (In-Hospital Mortality)"
    ).astype(int)

    # 5. Readmission Eligibility & Flags (CMS / NQF Compliant)
    # Patients who died during index admission are NOT eligible for readmission!
    df_out["is_readmission_eligible"] = (df_out["is_in_hospital_death"] == 0).astype(int)
    df_out["readmitted_30d_flag"] = (df_out["readmitted"] == "<30").astype(int)
    df_out["readmitted_any_flag"] = (df_out["readmitted"].isin(["<30", ">30"])).astype(int)

    # 6. High-Level Admission Source Grouping
    def _group_admission_source(src_id: int) -> str:
        if src_id == 7:
            return "Emergency Room"
        elif src_id in [1, 2, 3]:
            return "Physician / Clinic Referral"
        elif src_id in [4, 5, 6, 10, 18, 22, 25, 26]:
            return "Inter-Facility Transfer"
        elif src_id == 8:
            return "Court / Law Enforcement"
        else:
            return "Other / Not Available"

    df_out["admission_source_group"] = df_out["admission_source_id"].apply(_group_admission_source)

    # 7. Length of Stay (LOS) Stay Duration Cohorts
    def _categorize_los(days: int) -> str:
        if days <= 2:
            return "1–2 Days (Short Stay)"
        elif days <= 5:
            return "3–5 Days (Medium Stay)"
        elif days <= 9:
            return "6–9 Days (Extended Stay)"
        else:
            return "10–14 Days (Prolonged Acute Stay)"

    df_out["los_band"] = df_out["time_in_hospital"].apply(_categorize_los)

    # 8. Standardized Age Brackets
    def _simplify_age(age_str: str) -> str:
        if age_str in ["[0-10)", "[10-20)"]:
            return "0–19"
        elif age_str in ["[20-30)", "[30-40)"]:
            return "20–39"
        elif age_str in ["[40-50)", "[50-60)"]:
            return "40–59"
        elif age_str in ["[60-70)", "[70-80)"]:
            return "60–79"
        else:
            return "80+"

    df_out["age_bracket"] = df_out["age"].apply(_simplify_age)

    # 9. Primary Diagnosis Chapter
    df_out["primary_diagnosis_category"] = df_out["diag_1"].apply(categorize_icd9)

    # 10. Operational Workload Proxies
    # Real dataset lacks bed counts; total patient-days serves as authentic clinical workload proxy
    df_out["patient_days"] = df_out["time_in_hospital"].astype(int)

    # Clinical Intensity Index (Weighted composite of clinical actions)
    # Formula: 0.15*num_lab + 1.2*num_procedures + 0.4*num_medications + 0.6*number_diagnoses
    df_out["clinical_intensity_index"] = np.round(
        (df_out["num_lab_procedures"] * 0.15)
        + (df_out["num_procedures"] * 1.20)
        + (df_out["num_medications"] * 0.40)
        + (df_out["number_diagnoses"] * 0.60),
        2,
    )

    report: Dict[str, Any] = {
        "features_engineered": [
            "admission_type_desc",
            "admission_type_group",
            "is_emergency_admission",
            "discharge_disposition_desc",
            "discharge_disposition_group",
            "is_in_hospital_death",
            "is_readmission_eligible",
            "readmitted_30d_flag",
            "readmitted_any_flag",
            "admission_source_desc",
            "admission_source_group",
            "los_band",
            "age_bracket",
            "primary_diagnosis_category",
            "patient_days",
            "clinical_intensity_index",
        ],
        "total_readmission_eligible": int(df_out["is_readmission_eligible"].sum()),
        "total_in_hospital_deaths": int(df_out["is_in_hospital_death"].sum()),
        "total_30d_readmissions": int(df_out["readmitted_30d_flag"].sum()),
    }

    logger.info(
        f"Feature engineering complete. Readmission eligible cohort: "
        f"{report['total_readmission_eligible']:,} (Excluded {report['total_in_hospital_deaths']:,} in-hospital deaths)."
    )
    return df_out, report

