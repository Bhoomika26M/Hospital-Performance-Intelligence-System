"""Runs the whole pipeline in order. Same as running each script by hand."""
import subprocess, sys
from pathlib import Path

here = Path(__file__).parent
for script in ["make_supporting_data.py", "data_collection.py", "clean_data.py",
               "generate_hospital_kpis.py", "build_dashboard.py", "validate_kpis.py"]:
    print(f"\n=== {script} ===")
    if subprocess.run([sys.executable, here / script], cwd=here).returncode:
        sys.exit(f"{script} failed - fix it before going on")
