# Aegis.dv – User Interaction & Analytical Journey Flowchart

```mermaid
flowchart TD
    User([Hospital Executive / Administrator Launches Aegis.dv]) --> LandD1[Lands on Dashboard 1: Hospital Overview]
    
    LandD1 --> ReviewKPIs[Review Executive Scorecard:<br/>101,766 Admissions | 4.40d ALOS | 11.34% Readmit | 447k Patient-Days]
    
    ReviewKPIs --> CheckThroughput{Admissions vs Discharges<br/>Equilibrium Balanced?}
    CheckThroughput -- Yes --> DrillDept[Click Clinical Department Bar<br/>e.g., General Surgery or Emergency]
    CheckThroughput -- No --> AlertThroughput[Flag Potential Bed Board Congestion]
    
    DrillDept --> CrossFilter[Cross-Filter Action Filters Readmission Donut & Demographics]
    
    CrossFilter --> JumpD2[Click 'Patient Flow' on Left Navigation Rail]
    
    JumpD2 --> AnalyzeFlow[Examine Care Pathway Transition Funnel:<br/>Emergency Room 53.1% -> Specialty Treatment -> Discharge Destination]
    AnalyzeFlow --> InspectLOS[Inspect LOS Distribution Histogram:<br/>Right-skewed acute stay profile, Median 4.0d vs Mean 4.4d]
    InspectLOS --> InspectHeatmap[Audit Day-of-Week x Month Heatmap for Surge Bottlenecks]
    
    InspectHeatmap --> JumpD3[Click 'Department Analytics' on Left Navigation Rail]
    
    JumpD3 --> BenchmarkDepts[Inspect 4-Quadrant Strategic Portfolio:<br/>Patient Volume vs CMS Readmission Rate]
    BenchmarkDepts --> AdjustSample[Adjust Min Sample Size Parameter p_Min_Sample_Size<br/>Suppress noisy low-n specialties]
    AdjustSample --> AuditAcuity[Examine Weighted Clinical Intensity Index & Workload Days]
    
    AuditAcuity --> JumpD4[Click 'Resource Utilization' on Left Navigation Rail]
    
    JumpD4 --> ReadNotice[Read Section 3 Synthetic Reference Banner]
    ReadNotice --> AuditOccupancy[Inspect Daily Bed Occupancy Line vs 75-90% Operating Band]
    AuditOccupancy --> CheckStaffing[Review Nurse-to-Patient Staffing Ratio vs Patient Census]
    
    CheckStaffing --> Decision([Actionable Operational Decisions:<br/>Staffing Reallocation, Capacity Planning, Discharge Optimization])
```

