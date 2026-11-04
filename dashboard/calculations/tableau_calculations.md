# Aegis.dv – Tableau Calculated Fields, Parameters & LOD Expressions Repository

**Document ID:** AD-CALC-001  
**Project:** Aegis.dv – Hospital Operations & Patient Analytics Dashboard  
**Author:** Ananya Biju (Infosys Springboard Internship)  
**Standard:** Exact mathematical parity with `src/kpi/kpi_engine.py`  

---

## 1. Parameters Configuration

Configure these parameters in Tableau Desktop before creating worksheets:

### P1. Minimum Sample Size (`[p_Min_Sample_Size]`)
* **Data Type:** Integer
* **Current Value:** `30`
* **Allowable Values:** Range (Min: `10`, Max: `100`, Step: `5`)
* **Usage:** Applied in Department Analytics to flag or suppress low-volume specialties (Fair Comparison Rule).

### P2. Benchmark Occupancy Threshold (`[p_Occupancy_Threshold_Pct]`)
* **Data Type:** Float
* **Current Value:** `85.0` (Configurable operational threshold)
* **Display Format:** Percentage (`85.0%`)
* **Allowable Values:** Range (Min: `70.0`, Max: `95.0`, Step: `1.0`)
* **Usage:** Capacity warning boundary on Dashboard 4 (Resource Utilization).

### P3. Reporting Period Selector (`[p_Reporting_Period]`)
* **Data Type:** String
* **Allowable Values:** List (`All Available (1999–2008)`, `Last 3 Years`, `Last 12 Months`)
* **Current Value:** `All Available (1999–2008)`

### P4. Theme Variant Mode (`[p_Theme_Mode]`)
* **Data Type:** String
* **Allowable Values:** List (`Dark Mode (Default)`, `Light Mode`)
* **Current Value:** `Dark Mode (Default)`

---

## 2. Calculated Fields & LOD Expressions

Every calculated field below is copy-paste ready for Tableau Desktop.

```
+----+----------------------------------+-----------------------------+-----------------------+--------------------+
| ID | Field Name                       | Tableau Calculation Syntax  | Python Source Function| Expected Output    |
+----+----------------------------------+-----------------------------+-----------------------+--------------------+
| C1 | [Total Admissions]               | COUNTD([encounter_id])      | calculate_total_      | 101,766            |
|    |                                  |                             | admissions()          |                    |
+----+----------------------------------+-----------------------------+-----------------------+--------------------+
| C2 | [Total Discharges]               | COUNTD([encounter_id])      | calculate_total_      | 101,766            |
|    |                                  |                             | discharges()          |                    |
+----+----------------------------------+-----------------------------+-----------------------+--------------------+
| C3 | [Average Length of Stay]         | AVG([time_in_hospital])     | calculate_average_    | 4.40 days          |
|    |                                  |                             | length_of_stay()      |                    |
+----+----------------------------------+-----------------------------+-----------------------+--------------------+
| C4 | [Median Length of Stay]          | MEDIAN([time_in_hospital])  | calculate_median_     | 4.00 days          |
|    |                                  |                             | length_of_stay()      |                    |
+----+----------------------------------+-----------------------------+-----------------------+--------------------+
| C5 | [Total Patient-Days]             | SUM([time_in_hospital])     | calculate_total_      | 447,362 days       |
|    |                                  |                             | patient_days()        |                    |
+----+----------------------------------+-----------------------------+-----------------------+--------------------+
| C6 | [Readmission Rate 30d (CMS)]     | (SUM([readmitted_30d_flag]) | calculate_readmission_| 11.34%             |
|    |                                  | / SUM([is_readmission_      | rate_30d()            |                    |
|    |                                  | eligible])) * 100           |                       |                    |
+----+----------------------------------+-----------------------------+-----------------------+--------------------+
| C7 | [Emergency Admission Rate]       | (SUM([is_emergency_         | calculate_emergency_  | 53.07%             |
|    |                                  | admission]) / COUNTD(       | admission_rate()      |                    |
|    |                                  | [encounter_id])) * 100      |                       |                    |
+----+----------------------------------+-----------------------------+-----------------------+--------------------+
| C8 | [Clinical Intensity Index]       | (0.15 * [num_lab_procedures]| build_derived_        | Mean: 21.28        |
|    |                                  | ) + (1.20 * [num_procedures]| features()            |                    |
|    |                                  | ) + (0.40 * [num_           |                       |                    |
|    |                                  | medications]) + (0.60 *     |                       |                    |
|    |                                  | [number_diagnoses])         |                       |                    |
+----+----------------------------------+-----------------------------+-----------------------+--------------------+
| C9 | [Department Sample Flag]         | IF COUNTD([encounter_id])   | calculate_department_ | 'Robust' /         |
|    |                                  | >= [p_Min_Sample_Size] THEN | summary()             | 'Low Sample'       |
|    |                                  | "Robust Sample" ELSE        |                       |                    |
|    |                                  | "Low Sample (<" + STR(      |                       |                    |
|    |                                  | [p_Min_Sample_Size]) + ")"  |                       |                    |
|    |                                  | END                         |                       |                    |
+----+----------------------------------+-----------------------------+-----------------------+--------------------+
| C10| [Department Volume Share]        | COUNTD([encounter_id]) /    | calculate_department_ | % of total         |
|    |                                  | TOTAL(COUNTD([encounter_id])| summary()             | encounters         |
|    |                                  | ) * 100                     |                       |                    |
+----+----------------------------------+-----------------------------+-----------------------+--------------------+
| C11| [LOD Encounters per Patient]     | { FIXED [patient_nbr] :     | deduplicate_          | 1.423 encounters / |
|    |                                  | COUNTD([encounter_id]) }    | encounters()          | patient            |
+----+----------------------------------+-----------------------------+-----------------------+--------------------+
| C12| [LOD Dept Readmission Rate]      | { FIXED [department] :      | calculate_department_ | Fixed Dept %       |
|    |                                  | (SUM([readmitted_30d_flag]) | summary()             |                    |
|    |                                  | / SUM([is_readmission_      |                       |                    |
|    |                                  | eligible])) * 100 }         |                       |                    |
+----+----------------------------------+-----------------------------+-----------------------+--------------------+
```

