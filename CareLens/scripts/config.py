"""Project settings. If a number or mapping needs changing, change it here."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
DATA = ROOT / "data"
DOCS = ROOT / "docs"
DASH = ROOT / "dashboard"

# The data starts on 8 May 2019, so the first weeks of census are artificially low
# (patients admitted before that date are missing). Same problem at the end.
# All KPIs use only the months in between.
WINDOW_START = "2019-07"
WINDOW_END = "2024-04"

OCCUPANCY_TARGET = 0.85   # target used for the efficiency score

# The dataset has no department column, so I group medical conditions into departments.
CONDITION_TO_DEPT = {
    "Cancer": "Oncology",
    "Hypertension": "Cardiology",
    "Diabetes": "Endocrinology",
    "Obesity": "Endocrinology",
    "Asthma": "Pulmonology",
    "Arthritis": "Rheumatology",
}
