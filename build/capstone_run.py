import os, json, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
SITE="/sessions/zen-pensive-thompson/mnt/Tutorials/data-science-academy"; IMG=SITE+"/assets/img"
INDIGO,TEAL,AMBER,ROSE,GREEN="#3b53d6","#0e8f8a","#b7791f","#c2305a","#1f8a4c"
INK,INK_SOFT="#1f2430","#4a5160"
plt.rcParams.update({"figure.facecolor":"white","axes.facecolor":"white","font.size":12,
 "font.family":"DejaVu Sans","axes.edgecolor":INK_SOFT,"axes.titlesize":14,"axes.titleweight":"bold",
 "axes.titlecolor":INK,"axes.labelcolor":INK_SOFT,"xtick.color":INK_SOFT,"ytick.color":INK_SOFT,
 "axes.grid":True,"grid.color":"#edeff3","axes.axisbelow":True,"savefig.dpi":150,"savefig.bbox":"tight"})
def ds(ax):
    for s in ("top","right"): ax.spines[s].set_visible(False)
R={}
raw=pd.read_csv(SITE+"/data/ecommerce_orders.csv"); R["n_raw"]=len(raw)
df=raw.drop_duplicates().copy(); R["n_dupes"]=R["n_raw"]-len(df)
df["order_date"]=pd.to_datetime(df["order_date"])
bad=(df["order_value"]<=0)|(df["order_value"]>=10000); R["n_bad_value"]=int(bad.sum())
df=df[~bad].copy(); R["n_missing_region"]=int(df["region"].isna().sum())
df["region"]=df["region"].fillna("Unknown"); df["month"]=df["order_date"].dt.month; R["n_clean"]=len(df)
R["gross"]=df["order_value"].sum(); R["aov"]=df["order_value"].mean(); R["aov_median"]=df["order_value"].median()
bym=df.groupby("month")["order_value"].sum(); R["q4_share"]=bym.loc[[10,11,12]].sum()/R["gross"]; R["peak_month"]=int(bym.idxmax())
byc=df.groupby("category")["order_value"].sum().sort_values(ascending=False); R["top_cat"]=byc.index[0]; R["top_cat_share"]=byc.iloc[0]/R["gross"]
rbc=df.groupby("category")["is_returned"].mean().sort_values(ascending=False); R["overall_return"]=df["is_returned"].mean(); R["worst_ret_cat"]=rbc.index[0]; R["worst_ret_rate"]=rbc.iloc[0]
df["net_value"]=np.where(df["is_returned"],0.0,df["order_value"])
gc=df.groupby("category")["order_value"].sum(); nc=df.groupby("category")["net_value"].sum()
R["net"]=df["net_value"].sum(); R["return_loss"]=R["gross"]-R["net"]; R["apparel_loss"]=gc["Apparel"]-nc["Apparel"]
R["top_channel"]=df.groupby("channel")["order_value"].sum().idxmax()
M=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
# (a) monthly
fig,ax=plt.subplots(figsize=(10.5,4.3))
ax.bar([M[m-1] for m in bym.index],bym.values/1000,color=[ROSE if m in (10,11,12) else INDIGO for m in bym.index])
ax.set_title("Monthly gross revenue, 2025 — a strong Q4",loc="left"); ax.set_ylabel("Revenue ($000s)"); ds(ax)
ax.annotate("Q4 holiday lift",xy=(10.5,bym.loc[[11,12]].mean()/1000),xytext=(6.0,bym.max()/1000*0.96),color=ROSE,fontsize=11,arrowprops=dict(arrowstyle="->",color=ROSE,lw=1.4))
fig.savefig(IMG+"/cap_monthly.png",facecolor="white"); plt.close(fig)
# (b) category
fig,ax=plt.subplots(figsize=(10.5,4.0)); ax.barh(byc.index[::-1],byc.values[::-1]/1000,color=TEAL)
ax.set_title("Gross revenue by category",loc="left"); ax.set_xlabel("Revenue ($000s)"); ds(ax)
for i,v in enumerate(byc.values[::-1]): ax.text(v/1000+1,i,f"${v/1000:.0f}k",va="center",fontsize=10.5,color=INK_SOFT)
fig.savefig(IMG+"/cap_category.png",facecolor="white"); plt.close(fig)
# (c) order value dist
fig,ax=plt.subplots(figsize=(10.5,4.0)); ax.hist(df["order_value"],bins=60,color="#dfe4fb",edgecolor=INDIGO,linewidth=.5)
ax.axvline(R["aov"],color=ROSE,lw=2.2,label=f"Mean ${R['aov']:.0f}"); ax.axvline(R["aov_median"],color=TEAL,lw=2.2,ls="--",label=f"Median ${R['aov_median']:.0f}")
ax.set_title("Order value is right-skewed — report the median AOV",loc="left"); ax.set_xlabel("Order value ($)"); ax.set_ylabel("Number of orders")
ax.legend(frameon=False); ds(ax); ax.set_xlim(0,df["order_value"].quantile(0.99)); fig.savefig(IMG+"/cap_ordervalue.png",facecolor="white"); plt.close(fig)
# (d) returns
fig,ax=plt.subplots(figsize=(10.5,4.0)); bars=ax.bar(rbc.index,rbc.values*100,color=[ROSE if c==R["worst_ret_cat"] else "#b9c0d0" for c in rbc.index])
ax.axhline(R["overall_return"]*100,color=INK_SOFT,ls=":",lw=1.5); ax.text(len(rbc)-0.4,R["overall_return"]*100+0.4,f"overall {R['overall_return']*100:.1f}%",color=INK_SOFT,fontsize=10,ha="right")
ax.set_title("Return rate by category — Apparel is the outlier",loc="left"); ax.set_ylabel("Return rate (%)"); ds(ax)
for b,v in zip(bars,rbc.values): ax.text(b.get_x()+b.get_width()/2,v*100+0.3,f"{v*100:.1f}%",ha="center",fontsize=10.5,color=INK_SOFT)
fig.savefig(IMG+"/cap_returns.png",facecolor="white"); plt.close(fig)
# (e) net impact
fig,ax=plt.subplots(figsize=(10.5,4.3)); order=gc.sort_values(ascending=False).index; x=np.arange(len(order)); w=0.4
ax.bar(x-w/2,[gc[c]/1000 for c in order],w,label="Gross revenue",color="#c9d0f3"); ax.bar(x+w/2,[nc[c]/1000 for c in order],w,label="Net (after returns)",color=GREEN)
ax.set_xticks(x); ax.set_xticklabels(order); ax.set_title("Returns erode Apparel's contribution the most",loc="left"); ax.set_ylabel("Revenue ($000s)"); ax.legend(frameon=False); ds(ax)
fig.savefig(IMG+"/cap_netimpact.png",facecolor="white"); plt.close(fig)
print("charts OK"); print("RESULTS_JSON="+json.dumps({k:(round(v,4) if isinstance(v,(int,float)) else v) for k,v in R.items()}))
