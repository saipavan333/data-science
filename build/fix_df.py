import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from vstyle import *
def table(ax, cols, rows, x0, y0, cw=1.9, ch=0.6, idx=None, hi_col=None):
    for j,c in enumerate(cols):
        fc=AMBER_BG if hi_col==j else "#f0f2f8"
        ax.add_patch(Rectangle((x0+j*cw,y0),cw,ch,facecolor=fc,edgecolor="#c7cee0",lw=1.3))
        ax.text(x0+j*cw+cw/2,y0+ch/2,c,ha="center",va="center",fontsize=11.5,fontweight="bold",color=INK_SOFT)
    for i,row in enumerate(rows):
        yy=y0-(i+1)*ch
        if idx is not None:
            ax.add_patch(Rectangle((x0-cw*0.7,yy),cw*0.7,ch,facecolor="#f7f8fa",edgecolor="#d8dce3",lw=1.2))
            ax.text(x0-cw*0.35,yy+ch/2,str(idx[i]),ha="center",va="center",fontsize=11,color=INK_SOFT,fontweight="bold")
        for j,val in enumerate(row):
            fc=AMBER_BG if hi_col==j else "white"
            ax.add_patch(Rectangle((x0+j*cw,yy),cw,ch,facecolor=fc,edgecolor="#e0e3ea",lw=1.1))
            ax.text(x0+j*cw+cw/2,yy+ch/2,str(val),ha="center",va="center",fontsize=11,color=INK)
    if idx is not None:
        ax.text(x0-cw*0.35,y0+ch/2,"index",ha="center",va="center",fontsize=9.5,color=INK_FAINT,style="italic")

fig,ax=plt.subplots(figsize=(10.5,4.8)); ax.axis("off"); ax.set_xlim(-2.3,7.3); ax.set_ylim(-3.0,1.8)
cols=["category","amount","returned"]
rows=[["Electronics",180,"False"],["Apparel",45,"True"],["Electronics",220,"False"],["Beauty",30,"False"]]
table(ax, cols, rows, x0=0, y0=0.6, cw=1.9, ch=0.6, idx=[0,1,2,3], hi_col=1)
# columns annotation (top, pointing to header)
ax.annotate("columns (labeled)", xy=(2.85,1.2), xytext=(4.1,1.62), fontsize=11, color=INK_SOFT,
            ha="center", arrowprops=dict(arrowstyle="->",color=INK_FAINT,lw=1.2))
# index annotation (left, pointing to index column)
ax.annotate("index\n(row labels)", xy=(-0.7,-0.6), xytext=(-2.15,-0.25), fontsize=11, color=TEAL,
            ha="center", va="center", arrowprops=dict(arrowstyle="->",color=TEAL,lw=1.3))
# one column = a Series: label centered in clear margin BELOW, arrow up to the amber column's bottom edge
ax.annotate("one column = a Series", xy=(2.85,-1.84), xytext=(2.85,-2.62), fontsize=11.5, color=AMBER,
            ha="center", fontweight="bold", arrowprops=dict(arrowstyle="->",color=AMBER,lw=1.5))
ax.set_title("Anatomy of a DataFrame: labeled columns, a row index, and Series inside",
             loc="left", fontsize=14)
save(fig,"s_pd_dataframe.png")
print("fixed s_pd_dataframe")
