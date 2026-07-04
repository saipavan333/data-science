import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from vstyle import *

def table(ax, cols, rows, x0=0, y0=0, cw=2.0, ch=0.6, idx=None, idx_label="index",
          hi_col=None, hi_row=None, header_fc="#f0f2f8"):
    ncol=len(cols)
    # header
    for j,c in enumerate(cols):
        fc = AMBER_BG if hi_col==j else header_fc
        ax.add_patch(Rectangle((x0+j*cw, y0), cw, ch, facecolor=fc, edgecolor="#c7cee0", lw=1.3))
        ax.text(x0+j*cw+cw/2, y0+ch/2, c, ha="center", va="center", fontsize=11.5, fontweight="bold", color=INK_SOFT)
    # rows
    for i,row in enumerate(rows):
        yy=y0-(i+1)*ch
        if idx is not None:
            fc = TEAL_BG if hi_row==i else "#f7f8fa"
            ax.add_patch(Rectangle((x0-cw*0.7, yy), cw*0.7, ch, facecolor=fc, edgecolor="#d8dce3", lw=1.2))
            ax.text(x0-cw*0.35, yy+ch/2, str(idx[i]), ha="center", va="center", fontsize=11, color=INK_SOFT, fontweight="bold")
        for j,val in enumerate(row):
            fc="white"
            if hi_col==j: fc=AMBER_BG
            if hi_row==i: fc=TEAL_BG
            if hi_col==j and hi_row==i: fc="#f3e2c0"
            ax.add_patch(Rectangle((x0+j*cw, yy), cw, ch, facecolor=fc, edgecolor="#e0e3ea", lw=1.1))
            ax.text(x0+j*cw+cw/2, yy+ch/2, str(val), ha="center", va="center", fontsize=11, color=INK)
    if idx is not None:
        ax.text(x0-cw*0.35, y0+ch/2, idx_label, ha="center", va="center", fontsize=9.5, color=INK_FAINT, style="italic")

# --- 2.3 DataFrame anatomy ---
fig, ax = plt.subplots(figsize=(10.5,4.4)); ax.axis("off"); ax.set_xlim(-2.2,7.2); ax.set_ylim(-2.7,1.6)
cols=["category","amount","returned"]
rows=[["Electronics",180,"False"],["Apparel",45,"True"],["Electronics",220,"False"],["Beauty",30,"False"]]
table(ax, cols, rows, x0=0, y0=0.6, cw=1.9, ch=0.6, idx=[0,1,2,3], hi_col=1)
ax.annotate("columns (labeled)", xy=(2.85,1.2), xytext=(3.6,1.45), fontsize=11, color=INK_SOFT,
            arrowprops=dict(arrowstyle="->",color=INK_FAINT,lw=1.2))
ax.annotate("index\n(row labels)", xy=(-0.7,-0.9), xytext=(-2.1,-0.6), fontsize=11, color=TEAL,
            arrowprops=dict(arrowstyle="->",color=TEAL,lw=1.2))
ax.annotate("one column\n= a Series", xy=(2.85,-1.5), xytext=(4.0,-1.9), fontsize=11, color=AMBER,
            arrowprops=dict(arrowstyle="->",color=AMBER,lw=1.3))
ax.set_title("Anatomy of a DataFrame: labeled columns, a row index, and Series inside", loc="left", fontsize=14)
save(fig,"s_pd_dataframe.png")

# --- 2.3 loc vs iloc ---
fig, ax = plt.subplots(figsize=(10.5,4.6)); ax.axis("off"); ax.set_xlim(-2.4,7.0); ax.set_ylim(-3.2,1.8)
idx=["a101","a102","a103","a104"]
table(ax, cols, rows, x0=0, y0=0.6, cw=1.9, ch=0.6, idx=idx, idx_label="index", hi_row=2)
ax.text(-2.2,-2.2,'df.loc["a103"]', fontsize=12.5, color=TEAL, family="monospace", fontweight="bold")
ax.text(-2.2,-2.6,"by LABEL", fontsize=10.5, color=TEAL)
ax.text(2.6,-2.2,'df.iloc[2]', fontsize=12.5, color=ROSE, family="monospace", fontweight="bold")
ax.text(2.6,-2.6,"by POSITION (0-based)", fontsize=10.5, color=ROSE)
ax.annotate("", xy=(0.2,-1.35), xytext=(-1.0,-2.05), arrowprops=dict(arrowstyle="->",color=TEAL,lw=1.4))
ax.annotate("", xy=(3.4,-1.35), xytext=(3.2,-2.05), arrowprops=dict(arrowstyle="->",color=ROSE,lw=1.4))
ax.text(2.5,1.45,"both select the SAME row — one by its name, one by its position",
        fontsize=11, color=INK_SOFT, ha="center")
ax.set_title("loc vs iloc: select by label or by position", loc="left", fontsize=14)
save(fig,"s_pd_loc_iloc.png")

# --- 2.4 cleaning workflow ---
dot('''
 L [label="1. Load\\npd.read_csv(...)", fillcolor="#eef1fd", color="#cdd7fb"];
 I [label="2. Inspect\\n.shape .dtypes .info()\\n.isna().sum()  .duplicated()", fillcolor="#e3f5f3", color="#bfe7e3"];
 T [label="3. Fix dtypes\\nparse dates, numbers,\\ncategories", fillcolor="#e3f5f3", color="#bfe7e3"];
 M [label="4. Handle missing\\ndrop / impute / flag", fillcolor="#fbf3e0", color="#ecd9ad"];
 D [label="5. Drop duplicates", fillcolor="#e3f5f3", color="#bfe7e3"];
 O [label="6. Check outliers\\n& impossible values", fillcolor="#fbf3e0", color="#ecd9ad"];
 V [label="7. Validate & document\\n(every choice defensible)", fillcolor="#e6f5ec", color="#bfe0c8"];
 L -> I -> T -> M -> D -> O -> V;
''', "s_clean_flow.png", rd="TB", rs="0.32", ns="0.4")

# --- 2.4 missing-data decision ---
dot('''
 q [label="A value is missing.\\nWhy, and how much?", shape=diamond, style="filled", fillcolor="#fbf3e0", color="#ecd9ad"];
 drop [label="DROP the row\\nonly if rare & unrelated\\n(risk: bias)", fillcolor="#fce8ee", color="#e7b9c6"];
 imp  [label="IMPUTE a value\\nmedian / mode / model\\n(keeps n; invents data)", fillcolor="#e3f5f3", color="#bfe7e3"];
 flag [label="FLAG it\\nlabel 'Unknown' / add a\\n'was-missing' column", fillcolor="#e6f5ec", color="#bfe0c8"];
 q -> drop [label="few, random"];
 q -> imp  [label="need full n"];
 q -> flag [label="missingness\\nis informative"];
''', "s_clean_missing.png", rd="TB", rs="0.55", ns="0.5")
print("BATCH E DONE")
