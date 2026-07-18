import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from vstyle import *
def table(ax, cols, rows, x0, y0, cw=1.9, ch=0.6, idx=None, hi_col=None, hi_row=None):
    for j,c in enumerate(cols):
        fc=AMBER_BG if hi_col==j else "#f0f2f8"
        ax.add_patch(Rectangle((x0+j*cw,y0),cw,ch,facecolor=fc,edgecolor="#c7cee0",lw=1.3))
        ax.text(x0+j*cw+cw/2,y0+ch/2,c,ha="center",va="center",fontsize=11.5,fontweight="bold",color=INK_SOFT)
    for i,row in enumerate(rows):
        yy=y0-(i+1)*ch
        if idx is not None:
            fc=TEAL_BG if hi_row==i else "#f7f8fa"
            ax.add_patch(Rectangle((x0-cw*0.7,yy),cw*0.7,ch,facecolor=fc,edgecolor="#d8dce3",lw=1.2))
            ax.text(x0-cw*0.35,yy+ch/2,str(idx[i]),ha="center",va="center",fontsize=11,color=INK_SOFT,fontweight="bold")
        for j,val in enumerate(row):
            fc="white"
            if hi_col==j: fc=AMBER_BG
            if hi_row==i: fc=TEAL_BG
            ax.add_patch(Rectangle((x0+j*cw,yy),cw,ch,facecolor=fc,edgecolor="#e0e3ea",lw=1.1))
            ax.text(x0+j*cw+cw/2,yy+ch/2,str(val),ha="center",va="center",fontsize=11,color=INK)
    if idx is not None:
        ax.text(x0-cw*0.35,y0+ch/2,"index",ha="center",va="center",fontsize=9.5,color=INK_FAINT,style="italic")

fig,ax=plt.subplots(figsize=(10.5,4.9)); ax.axis("off"); ax.set_xlim(-2.4,7.2); ax.set_ylim(-3.1,1.9)
cols=["category","amount","returned"]
rows=[["Electronics",180,"False"],["Apparel",45,"True"],["Electronics",220,"False"],["Beauty",30,"False"]]
idx=["a101","a102","a103","a104"]
table(ax, cols, rows, x0=0, y0=0.6, cw=1.9, ch=0.6, idx=idx, hi_row=2)   # a103 highlighted
ax.text(2.5,1.55,"both select the SAME row — one by its name, one by its position",
        fontsize=11,color=INK_SOFT,ha="center")
# a103 row spans y -1.2..-0.6 (center -0.9). Point both arrows INTO it.
ax.annotate('df.loc["a103"]', xy=(-0.66,-0.9), xytext=(-2.2,-2.25), fontsize=12.5, color=TEAL,
            family="monospace", fontweight="bold", va="center",
            arrowprops=dict(arrowstyle="->",color=TEAL,lw=1.6))
ax.text(-2.2,-2.7,"by LABEL",fontsize=10.5,color=TEAL)
ax.annotate('df.iloc[2]', xy=(2.85,-0.9), xytext=(2.85,-2.25), fontsize=12.5, color=ROSE,
            family="monospace", fontweight="bold", ha="center",
            arrowprops=dict(arrowstyle="->",color=ROSE,lw=1.6))
ax.text(2.85,-2.7,"by POSITION (0-based)",fontsize=10.5,color=ROSE,ha="center")
ax.set_title("loc vs iloc: select by label or by position", loc="left", fontsize=14)
save(fig,"s_pd_loc_iloc.png")
print("fixed s_pd_loc_iloc")
