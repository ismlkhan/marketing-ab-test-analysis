# Marketing A/B Test Analysis

Did an ad campaign actually move conversion, and is it worth running at scale? A full statistical test, segmentation, and break-even cost model on a 588K-user marketing A/B test.

## Dataset

[Marketing A/B Testing](https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing) (Kaggle) — 588,101 users randomly assigned to see either an ad (`ad`, treatment) or a public service announcement (`psa`, control). Target: `converted`.

| Column | Description |
|---|---|
| `user_id` | Unique user identifier |
| `test_group` | `ad` (treatment) or `psa` (control) |
| `converted` | Whether the user purchased |
| `total_ads` | Number of ads shown to the user |
| `most_ads_day` | Day of week with the most ad exposure |
| `most_ads_hour` | Hour of day with the most ad exposure |

## Approach

1. **Validate** — check for missing values, duplicate rows, and duplicate users. None found (`scripts/01_load_and_validate.py`).
2. **Test** — two-proportion z-test comparing conversion rate between groups, with a 95% confidence interval on the difference (`scripts/02_conversion_test.py`).
3. **Segment** — break the lift down by ad-exposure volume and day of week to see where the effect holds vs. breaks down (`scripts/03_segmentation.py`).
4. **Model the economics** — a break-even cost model across a 3x3 grid of average-order-value and cost-per-ad assumptions (9 scenarios), since neither is known from the data (`scripts/04_breakeven_model.py`).
5. **Recommend** — a conditional rollout recommendation based on all of the above (`notebooks/marketing_ab_test_analysis.ipynb`, full writeup).

## Key results

- **588,101** users validated — 0 missing values, 0 duplicate rows/users
- Ad group converts at **2.55%** vs. **1.79%** for control — a **0.77 percentage point** lift (**43.1%** relative)
- Two-proportion z-test: **p < 0.001**, 95% CI on the lift: **[0.60, 0.94] percentage points** — statistically significant
- Conversion rate rises with ad exposure up through ~100–200 ads/user, then **declines** past that — evidence of diminishing returns
- Lift is uneven across the week: **Tuesday (+1.60pp) and Monday (+1.07pp)** show the strongest effect, **Thursday (+0.14pp)** the weakest
- Break-even model across **9 scenarios** (3 AOV levels x 3 ad-cost levels): a flat, full-population rollout at average exposure (~25 ads/user) is **net-negative in every scenario tested** — break-even cost per ad ranges from **$0.0062–$0.0155**, below the $0.02–$0.10 range modeled

## Recommendation

Not a blanket rollout. The lift is real and significant, but at typical ad costs a flat campaign to everyone doesn't clear break-even. A **capped-exposure, Monday/Tuesday-weighted pilot** — informed by the segmentation findings above — is a cheaper path to most of the same lift, and should be re-measured before committing full budget. Full reasoning and the explicit cost assumptions are in the notebook.

## Repo structure

```
marketing-ab-test-analysis/
├── data/
│   └── marketing_AB.csv
├── notebooks/
│   └── marketing_ab_test_analysis.ipynb   # full analysis, run end-to-end
├── scripts/
│   ├── 01_load_and_validate.py
│   ├── 02_conversion_test.py
│   ├── 03_segmentation.py
│   └── 04_breakeven_model.py
├── results/
│   └── breakeven_scenarios.csv
├── requirements.txt
└── README.md
```

## Running it

```bash
pip install -r requirements.txt
cd marketing-ab-test-analysis
python scripts/01_load_and_validate.py
python scripts/02_conversion_test.py
python scripts/03_segmentation.py
python scripts/04_breakeven_model.py
# or open notebooks/marketing_ab_test_analysis.ipynb for the full writeup
```

## Tools

Python, pandas, statsmodels, Jupyter

## Limitations

Average order value and cost-per-ad-impression aren't in the dataset — both are stated assumptions, tested across a range rather than picked once. The data also doesn't include post-campaign retention or repeat-purchase behavior, which a real rollout decision should weigh alongside the numbers here.
