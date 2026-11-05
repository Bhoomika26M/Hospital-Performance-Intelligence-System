
import pandas as pd

# Load healthcare dataset
healthcare = pd.read_csv("data/healthcare_dataset.csv")

# Load HDHI dataset
hdhi = pd.read_csv("data/HDHI Admission data.csv")

def inspect_dataset(df, name):
    print("\n==============================")
    print(name)
    print("==============================")

    print("Dataset Shape:", df.shape)

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nMissing Values:")
    print(df.isnull().sum().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nFirst 5 Records:")
    print(df.head())

inspect_dataset(healthcare, "Healthcare Dataset")
inspect_dataset(hdhi, "HDHI Admission Dataset")
