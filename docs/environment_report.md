# Aegis.dv – Environment & Tooling Audit Report

**Generated:** November 4, 2026  
**Auditor:** Aegis.dv Engineering Team  
**Project:** Aegis.dv – Hospital Operations & Patient Analytics Dashboard  
**Developer Attribution:** Ananya Biju (Infosys Springboard Internship)  

---

## 1. Operating System & Hardware Architecture

| Parameter | Detection Result | Notes |
| :--- | :--- | :--- |
| **Operating System** | macOS (Darwin Kernel 24+) | Apple Silicon ARM64 architecture |
| **Shell** | `/bin/zsh` | Standard interactive zsh environment |
| **Home Directory** | `/Users/ananyabiju` | Active development user workspace |
| **Workspace Root** | `/Users/ananyabiju/Desktop/Aegis` | Local repository root directory |

---

## 2. Python Runtime & Virtual Environment

| Component | Status / Version | Path |
| :--- | :--- | :--- |
| **System Python** | Python 3.9.6 | `/usr/bin/python3` (macOS Developer Tools default) |
| **Homebrew Python** | Python 3.11.15 | `/opt/homebrew/bin/python3.11` (Selected for pipeline) |
| **Project Virtualenv** | Active (`.venv`) | `/Users/ananyabiju/Desktop/Aegis/.venv` |
| **Package Installer** | `pip 26.3` | Installed in `.venv` |
| **Core Libraries** | `pandas 3.1.0`, `numpy 2.4.6`, `openpyxl 3.1.5` | Installed and verified in `.venv` |
| **Testing Harness** | `pytest 9.2.0` | Installed in `.venv` |
| **Reporting / PDF** | `reportlab 5.1.0`, `pillow 13.0.0` | Installed in `.venv` for wireframe generation |

---

## 3. Network & Remote Repository Access

* **Sandbox Security Mode:** Standard execution runs inside a secure sandbox container with local file isolation. Network operations (package installation, real dataset acquisition) require elevation via bypass sandbox execution.
* **Internet Connectivity:** Verified working. Direct downloads from UCI Machine Learning Repository (`archive.ics.uci.edu`) and PyPI package indices are accessible.
* **Public Dataset Access:** Direct HTTP/HTTPS downloads confirmed functional for UCI dataset endpoints.

---

## 4. Tableau Capability Detection

| Tool / Technology | Status | Verification Detail |
| :--- | :--- | :--- |
| **Tableau Desktop (GUI)** | **Installed & Verified** | `/Applications/Tableau Desktop (Apple silicon) 2026.3.app` detected, active, and validated by successfully launching `Aegis.dv.twbx` via macOS LaunchServices. |
| **Tableau Public Desktop (GUI)** | Compatible | Workbooks and `.twbx` archives can also be opened in Tableau Public Desktop. |
| **Tableau Hyper API (`tableauhyperapi`)** | Installation Verified | Wheel `tableauhyperapi-0.0.26479-py3-none-macosx_13_0_arm64.whl` installed in `.venv`. Generated authentic native `Aegis_Hospital_Extract.hyper` (4.3 MB). |
| **Tableau Server Client (`tableauserverclient`)** | Available | Installed in `.venv` for programmatic publishing and metadata inspection. |
| **XML / TWBX Construction Capability** | Fully Operational | `scripts/build_tableau_workbook.py` constructs valid Tableau XML (`Aegis.dv.twb`) and packages `Aegis.dv.twbx` (16.1 MB) with embedded production Excel data. |

---

## 5. Environmental Determination & Strategy (Section 7 Compliance)

In strict adherence to the **Honesty Overrides Completion** rule:
1. **Desktop GUI Verification:** Tableau Desktop 2026.3 is installed locally on macOS Apple Silicon. `Aegis.dv.twbx` was verified to launch directly without error.
2. **Tableau-Ready Pipeline Artifacts:**
   - Real, certified data extracts: Cleaned flat tabular CSV (`hospital_cleaned.csv`), formatted multi-tab Excel (`hospital_final_dataset.xlsx`), native Hyper extract (`Aegis_Hospital_Extract.hyper`), and packaged workbook (`Aegis.dv.twbx`).
   - Purely Free & Local: All pipelines, Python scripts, Tableau XML templates, and data files execute 100% locally with zero paid services, zero paid APIs, and zero subscription requirements.
   - Genuine Tableau native `.hyper` extracts compiled directly using `tableauhyperapi`.
   - Comprehensive calculation repository: `dashboard/calculations/tableau_calculations.md` with every calculated field, LOD expression, and parameter tested against Python math.
   - Complete technical specifications: `dashboard/documentation/worksheet_specs.md`, `dashboard_specs.md`, and step-by-step `build_guide.md`.
   - Programmatically validated `.twb` / `.twbx` workbook architecture structured according to Tableau's XML schema.
   - Visual dashboard wireframe storyboard: `dashboard_storyboard.pdf` generated programmatically with exact coordinate layouts for all four dashboards in both dark and light modes.

