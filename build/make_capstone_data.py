# -*- coding: utf-8 -*-
"""Generate a realistic (synthetic) e-commerce orders dataset for the capstone.
Deliberately includes real-world messiness: missing values, a few data-entry
errors, duplicates, and string dates — so the EDA has something to clean."""
import numpy as np, pandas as pd

np.random.seed(2025)
OUT = "/sessions/zen-pensive-thompson/mnt/Tutorials/data-science-academy/data/ecommerce_orders.csv"

N = 5000
cats = ["Electronics", "Home", "Apparel", "Beauty", "Sports"]
cat_p = [0.22, 0.20, 0.28, 0.16, 0.14]
cat_price = {"Electronics": 180, "Home": 60, "Apparel": 45, "Beauty": 28, "Sports": 75}
cat_return = {"Electronics": .06, "Home": .05, "Apparel": .17, "Beauty": .08, "Sports": .09}
regions = ["North", "South", "East", "West"]
channels = ["Web", "Mobile", "Store"]

# Order dates across 2025 with a Q4 holiday lift and a summer dip.
month_weight = np.array([0.7, 0.7, 0.85, 0.9, 1.0, 0.8, 0.75, 0.85, 1.0, 1.15, 1.6, 1.9])
month_weight = month_weight / month_weight.sum()
months = np.random.choice(np.arange(1, 13), size=N, p=month_weight)
days = np.random.randint(1, 28, size=N)
dates = pd.to_datetime(dict(year=2025, month=months, day=days))

cat = np.random.choice(cats, size=N, p=cat_p)
qty = np.random.choice([1, 2, 3, 4, 5], size=N, p=[0.5, 0.25, 0.13, 0.08, 0.04])
unit_price = np.array([max(3, np.random.lognormal(np.log(cat_price[c]), 0.45)) for c in cat]).round(2)
discount = np.random.choice([0.0, 0.05, 0.10, 0.20], size=N, p=[0.6, 0.2, 0.13, 0.07])
channel = np.random.choice(channels, size=N, p=[0.45, 0.40, 0.15])
region = np.random.choice(regions, size=N, p=[0.3, 0.25, 0.25, 0.2])
cust = np.random.randint(10000, 13000, size=N)        # repeat customers
returned = np.array([np.random.rand() < cat_return[c] for c in cat])
order_value = (qty * unit_price * (1 - discount)).round(2)

df = pd.DataFrame({
    "order_id": np.arange(100000, 100000 + N),
    "order_date": dates.dt.strftime("%Y-%m-%d"),      # stored as strings (realistic)
    "customer_id": cust,
    "region": region,
    "category": cat,
    "channel": channel,
    "quantity": qty,
    "unit_price": unit_price,
    "discount": discount,
    "order_value": order_value,
    "is_returned": returned,
})

# --- inject realistic messiness ---------------------------------------------
miss = np.random.choice(N, size=int(0.03 * N), replace=False)      # 3% missing region
df.loc[miss, "region"] = np.nan
err = np.random.choice(N, size=8, replace=False)                   # a few bad order_values
df.loc[err, "order_value"] = [-5.0, 0.0, -120.0, 0.0, -1.0, 99999.0, -45.0, 0.0]
dupes = df.sample(15, random_state=1).copy()                       # duplicate rows
df = pd.concat([df, dupes], ignore_index=True)
df = df.sample(frac=1, random_state=7).reset_index(drop=True)      # shuffle

df.to_csv(OUT, index=False)
print("wrote", OUT)
print("rows:", len(df), "| columns:", list(df.columns))
print("missing region:", df.region.isna().sum(), "| duplicates:", df.duplicated().sum())
print(df.head(3).to_string())
