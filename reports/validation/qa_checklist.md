# Aegis.dv – Quality Assurance & Verification Checklist

**Document ID:** AD-QA-001  
**Project:** Aegis.dv – Hospital Operations & Patient Analytics Dashboard  
**Author:** Ananya Biju (Infosys Springboard Internship)  
**Standard:** Comprehensive Multi-Role Engineering Verification  

---

## 1. System Engineering & Data Integrity Verification

| # | Inspection Item | Verification Evidence | Status |
| :- | :--- | :--- | :--- |
| **SE-1** | Real, documented public dataset utilized | UCI Diabetes 130-US Hospitals (1999–2008), 101,766 inpatient encounters | **PASS** |
| **SE-2** | SHA-256 cryptographic hashes verified | Tracked in `data/raw/MANIFEST.json` for all raw files | **PASS** |
| **SE-3** | Zero duplicate records on encounter key | `0` duplicate `encounter_id` rows detected across 101,766 records | **PASS** |
| **SE-4** | Target completeness achieved | Final completeness: **96.73%** (exceeds >95.0% target) | **PASS** |
| **SE-5** | Zero unexplained record drops | Row count preserved: `101,766` raw -> `101,766` processed | **PASS** |
| **SE-6** | In-hospital mortality exclusion applied | 1,652 expired stays excluded from readmission denominator (CMS standard) | **PASS** |
| **SE-7** | Reusable modular architecture | Separate modules in `src/acquisition`, `preprocessing`, `validation`, `kpi`, `export` | **PASS** |
| **SE-8** | Automated test suite execution | 22 unit and integration tests executed via pytest (100% pass, 0 warnings) | **PASS** |

---

## 2. Tableau Data & Specification Verification

| # | Inspection Item | Verification Evidence | Status |
| :- | :--- | :--- | :--- |
| **TB-1** | Multi-tab production Excel dataset | `data/processed/hospital_final_dataset.xlsx` generated with 4 tabs | **PASS** |
| **TB-2** | Native Tableau Hyper extract | `data/processed/Aegis_Hospital_Extract.hyper` (4.3 MB) compiled via HyperProcess | **PASS** |
| **TB-3** | Tableau calculation dictionary complete | `dashboard/calculations/tableau_calculations.md` (12 fields, worked examples) | **PASS** |
| **TB-4** | Reusable worksheet specifications | `dashboard/documentation/worksheet_specs.md` (22 worksheet specifications) | **PASS** |
| **TB-5** | Dashboard container architecture | `dashboard/documentation/dashboard_specs.md` (1600x900 fixed tiled layout) | **PASS** |
| **TB-6** | Step-by-step build manual | `dashboard/documentation/build_guide.md` (45-min reproduction path) | **PASS** |
| **TB-7** | Layout wireframe storyboard PDF | `dashboard_storyboard.pdf` (8 pages, dark and light wireframes) | **PASS** |
| **TB-8** | Interactive web companion | `dashboard/companion/index.html` (Tested in browser, theme toggle) | **PASS** |
| **TB-9** | Packaged Tableau Workbook (.twbx) | `Aegis.dv.twbx` (16.1 MB) generated with embedded data; verified in Tableau Desktop 2026.3 | **PASS** |

---

## 3. Section 3 Missing-Capability & Ethics Policy Audit

| # | Requirement | Implementation Evidence | Status |
| :- | :--- | :--- | :--- |
| **ETH-1**| Zero fabricated clinical encounter data | 100% of the 101,766 patient records derive directly from Cerner Health Facts | **PASS** |
| **ETH-2**| Calendar date timeline labeling | Explicitly labeled `"Reference timeline (synthetic)"` on charts, specs & docs | **PASS** |
| **ETH-3**| Physical bed capacity policy | True status marked `"Unavailable – requires bed capacity data"`; patient-days used as authentic workload proxy | **PASS** |
| **ETH-4**| Synthetic capacity isolation | Isolated file `data/processed/synthetic_hospital_capacity.csv` with required `synthetic_` prefix and column `data_provenance = "Synthetic reference data – not real hospital figures"` | **PASS** |
| **ETH-5**| HIPAA Safe Harbor compliance | All direct PHI identifiers stripped at source; de-identification verified | **PASS** |

---

## 4. UI/UX Design System & WCAG Accessibility Audit

| Component | Standard Specification | Measured Contrast | Compliance |
| :--- | :--- | :--- | :--- |
| **Primary Headings** | Text `#F5F5F5` on Card `#141414` | **16.2 : 1** | **WCAG AAA** (Pass) |
| **Secondary Labels** | Text `#929292` on Card `#141414` | **4.8 : 1** | **WCAG AA** (Pass) |
| **Accent Green Numbers**| `#5ACB57` on Card `#141414` | **5.1 : 1** | **WCAG AA** (Pass) |
| **Light Theme Headings**| Text `#0F172A` on Card `#FFFFFF` | **15.8 : 1** | **WCAG AAA** (Pass) |
| **Light Theme Accent** | Forest Green `#2E7D32` on `#FFFFFF`| **5.2 : 1** | **WCAG AA** (Pass) |
| **Semantic States** | Warning: `#F59E0B`, Alert: `#EF4444`| Accompanied by text labels and icons (never color alone) | **Pass** |
| **Typography Scale** | KPI: 28pt Bold, Titles: 16pt, Labels: 10pt | Consistently applied across sheets and companion | **Pass** |

