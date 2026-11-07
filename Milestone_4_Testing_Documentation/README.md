# MedTrack_DV – Testing and Documentation

## 1. Project Overview

MedTrack_DV is a Hospital Operations and Patient Analytics Dashboard project developed to analyze hospital admissions, patient flow, clinical trends and resource utilization.

## 2. Testing and Validation

The following checks are included in the project testing process:

- Verified the hospital dataset was loaded successfully.
- Checked and removed duplicate records.
- Validated admission and discharge date fields.
- Calculated patient length of stay.
- Checked the cleaned dataset for remaining duplicate records.
- Reviewed KPI calculations.
- Tested dashboard filters and interactions.

## 3. Dataset Validation

| Validation                | Result |
| ------------------------- | ------ |
| Original records          | 55,500 |
| Duplicate records removed | 534    |
| Final cleaned records     | 54,966 |
| Remaining duplicate rows  | 0      |
| Cleaned dataset columns   | 16     |

## 4. KPI Validation

The following KPIs are supported by the available dataset:

- Total Admissions
- Average Length of Stay
- Total Hospitals
- Total Billing

The following KPIs require additional operational data:

- Occupancy Rate
- Readmission Rate
- Bed Utilization Rate
- Department Efficiency Score
- Staff Utilization

These unsupported KPIs should not be presented as measured results without the required data.

## 5. Dashboard Testing Checklist

The project contains four dashboard sections:

1. Hospital Overview
2. Patient Flow
3. Clinical Analytics
4. Resource Utilization

Testing checklist:

- [ ] Dashboard titles are displayed correctly.
- [ ] Charts and visualizations load correctly.
- [ ] Filters work correctly.
- [ ] Dashboard navigation works.
- [ ] Chart interactions work.
- [ ] Data values are displayed correctly.
- [ ] Tableau Public workbook is accessible.

## 6. Data Limitations

The available dataset does not contain:

- Department information
- Unique patient identifiers
- Bed capacity information
- Staff allocation information
- Equipment inventory and usage information

Additional trusted operational datasets are required to calculate these metrics accurately.

## 7. Tools and Technologies

- Python
- Pandas
- Microsoft Excel
- Tableau Public
- CSV datasets

## 8. Final Deliverables

- Raw hospital dataset
- Cleaned hospital dataset
- KPI engineering workbook
- Tableau Public dashboard workbook
- Testing and validation documentation

## 9. Conclusion

The MedTrack_DV project transforms hospital admission data into interactive visual insights. The dashboard suite supports analysis of hospital performance, patient flow, clinical trends and resource utilization, while documenting the limitations of the available operational data.
