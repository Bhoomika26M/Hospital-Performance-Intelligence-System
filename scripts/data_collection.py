#!/usr/bin/env python3
"""CLI wrapper for data acquisition."""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.acquisition.data_collection import run_acquisition

if __name__ == "__main__":
    run_acquisition()

