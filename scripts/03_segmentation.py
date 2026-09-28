"""
Step 3: Segment the effect.

A single overall lift number can hide where the campaign is actually
working. This checks:
  1. Conversion rate by ad-exposure bucket (diminishing returns?)
  2. Conversion rate by day of week, ad vs. psa
"""

import pandas as pd
from importlib import import_module

load = import_module("01_load_and_validate").load_data


def exposure_buckets(df: pd.DataFrame) -> pd.DataFrame:
    ad = df[df.test_group == "ad"].copy()
    bins = [0, 10, 25, 50, 100, 200, ad["total_ads"].max()]
    ad["ad_bucket"] = pd.cut(ad["total_ads"], bins=bins)
    return ad.groupby("ad_bucket", observed=True)["converted"].agg(
        conversion_rate="mean", users="count"
    )


def day_of_week(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["most_ads_day", "test_group"], observed=True)["converted"]
        .mean()
        .unstack("test_group")
        .assign(lift_pp=lambda x: (x["ad"] - x["psa"]) * 100)
        .sort_values("lift_pp", ascending=False)
    )


if __name__ == "__main__":
    df = load()

    print("Conversion rate by ad-exposure bucket (ad group only):")
    print(exposure_buckets(df))
    print(
        "\nNote: conversion keeps climbing through the 100-200 ad bucket, "
        "then drops in the 200+ bucket -- evidence of diminishing (or even "
        "negative) returns to very heavy ad exposure."
    )

    print("\nConversion rate by day of week, ad vs. psa:")
    print(day_of_week(df))