---

## 3. Detailed Worked Examples & Mathematical Validation

### Example 1: CMS 30-Day Readmission Rate (`[Readmission Rate 30d (CMS)]`)
* **Tableau Syntax:**
  ```tableau
  IIF(SUM([is_readmission_eligible]) > 0,
      (SUM([readmitted_30d_flag]) / SUM([is_readmission_eligible])) * 100,
      NULL)
  ```
* **Python Mapping:** `src.kpi.kpi_engine.calculate_readmission_rate_30d(df)`
* **Input Values (Full Dataset):**
  - Numerator: $\sum \text{readmitted\_30d\_flag} = 11,357$
  - Total Encounters: $101,766$
  - In-Hospital Mortality Excluded: $1,652$
  - Denominator: $\sum \text{is\_readmission\_eligible} = 101,766 - 1,652 = 100,114$
* **Calculation:**  
  $$\frac{11,357}{100,114} \times 100 = 11.34407\% \to \mathbf{11.34\%}$$
* **Display Format in Tableau:** `Percentage, 2 decimal places (11.34%)`. Tableau renders `NULL` as `"–"`.

---

### Example 2: Average Length of Stay (`[Average Length of Stay]`)
* **Tableau Syntax:**
  ```tableau
  IIF(COUNTD([encounter_id]) > 0,
      SUM([time_in_hospital]) / COUNTD([encounter_id]),
      NULL)
  ```
* **Python Mapping:** `src.kpi.kpi_engine.calculate_average_length_of_stay(df)`
* **Input Values (Full Dataset):**
  - $\sum \text{time\_in\_hospital} = 447,362$ patient-days
  - $\text{COUNTD}(\text{encounter\_id}) = 101,766$
* **Calculation:**  
  $$\frac{447,362}{101,766} = 4.395987 \to \mathbf{4.40\text{ days}}$$
* **Display Format in Tableau:** `Number (Custom), 2 decimal places, Suffix: " days"`.

---

### Example 3: Emergency Admission Rate (`[Emergency Admission Rate]`)
* **Tableau Syntax:**
  ```tableau
  IIF(COUNTD([encounter_id]) > 0,
      (SUM([is_emergency_admission]) / COUNTD([encounter_id])) * 100,
      NULL)
  ```
* **Python Mapping:** `src.kpi.kpi_engine.calculate_emergency_admission_rate(df)`
* **Input Values:**
  - Emergency Encounters (Admission Type 1 + 7): $53,990 + 21 = 54,011$
  - Total Encounters: $101,766$
* **Calculation:**  
  $$\frac{54,011}{101,766} \times 100 = 53.0737\% \to \mathbf{53.07\%}$$
* **Display Format in Tableau:** `Percentage, 1 decimal place (53.1%)`.

---

### Example 4: Fixed LOD Department Readmission (`[LOD Dept Readmission Rate]`)
* **Tableau Syntax:**
  ```tableau
  { FIXED [department] : 
      (SUM([readmitted_30d_flag]) / NULLIF(SUM([is_readmission_eligible]), 0)) * 100 
  }
  ```
* **Purpose:** Preserves department-level baseline readmission rate regardless of user date-range filtering for benchmark comparison in Dashboard 3.

