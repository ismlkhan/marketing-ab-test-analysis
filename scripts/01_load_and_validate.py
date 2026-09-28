"""
Step 1: Load and validate the marketing A/B test dataset.

Source: Marketing A/B Testing dataset (Kaggle, faviovaz/marketing-ab-testing)
Two groups: 'ad' (saw the campaign) vs 'psa' (control, saw a public
service announcement instead of an ad).
"""

import pandas as pd

DATA_PATH = "data/marketing_AB.csv"


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def validate(df: pd.DataFrame) -> None:
    print(f"Rows: {len(df):,}")
    print(f"Columns: {list(df.columns)}")

    n_missing = df.isnull().sum().sum()
    print(f"Missing values (total): {n_missing}")

    n_dupe_rows = df.duplicated().sum()
    n_dupe_users = df["user_id"].duplicated().sum()
    print(f"Duplicate rows: {n_dupe_rows}")
    print(f"Duplicate user_ids: {n_dupe_users}")

    print("\nGroup sizes:")
    print(df["test_group"].value_counts())


if __name__ == "__main__":
    df = load_data()
    validate(df)
