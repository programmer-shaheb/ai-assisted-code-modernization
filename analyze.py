# analyze.py
# Make KM-Waechter smarter. The 80% rule only warns you once a car is nearly worn. Here you find
# which cars are most likely to break down SOON, from their history, and rank them by risk, so the
# fleet team fixes the risky ones first.
#
# fleet_history.csv has one row per car (120 of them) and a "broke_down" column (1 = it later
# broke down).
#
# TODO(you), with IBM Bob and pandas:
#   1. Load fleet_history.csv.
#   2. Find which columns actually separate the cars that broke down from those that did not.
#      Do not assume. Compare the two groups column by column and let the numbers answer.
#      (Total mileage and age look like the obvious answers. Check whether they really are.)
#   3. Build a simple risk score from 0 to 100 for each car, from the columns that DO separate.
#      No heavy machine learning needed.
#   4. Print the cars ranked by risk, highest first.
#   5. Write a two-line summary at the top of this file: which factors matter most, and why.

# analyze.py
# Breakdown risk is driven by the factors that differ most between cars
# that broke down and those that did not. Total mileage is checked rather
# than assumed to be important.

import pandas as pd


df = pd.read_csv("fleet_history.csv")

FEATURES = [
    "odometer_km",
    "km_since_service",
    "avg_daily_km",
    "load_factor",
    "age_years",
]


# Compare cars that broke down with cars that did not.
group_means = df.groupby("broke_down")[FEATURES].mean()

print("Average values by breakdown outcome:")
print(group_means.round(2))


# Measure how strongly each feature separates the two groups.
# Dividing the mean difference by the overall standard deviation makes
# features with different units easier to compare.
effects = {}

for feature in FEATURES:
    no_breakdown = group_means.loc[0, feature]
    breakdown = group_means.loc[1, feature]
    std = df[feature].std()

    if std == 0:
        effects[feature] = 0
    else:
        effects[feature] = abs(breakdown - no_breakdown) / std


print("\nRelative separation between the groups:")
for feature, effect in sorted(
    effects.items(),
    key=lambda item: item[1],
    reverse=True,
):
    print(f"{feature}: {effect:.3f}")


# Use the three strongest signals for a simple risk score.
risk_features = sorted(
    effects,
    key=effects.get,
    reverse=True,
)[:3]

total_weight = sum(effects[f] for f in risk_features)

df["risk_score"] = 0.0

for feature in risk_features:
    minimum = df[feature].min()
    maximum = df[feature].max()

    if maximum == minimum:
        normalized = 0
    else:
        normalized = (df[feature] - minimum) / (maximum - minimum)

    weight = effects[feature] / total_weight
    df["risk_score"] += normalized * weight * 100


df["risk_score"] = df["risk_score"].clip(0, 100)

ranked = df.sort_values("risk_score", ascending=False)

print("\nFactors used for risk score:")
print(", ".join(risk_features))

print("\nCars ranked by breakdown risk:")
print(
    ranked[
        [
            "car_id",
            *risk_features,
            "risk_score",
        ]
    ]
    .head(20)
    .to_string(index=False)
)