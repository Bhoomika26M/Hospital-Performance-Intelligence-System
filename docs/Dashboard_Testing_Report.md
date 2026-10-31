# MedTrack – Dashboard Testing Report and QA Checklist

**Project:** Hospital Performance Intelligence System  
**Milestone:** 4 – Testing and Delivery  
**Module:** 7 – Testing and Validation

---

## 1. Testing Overview

This report documents the testing and validation activities performed on the MedTrack Hospital Performance Intelligence System dashboard.

The application uses Python, Streamlit, Pandas and Plotly. Testing focused on dashboard functionality, navigation, filters, error handling, dataset quality and KPI calculation verification.

## 2. Testing Objectives

- Verify that all dashboard pages load correctly.
- Test global filter functionality.
- Verify navigation between dashboard pages.
- Check dashboard behaviour when filters are empty.
- Validate dataset quality.
- Verify KPI calculations.
- Identify and document data limitations.

## 3. Test Environment

| Component | Details |
|---|---|
| Application | MedTrack |
| Framework | Streamlit |
| Visualization | Plotly |
| Programming Language | Python |
| Data Processing | Pandas |
| Dataset | hospital_dashboard_demo_data.csv |
| Dataset Size | 54,966 rows × 41 columns |

## 4. Test Case Results

| Test ID | Test Description | Actual Result | Status |
|---|---|---|---|
| TC01 | Hospital Overview | All four KPI cards and three charts displayed correctly. | Passed |
| TC02 | Patient Flow | KPI cards and charts displayed correctly. Simulated transfer information was visible. | Passed |
| TC03 | Department Analytics | Simulation warning, three charts and summary table displayed correctly. | Passed |
| TC04 | Resource Utilization | Simulation warning, three KPI cards and five charts displayed correctly. | Passed |
| TC05 | Global Filters | Admission Year, Gender and Medical Condition filters updated dashboard content and could be reset. | Passed |
| TC06 | Navigation | All four pages opened successfully. Sidebar and global filters remained accessible. | Passed |
| TC07 | Dataset Validation | Dataset validation completed successfully. | Passed |
| TC08 | Error Testing | Empty filter selection handled correctly. Page switching worked. No unexpected errors occurred. | Passed |
| TC09 | KPI Verification | Independent calculations matched the dashboard values, as confirmed by the user. | Passed |

## 5. KPI Calculation Verification

The following values were independently calculated using the dashboard dataset with all filters set to All.

| KPI | Verified Value |
|---|---:|
| Total Admissions | 54,966 |
| Average Stay | 15.50 days |
| Total Billing | 1,404,068,339.23 |
| Average Billing | 25,544.31 |

The calculated values were confirmed to match the dashboard values.

*Note: The billing currency has not been confirmed. Values are therefore reported without a currency symbol.*

## 6. Dataset Validation Results

| Validation Check | Result |
|---|---:|
| Total Rows | 54,966 |
| Total Columns | 41 |
| Missing Values | 0 |
| Duplicate Records | 0 |
| Invalid Date Records | 0 |
| Negative Length-of-Stay Records | 0 |

## 7. Known Limitations

1. The original dataset does not contain verified bed availability and occupancy records.
2. Staff and equipment utilization values are simulated.
3. Patient transfer information is simulated because actual transfer records are unavailable.
4. Department assignments are simulated and are not verified hospital department records.
5. Billing currency has not been confirmed.
6. The dataset does not provide sufficient verified longitudinal patient history to calculate a reliable readmission rate.

These limitations should be considered when interpreting dashboard results.

## 8. QA Checklist

- Dashboard launches successfully.
- Hospital Overview page displays correctly.
- Patient Flow page displays correctly.
- Department Analytics page displays correctly.
- Resource Utilization page displays correctly.
- Admission Year filter works.
- Gender filter works.
- Medical Condition filter works.
- Filters can be reset.
- Navigation between all four pages works.
- Global filters remain accessible during navigation.
- Empty filter selection is handled correctly.
- Page switching after filtering works.
- No unexpected dashboard crash was observed.
- Dataset validation completed.
- KPI calculations independently verified.
- Known data limitations documented.

## 9. Conclusion

The MedTrack dashboard successfully completed the reported Module 7 testing activities.

All four dashboard pages displayed their expected content, global filters and navigation worked correctly, and no unexpected errors were observed during the reported tests.

Independent KPI calculations matched the dashboard values. Dataset validation was completed successfully.

Simulated resource utilization, department and transfer metrics have also been documented as limitations.

Overall, the dashboard is considered to have completed the testing and validation activities, subject to the documented dataset limitations.

---

**End of Report**