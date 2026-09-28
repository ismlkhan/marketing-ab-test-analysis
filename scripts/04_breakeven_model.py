"""
Step 4: Break-even cost model.

The z-test tells us the lift is real. It doesn't tell us whether the
campaign is worth running. This models incremental revenue vs.
campaign cost across a 3x3 grid of business assumptions (9 scenarios),
since neither average order value nor cost-per-ad-impression is known
from the dataset -- they're assumptions, stated explicitly here.
"""

import itertools
import pandas as pd
from importlib import import_module

load = import_module("01_load_and_validate").load_data

# --- Assumptions (explicit, not from the data) ---
AOV_SCENARIOS = [20, 35, 50]          # average order value, $
COST_PER_AD_SCENARIOS = [0.02, 0.05, 0.10]  # cost per ad impression, $


def build_scenarios(df: pd.DataFrame) -> pd.DataFrame:
    ad = df[df.test_group == "ad"]
    psa = df[df.test_group == "psa"]

    ad_rate = ad["converted"].mean()
    psa_rate = psa["converted"].mean()
    lift_rate = ad_rate - psa_rate  # as a fraction, not pp

    n_reach = len(ad)                       # potential rollout population
    avg_ads_per_user = ad["total_ads"].mean()  # avg ad impressions/user

    rows = []
    for aov, cost_per_ad in itertools.product(AOV_SCENARIOS, COST_PER_AD_SCENARIOS):
        incr_conversions = lift_rate * n_reach
        incr_revenue = incr_conversions * aov
        campaign_cost = n_reach * avg_ads_per_user * cost_per_ad
        net_value = incr_revenue - campaign_cost
        breakeven_cost_per_ad = incr_revenue / (n_reach * avg_ads_per_user)

        rows.append(
            {
                "aov_usd": aov,
                "cost_per_ad_usd": cost_per_ad,
                "incremental_conversions": round(incr_conversions),
                "incremental_revenue_usd": round(incr_revenue, 2),
                "campaign_cost_usd": round(campaign_cost, 2),
                "net_value_usd": round(net_value, 2),
                "breakeven_cost_per_ad_usd": round(breakeven_cost_per_ad, 4),
                "recommendation": "ship" if net_value > 0 else "hold",
            }
        )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = load()
    scenarios = build_scenarios(df)
    print(scenarios.to_string(index=False))
    scenarios.to_csv("results/breakeven_scenarios.csv", index=False)
    print("\nSaved to results/breakeven_scenarios.csv")
