"""Small helpers shared by the scripts."""
import numpy as np
import pandas as pd

BASE = pd.Timestamp("2019-05-08")                 # first admission date in the data
N_DAYS = (pd.Timestamp("2024-06-30") - BASE).days + 1
DAYS = pd.date_range(BASE, periods=N_DAYS)
MONTH_OF_DAY = DAYS.to_period("M")


def day_index(dates):
    return (pd.to_datetime(dates) - BASE).dt.days.to_numpy()


def daily_census(admit, discharge):
    """Patients in a bed on each day. A patient counts from admission day up to the
    day before discharge, so the sum over all days equals the length of stay."""
    start, end = day_index(admit), day_index(discharge)
    change = np.bincount(start, minlength=N_DAYS + 1) - np.bincount(end, minlength=N_DAYS + 1)
    return np.cumsum(change)[:N_DAYS]
