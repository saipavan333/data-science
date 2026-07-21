# -*- coding: utf-8 -*-
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch
from vstyle import save, despine, INDIGO, INDIGO_BG, TEAL, AMBER, ROSE, GREEN, INK, INK_SOFT, INK_FAINT
IMG="/sessions/zen-pensive-thompson/mnt/data-science-academy/assets/img"

# 12.1 — the Pyramid Principle (answer first)
fig,ax=plt.subplots(figsize=(7.6,5.2))
# three horizontal tiers of a triangle
apex=(5,4.6); bl=(1.2,0.5); br=(8.8,0.5)
def yx(y):
    # x extent of triangle at height y (0..4.6)
    t=(y-0.5)/(4.6-0.5)
    left=bl[0]+(apex[0]-bl[0])*t; right=br[0]+(apex[0]-br[0])*t
    return left,right
# tier boundaries
y0,y1,y2,y3=0.5,1.9,3.2,4.6
def tier(ya,yb,color):
    la,ra=yx(ya); lb,rb=yx(yb)
    ax.add_patch(Polygon([(la,ya),(ra,ya),(rb,yb),(lb,yb)],closed=True,fc=color,ec="white",lw=2.5))
tier(y2,y3,INDIGO); tier(y1,y2,"#6f79e6"); tier(y0,y1,"#aab2f2")
ax.text(5,3.85,"THE ANSWER",ha="center",va="center",fontsize=13,color="white",fontweight="bold")
ax.text(5,3.5,"(recommendation, first)",ha="center",va="center",fontsize=9.5,color="white")
ax.text(5,2.55,"3 key supporting arguments",ha="center",va="center",fontsize=12,color="white",fontweight="bold")
ax.text(5,1.15,"data · analysis · detail (the evidence)",ha="center",va="center",fontsize=11,color=INK,fontweight="bold")
ax.annotate("executives start\nhere — lead with\nthe conclusion",(5,4.3),xytext=(8.7,4.2),fontsize=10.5,
            color=INK_SOFT,ha="center",arrowprops=dict(arrowstyle="->",color=INK_SOFT,lw=1.6))
ax.annotate("dive down only\nif they ask",(2.0,1.0),xytext=(0.2,2.4),fontsize=10.5,color=INK_SOFT,ha="center",
            arrowprops=dict(arrowstyle="->",color=INK_SOFT,lw=1.5))
ax.set_xlim(-0.2,10.2); ax.set_ylim(0,5.1); ax.axis("off")
ax.set_title("The Pyramid Principle: answer first, evidence underneath",fontsize=13.5)
save(fig,"s_comm_pyramid.png")

# 12.3 — declutter: cluttered vs clean
regions=["North","South","East","West","Central"]
vals=[22,25,19,41,23]
fig,axs=plt.subplots(1,2,figsize=(11,4.6))
# LEFT: cluttered
cols=[ROSE,AMBER,GREEN,INDIGO,TEAL]
axs[0].bar(regions,vals,color=cols,edgecolor="black",linewidth=1.2)
axs[0].grid(True,axis="both",color="#bbb",linewidth=1.0)
axs[0].set_title("Q3 GROWTH BY REGION (%) — all regions shown!!!",fontsize=11,fontweight="bold")
axs[0].set_ylabel("Growth %"); axs[0].set_xlabel("Region")
axs[0].legend(regions,title="Region",loc="upper left",fontsize=8)
for i,v in enumerate(vals): axs[0].text(i,v+0.6,str(v),ha="center",fontsize=9)
axs[0].tick_params(axis="x",rotation=45)
axs[0].text(2,-14,"cluttered: rainbow, gridlines,\nredundant legend, no message",ha="center",color=ROSE,fontsize=10,fontweight="bold")
# RIGHT: clean, one message
clean_cols=["#d3d7e0"]*5; clean_cols[3]=INDIGO
axs[1].bar(regions,vals,color=clean_cols)
axs[1].set_title("West drove Q3 growth — nearly 2× any other region",fontsize=12,fontweight="bold",color=INK,loc="left")
axs[1].text(3,41+0.8,"41%",ha="center",fontsize=12,fontweight="bold",color=INDIGO)
despine(axs[1],left=False,bottom=True); axs[1].set_yticks([])
axs[1].text(2,-9.5,"clean: one highlighted bar, direct label,\ntakeaway as the title",ha="center",color=GREEN,fontsize=10,fontweight="bold")
axs[1].set_ylim(0,46)
fig.suptitle("Same data — decoration vs. communication",fontsize=13.5,fontweight="bold",y=1.03)
save(fig,"s_comm_declutter.png")
print("done")
