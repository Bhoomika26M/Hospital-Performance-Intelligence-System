# Aegis.dv – Data Processing Flowchart

```mermaid
flowchart TD
    Start([Start: Ingest Raw Clinical Data]) --> ReadRaw[/Read data/raw/hospital_raw_data.csv/]
    ReadRaw --> Gate1{Schema Valid?<br/>Mandatory Columns & Ranges}
    
    Gate1 -- No --> FailSchema[Halt: SchemaValidationError<br/>Missing columns or invalid domain]
    Gate1 -- Yes --> Dedup[Audit Duplicates on encounter_id]
    
    Dedup --> Gate2{Duplicate Encounters Found?}
    Gate2 -- Yes --> DropDup[Deduplicate keeping first<br/>Log dropped duplicates]
    Gate2 -- No --> KeepAll[Zero duplicates: Keep all records]
    
    DropDup --> MissingAnalysis[Missing Value Token Analysis<br/>Convert '?' to NaN]
    KeepAll --> MissingAnalysis
    
    MissingAnalysis --> TreatMissing[Apply Principled Clinical Categorization:<br/>- Specialty: General Inpatient / Unspecified<br/>- Race: Unknown / Not Reported<br/>- Gender: Not Specified<br/>- Diagnoses: 000.0 Uncoded<br/>- Add indicator flags: is_specialty_unspecified]
    
    TreatMissing --> MapDepts[Map 73 Specialties to 15 Clinical Departments<br/>via data/interim/specialty_mapping.csv]
    
    MapDepts --> Gate3{Unmapped Specialties?}
    Gate3 -- Yes --> DefaultDept[Log Warning & Map to General Inpatient]
    Gate3 -- No --> TimeNorm[Timeline Normalization:<br/>Generate Reference Timeline 1999-2008<br/>Set timeline_type = Reference timeline synthetic]
    DefaultDept --> TimeNorm
    
    TimeNorm --> TypeCast[Strict Data Type Enforcement:<br/>int64 for counts/keys, string for categories]
    
    TypeCast --> OutlierCheck[Tukey IQR Outlier Auditing (k=1.5):<br/>Audit LOS, Labs, Meds, Diagnoses<br/>Flag with is_col_outlier; zero drops]
    
    OutlierCheck --> FeatureGen[Derived Feature Engineering:<br/>- Admission Group: Emergency vs Elective<br/>- Mortality: Expired (dispositions 11,19,20,21)<br/>- CMS Readmission Eligibility: Surviving Cohort<br/>- LOS Stay Cohorts: Short, Medium, Extended<br/>- Clinical Intensity Index: Weighted Score]
    
    FeatureGen --> Gate4{Final Quality Target:<br/>Completeness >= 95%?}
    Gate4 -- No --> ReportWarn[Log Warning in DQ Report]
    Gate4 -- Yes --> ExportStage[Tableau-Ready Export Engine]
    ReportWarn --> ExportStage
    
    ExportStage --> OutCSV[/data/processed/hospital_cleaned.csv/]
    ExportStage --> OutXLSX[/data/processed/hospital_final_dataset.xlsx/]
    ExportStage --> OutHyper[/data/processed/Aegis_Hospital_Extract.hyper/]
    ExportStage --> OutCap[/data/processed/synthetic_hospital_capacity.csv/]
    ExportStage --> OutDQR[/reports/data_quality/data_quality_report.md & json/]
    
    OutDQR --> End([Pipeline Completed Successfully])
```

