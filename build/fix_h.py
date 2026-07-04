import numpy as np, matplotlib.pyplot as plt
from vstyle import *
np.random.seed(3)
fig, ax = plt.subplots(2,3, figsize=(11.5,6.6))
v=np.random.lognormal(3.6,0.5,2000); ax[0,0].hist(v,bins=40,color=INDIGO_BG,edgecolor=INDIGO,lw=.4)
ax[0,0].set_title("Histogram",color=INDIGO_DK); ax[0,0].set_xlabel("one variable's distribution"); ax[0,0].set_yticks([]); despine(ax[0,0],left=False)
cats=["Elec","Home","App","Bty","Spt"]; vals=[399,118,125,47,113]
ax[0,1].bar(cats,vals,color=TEAL); ax[0,1].set_title("Bar chart",color=TEAL); ax[0,1].set_xlabel("compare across groups"); despine(ax[0,1])
x=np.random.normal(0,1,150); y=0.7*x+np.random.normal(0,0.6,150)
ax[0,2].scatter(x,y,s=12,color=AMBER,alpha=.6,edgecolors="none"); ax[0,2].set_title("Scatter plot",color=AMBER); ax[0,2].set_xlabel("two numbers' relationship"); ax[0,2].set_xticks([]); ax[0,2].set_yticks([]); despine(ax[0,2])
m=np.arange(1,13); rev=[48,46,53,55,63,49,54,59,70,73,115,121]
ax[1,0].plot(m,rev,color=ROSE,lw=2.2,marker="o",ms=4); ax[1,0].set_title("Line chart",color=ROSE); ax[1,0].set_xlabel("trend over months"); ax[1,0].set_yticks([]); despine(ax[1,0],left=False)
data=[np.random.normal(m_,8,200) for m_ in (40,55,62)]
bp=ax[1,1].boxplot(data,patch_artist=True)
ax[1,1].set_xticks([1,2,3]); ax[1,1].set_xticklabels(["A","B","C"])
for b_ in bp['boxes']: b_.set(facecolor=GREEN_BG,edgecolor=GREEN)
for med in bp['medians']: med.set(color=GREEN,lw=2)
ax[1,1].set_title("Boxplot",color=GREEN); ax[1,1].set_xlabel("spread & outliers by group"); despine(ax[1,1])
ax[1,2].axis("off")
ax[1,2].text(0.5,0.6,"Pick the chart that\nanswers your QUESTION,\nnot the one that\nlooks fanciest.",ha="center",va="center",fontsize=12.5,color=INK,fontweight="bold")
fig.suptitle("Five charts that answer five kinds of question",fontsize=14,fontweight="bold",color=INK)
fig.tight_layout(rect=[0,0,1,0.95])
save(fig,"s_eda_gallery.png")
print("FIX H DONE")
