# Project Limitations and Data Notes

## Data sources
I treated the Patient Admissions dataset and PMC Hospital Infrastructure dataset as separate sources. I did not perform a join because I did not establish a verified common hospital key.

## Patient admissions
- I calculate **Total Admissions** by counting admission-date records. This is not a distinct-patient count because a patient identifier was not available.
- I cannot reliably calculate readmission rate without a patient identifier and suitable longitudinal linkage.
- I use **Medical Condition** as a condition category, not as a hospital department.
- I aggregate billing amounts as provided. The currency was not confirmed, so I do not assume a currency symbol or currency-specific interpretation.
- The admissions data covers May 2019 through May 2024. The final month may be partial depending on the source extract.

## Hospital infrastructure
- I interpret **Total Hospital Beds** as reported bed capacity, not occupied beds or currently available beds.
- I do not interpret **Average Monthly Patient Footfall** as bed occupancy or utilization.
- I treat the PMC infrastructure dataset as a snapshot, not a time series.
- I cannot measure equipment utilization because equipment-level fields were unavailable.

## Interpretation
- I do not combine the two datasets at hospital level without a verified matching key and documented method.
- I interpret dashboard KPIs alongside my KPI Dictionary.
- My dashboard results describe the supplied datasets and do not establish causal relationships.

## Privacy and publication
The datasets were provided for this project, but receiving vendor-provided data does not by itself establish permission for public distribution. I will confirm the vendor terms and obtain supervisor or data-owner authorization before publishing patient-level data or a Tableau packaged workbook that may contain embedded extracts.
