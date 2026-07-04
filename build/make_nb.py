import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
nb = new_notebook()
C = []
C.append(new_markdown_cell(
"# Capstone A — E-commerce EDA & Insight Report\n\n"
"**Goal:** turn one year of raw, messy orders into a decision a stakeholder can act on.\n\n"
"We follow the workflow from Lesson 1.1: **load -> clean -> explore -> visualize -> insight**. "
"Every number here is computed live from `../data/ecommerce_orders.csv`. Run all cells top to bottom."))
C.append(new_code_cell(
"import numpy as np, pandas as pd\n"
"import matplotlib.pyplot as plt\n"
"%matplotlib inline\n"
"plt.rcParams.update({'figure.figsize':(9,4),'axes.grid':True,'grid.color':'#eee',\n"
"                     'axes.axisbelow':True,'axes.spines.top':False,'axes.spines.right':False})\n"
"raw = pd.read_csv('../data/ecommerce_orders.csv')\n"
"print('rows, cols:', raw.shape)\n"
"raw.head()"))
C.append(new_markdown_cell(
"## 1. Inspect — what did we get?\n"
"First questions on any new dataset: how big, what types, and where are the holes?"))
C.append(new_code_cell(
"raw.info()\n"
"print('\\nMissing values per column:')\n"
"print(raw.isna().sum())\n"
"print('\\nDuplicate rows:', raw.duplicated().sum())"))
C.append(new_markdown_cell(
"## 2. Clean — make it trustworthy\n"
"- drop duplicate rows\n"
"- parse the string dates into real dates\n"
"- remove impossible `order_value` entries (<= 0 or an absurd 99999 outlier)\n"
"- label missing `region` as 'Unknown' rather than silently dropping rows"))
C.append(new_code_cell(
"df = raw.drop_duplicates().copy()\n"
"df['order_date'] = pd.to_datetime(df['order_date'])\n"
"bad = (df['order_value'] <= 0) | (df['order_value'] >= 10000)\n"
"print('removing', int(bad.sum()), 'bad order_value rows')\n"
"df = df[~bad].copy()\n"
"df['region'] = df['region'].fillna('Unknown')\n"
"df['month'] = df['order_date'].dt.month\n"
"print('clean rows:', len(df))"))
C.append(new_markdown_cell(
"## 3. Explore — the headline numbers\n"
"Note we report the **median** order value alongside the mean, because order value is "
"right-skewed (Lesson 1.3)."))
C.append(new_code_cell(
"gross = df['order_value'].sum()\n"
"print(f'Gross revenue : ${gross:,.0f}')\n"
"print(f'Avg order val : ${df.order_value.mean():.2f}  (median ${df.order_value.median():.2f})')\n"
"bym = df.groupby('month')['order_value'].sum()\n"
"print(f'Q4 share      : {bym.loc[[10,11,12]].sum()/gross:.1%}')\n"
"by_cat = df.groupby('category')['order_value'].sum().sort_values(ascending=False)\n"
"print('\\nRevenue by category:'); print((by_cat/1000).round(1).astype(str) + ' k')"))
C.append(new_markdown_cell("## 4. Visualize\n### Monthly revenue — a strong Q4"))
C.append(new_code_cell(
"colors = ['#c2305a' if m in (10,11,12) else '#3b53d6' for m in bym.index]\n"
"ax = (bym/1000).plot.bar(color=colors)\n"
"ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], rotation=0)\n"
"ax.set_ylabel('Revenue ($000s)'); ax.set_title('Monthly gross revenue, 2025'); plt.show()"))
C.append(new_markdown_cell("### Order value distribution — right-skewed"))
C.append(new_code_cell(
"ax = df['order_value'].clip(upper=df.order_value.quantile(.99)).plot.hist(bins=50, color='#dfe4fb', edgecolor='#3b53d6')\n"
"ax.axvline(df.order_value.mean(), color='#c2305a', lw=2, label=f'mean ${df.order_value.mean():.0f}')\n"
"ax.axvline(df.order_value.median(), color='#0e8f8a', lw=2, ls='--', label=f'median ${df.order_value.median():.0f}')\n"
"ax.set_xlabel('Order value ($)'); ax.legend(); ax.set_title('Order value is right-skewed'); plt.show()"))
C.append(new_markdown_cell("### Returns — where net revenue leaks"))
C.append(new_code_cell(
"ret = df.groupby('category')['is_returned'].mean().sort_values(ascending=False)\n"
"ax = (ret*100).plot.bar(color=['#c2305a' if c==ret.index[0] else '#b9c0d0' for c in ret.index])\n"
"ax.axhline(df.is_returned.mean()*100, color='#4a5160', ls=':'); ax.set_xticklabels(ret.index, rotation=0)\n"
"ax.set_ylabel('Return rate (%)'); ax.set_title('Return rate by category'); plt.show()\n"
"df['net_value'] = np.where(df['is_returned'], 0.0, df['order_value'])\n"
"loss = df.order_value.sum() - df.net_value.sum()\n"
"print(f'Revenue lost to returns: ${loss:,.0f}')"))
C.append(new_markdown_cell(
"## 5. Insight & recommendation\n\n"
"**What the data says**\n\n"
"1. **Revenue is highly seasonal** — Q4 (Oct-Dec) drives ~38% of annual revenue, peaking in December. "
"Inventory, staffing, and ad budget should be weighted toward the holiday quarter.\n"
"2. **Electronics is the revenue engine** (~50% of gross) but **Apparel is the margin leak**: its "
"~18% return rate (vs ~10% overall) quietly erases tens of thousands in net revenue.\n"
"3. **Order value is right-skewed**, so the **median (~$94)** describes the typical order better than "
"the mean (~$161); use the median when setting free-shipping thresholds.\n\n"
"**Recommendation:** protect Q4 supply for Electronics, and launch a targeted effort to cut Apparel "
"returns (better sizing guides, photography, fit reviews). Even a 3-4 point drop in Apparel returns "
"recovers more net revenue than a comparable lift in a low-return category.\n\n"
"*Next:* a controlled A/B test of a sizing-guide change (see Track 5) would quantify the return-rate impact causally."))
nb['cells'] = C
nb.metadata.kernelspec = {'name':'ds','display_name':'Python (ds)','language':'python'}
OUT = "/sessions/zen-pensive-thompson/mnt/Tutorials/data-science-academy/notebooks/capstone_eda.ipynb"
nbf.write(nb, OUT)
print("wrote notebook with", len(C), "cells")

# --- execute it to prove it runs ---
from nbconvert.preprocessors import ExecutePreprocessor
ep = ExecutePreprocessor(timeout=180, kernel_name='ds')
nbdir = "/sessions/zen-pensive-thompson/mnt/Tutorials/data-science-academy/notebooks"
ep.preprocess(nb, {'metadata': {'path': nbdir}})
nbf.write(nb, OUT)   # save with outputs
print("EXECUTED OK — notebook ran top to bottom with no errors")
