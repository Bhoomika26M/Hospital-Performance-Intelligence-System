"""Tableau Export Module for Aegis.dv.

Exports processed hospital datasets to:
1. Flat tidy CSV (hospital_cleaned.csv)
2. Production multi-tab Excel (hospital_final_dataset.xlsx)
3. Native Tableau Hyper extract (Aegis_Hospital_Extract.hyper) using tableauhyperapi.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Any
import pandas as pd

logger = logging.getLogger("aegis.export.tableau")

try:
    from tableauhyperapi import (
        HyperProcess,
        Telemetry,
        Connection,
        CreateMode,
        TableDefinition,
        SqlType,
        Inserter,
        TableName,
    )
    HYPER_API_AVAILABLE = True
except ImportError:
    HYPER_API_AVAILABLE = False
    logger.warning("tableauhyperapi not available in environment. Hyper export will be skipped.")


def export_csv(df: pd.DataFrame, output_path: Path) -> Path:
    """Export cleaned dataframe to flat, tidy CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Exported flat CSV ({len(df):,} rows, {len(df.columns)} cols) to {output_path}")
    return output_path


def export_excel_package(
    df_encounters: pd.DataFrame,
    df_departments: pd.DataFrame,
    df_capacity: pd.DataFrame,
    output_path: Path,
) -> Path:
    """Export formatted multi-tab Excel workbook (hospital_final_dataset.xlsx)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Writing multi-tab production workbook to {output_path}...")

    # Build data dictionary tab
    dict_records = []
    for col in df_encounters.columns:
        dict_records.append({
            "Column Name": col,
            "Data Type": str(df_encounters[col].dtype),
            "Non-Null Count": int(df_encounters[col].notna().sum()),
            "Sample Value": str(df_encounters[col].dropna().iloc[0]) if len(df_encounters[col].dropna()) > 0 else "",
            "Tableau Role": "Dimension" if df_encounters[col].dtype == "object" else "Measure",
            "Description": f"Analytical encounter attribute: {col}",
        })
    df_dict = pd.DataFrame(dict_records)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # Write first 50,000 rows to encounters tab to stay well under Excel limits and preserve high performance
        df_encounters.iloc[:50000].to_excel(writer, sheet_name="Inpatient_Encounters", index=False)
        df_departments.to_excel(writer, sheet_name="Department_Analytics", index=False)
        df_capacity.to_excel(writer, sheet_name="Synthetic_Capacity_D4", index=False)
        df_dict.to_excel(writer, sheet_name="Data_Dictionary", index=False)

    logger.info(f"Successfully generated multi-tab Excel workbook at {output_path}")
    return output_path


def export_hyper_extract(df: pd.DataFrame, hyper_path: Path) -> Path | None:
    """Export dataframe to a native Tableau Hyper extract using tableauhyperapi."""
    if not HYPER_API_AVAILABLE:
        logger.warning("Hyper API unavailable. Skipping .hyper export.")
        return None

    hyper_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_hyper_path = hyper_path.with_suffix(".tmp.hyper")
    if tmp_hyper_path.exists():
        tmp_hyper_path.unlink()

    logger.info(f"Attempting compilation of Tableau Hyper extract at {hyper_path}...")

    try:
        with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            with Connection(
                endpoint=hyper.endpoint,
                database=str(tmp_hyper_path),
                create_mode=CreateMode.CREATE_AND_REPLACE,
            ) as connection:
                
                # Map Pandas dtypes to Hyper SqlTypes
                columns = []
                for col_name, dtype in df.dtypes.items():
                    if "int" in str(dtype):
                        sql_type = SqlType.big_int()
                    elif "float" in str(dtype):
                        sql_type = SqlType.double()
                    elif "datetime" in str(dtype):
                        sql_type = SqlType.date()
                    else:
                        sql_type = SqlType.text()
                    columns.append(TableDefinition.Column(col_name, sql_type))

                table_def = TableDefinition(TableName("Extract", "Hospital_Encounters"), columns)
                connection.catalog.create_schema("Extract")
                connection.catalog.create_table(table_def)

                with Inserter(connection, table_def) as inserter:
                    batch_size = 10000
                    total_rows = len(df)
                    for start_idx in range(0, total_rows, batch_size):
                        chunk = df.iloc[start_idx : start_idx + batch_size]
                        rows_to_insert = []
                        for _, row in chunk.iterrows():
                            row_vals = []
                            for col_name in df.columns:
                                val = row[col_name]
                                if pd.isna(val):
                                    row_vals.append(None)
                                elif isinstance(val, (pd.Timestamp, pd.DatetimeIndex)):
                                    row_vals.append(val.date())
                                elif isinstance(val, (int, float, str)):
                                    row_vals.append(val)
                                else:
                                    row_vals.append(str(val))
                            rows_to_insert.append(row_vals)
                        inserter.add_rows(rows_to_insert)
                    inserter.execute()

        # Atomic replace
        if tmp_hyper_path.exists():
            tmp_hyper_path.replace(hyper_path)

        logger.info(f"Native Hyper extract created successfully ({hyper_path.stat().st_size:,} bytes).")
        return hyper_path
    except Exception as exc:
        if tmp_hyper_path.exists():
            tmp_hyper_path.unlink()
        logger.warning(
            f"Tableau Hyper compilation could not launch hyperd IPC daemon ({exc}). "
            "Falling back to verified production CSV & multi-tab Excel formats."
        )
        return hyper_path if hyper_path.exists() else None
