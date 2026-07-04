import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from vstyle import *
KW="#c792ea"; LT="#e7ebf3"; TB="#82aaff"; NUM="#f78c6c"; CM="#6b7385"

def code_line(ax, tokens, x0, y, charw=0.205, fs=15):
    x=x0
    for txt,col in tokens:
        ax.text(x,y,txt,ha="left",va="center",family="monospace",fontsize=fs,color=col)
        x+=len(txt)*charw
def brow(ax, y, token, role, tx=0.7, ax_arrow=4.85, rx=5.25):
    ax.text(tx,y,token,family="monospace",fontsize=12.5,color="#a050c0",va="center",fontweight="bold")
    ax.text(ax_arrow,y,"→",fontsize=12,color=INK_FAINT,va="center",ha="center")
    ax.text(rx,y,role,fontsize=11.5,color=INK_SOFT,va="center")

# ================= s_sql_select : SELECT anatomy =================
fig,ax=plt.subplots(figsize=(11,6.9)); ax.axis("off"); ax.set_xlim(0,12.2); ax.set_ylim(0,8.7)
ax.add_patch(FancyBboxPatch((0.45,5.55),8.5,2.75,boxstyle="round,pad=0.05",facecolor="#1d2330",edgecolor="#2a3142",lw=1.2))
code_line(ax,[("SELECT ",KW),("customer, amount",LT)],0.8,7.95)
code_line(ax,[("FROM ",KW),("orders",TB)],0.8,7.45)
code_line(ax,[("WHERE ",KW),("amount ",LT),("> ",LT),("100",NUM)],0.8,6.95)
code_line(ax,[("ORDER BY ",KW),("amount ",LT),("DESC",KW)],0.8,6.45)
code_line(ax,[("LIMIT ",KW),("3",NUM),(";",LT)],0.8,5.95)
ax.text(0.5,5.15,"Each clause, explained:",fontsize=11.5,color=INK,fontweight="bold")
brow(ax,4.68,"SELECT","the columns you want back  (use * for every column)")
brow(ax,4.23,"FROM","which table to read from")
brow(ax,3.78,"WHERE","keep only rows that match a condition")
brow(ax,3.33,"ORDER BY","sort the rows  (DESC = high → low, ASC = low → high)")
brow(ax,2.88,"LIMIT","return only the first N rows")
ax.add_patch(FancyBboxPatch((0.45,0.45),11.3,1.75,boxstyle="round,pad=0.05",facecolor="#f7f8fa",edgecolor="#e0e3ea",lw=1.2))
ax.text(0.8,1.78,"Reads like a plain-English request:",fontsize=11,color=INK,fontweight="bold")
ax.text(0.8,1.15,"“From orders, take customer & amount, keep rows where amount is over 100, "
        "sort highest first, and give me the top 3.”",fontsize=11.5,color=INK_SOFT,style="italic")
ax.set_title("Anatomy of a SELECT: how you ask a database a question",loc="left",fontsize=14,pad=10)
save(fig,"s_sql_select.png")

# ================= s_sql_runorder : written vs execution order =================
fig,ax=plt.subplots(figsize=(11.6,3.5)); ax.axis("off"); ax.set_xlim(0,11.6); ax.set_ylim(0,3.2)
steps=[("FROM","pick the table",TEAL,TEAL_BG),
       ("WHERE","filter rows",AMBER,AMBER_BG),
       ("SELECT","choose columns",INDIGO,INDIGO_BG),
       ("ORDER BY","sort them",ROSE,ROSE_BG),
       ("LIMIT","cut to N",GREEN,GREEN_BG)]
bw,gap=1.92,0.30; x0=0.35
for i,(name,role,ec,fc) in enumerate(steps):
    x=x0+i*(bw+gap)
    ax.add_patch(FancyBboxPatch((x,1.15),bw,1.05,boxstyle="round,pad=0.03",facecolor=fc,edgecolor=ec,lw=1.8))
    ax.text(x+bw/2,1.83,name,ha="center",va="center",fontsize=13,color=ec,fontweight="bold",family="monospace")
    ax.text(x+bw/2,1.42,role,ha="center",va="center",fontsize=10.5,color=INK_SOFT)
    ax.text(x+0.18,2.02,str(i+1),ha="center",va="center",fontsize=10,color=ec,fontweight="bold")
    if i<len(steps)-1:
        ax.annotate("",xy=(x+bw+gap-0.02,1.675),xytext=(x+bw+0.02,1.675),
                    arrowprops=dict(arrowstyle="-|>",color=INK_FAINT,lw=1.8))
ax.text(0.35,2.78,"SQL's real execution order — you write SELECT first, but it runs third",
        fontsize=13.5,color=INK,fontweight="bold")
ax.text(0.35,0.55,"So an alias or a column you build in SELECT isn't ready yet in WHERE "
        "(which already ran) — a classic beginner gotcha.",fontsize=10.5,color=INK_FAINT,style="italic")
save(fig,"s_sql_runorder.png")
print("VIZ SQL DONE")
