"""
Step 2: Baseline conversion rates and the two-proportion z-test.

Answers: is the difference in conversion rate between the ad group and
the psa (control) group statistically significant, and how big is it?
"""

import pandas as pd
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep

from importlib import import_module

load = import_module("01_load_and_validate").load_data


def conversion_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("test_group")["converted"].agg(
        conversions="sum", users="count", rate="mean"
    )


def run_z_test(df: pd.DataFrame):
    ad = df.loc[df.test_group == "ad", "converted"]
    psa = df.loc[df.test_group == "psa", "converted"]

    count = [ad.sum(), psa.sum()]
    nobs = [len(ad), len(psa)]

    z_stat, p_value = proportions_ztest(count, nobs, alternative="two-sided")
    ci_low, ci_high = confint_proportions_2indep(
        count[0], nobs[0], count[1], nobs[1], method="wald"
    )

    ad_rate = count[0] / nobs[0]
    psa_rate = count[1] / nobs[1]
    diff_pp = (ad_rate - psa_rate) * 100
    relative_lift = (ad_rate - psa_rate) / psa_rate * 100

    return {
        "ad_rate_pct": ad_rate * 100,
        "psa_rate_pct": psa_rate * 100,
        "diff_pp": diff_pp,
        "relative_lift_pct": relative_lift,
        "z_stat": z_stat,
        "p_value": p_value,
        "ci_95_low_pp": ci_low * 100,
        "ci_95_high_pp": ci_high * 100,
    }


if __name__ == "__main__":
    df = load()

    print("Conversion summary by group:")
    print(conversion_summary(df))

    print("\nTwo-proportion z-test:")
    results = run_z_test(df)
    for k, v in results.items():
        print(f"  {k}: {v:.6f}" if isinstance(v, float) else f"  {k}: {v}")
