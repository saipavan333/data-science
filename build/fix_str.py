import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from vstyle import *

def cells(ax, vals, x0, y0, w=0.92, h=0.92, gap=0.12, fc=INDIGO_BG, ec=INDIGO, fs=15):
    for i,v in enumerate(vals):
        x=x0+i*(w+gap)
        ax.add_patch(Rectangle((x,y0),w,h,facecolor=fc,edgecolor=ec,lw=1.6))
        ax.text(x+w/2,y0+h/2,str(v),ha="center",va="center",fontsize=fs,color=INK,fontweight="bold")

fig,ax=plt.subplots(figsize=(11,4.6)); ax.axis("off"); ax.set_xlim(0,12.5); ax.set_ylim(-1.2,3.2)
word="DataSci"
cells(ax, list(word), 0.4, 1.6)
for i in range(len(word)):
    x=0.4+i*(0.92+0.12)+0.46
    ax.text(x,1.38,str(i),ha="center",va="top",fontsize=11,color=INK_FAINT)
    ax.text(x,2.7,str(i-len(word)),ha="center",va="bottom",fontsize=10,color=AMBER)
ax.text(0.4,3.0,"negative index (from the end)",fontsize=10,color=AMBER)
# FIX: lower the caption and anchor its TOP so it clears the index digits above it
ax.text(0.4,1.02,"position (from 0)",fontsize=10,color=INK_FAINT,va="top")
ax.text(0.4,0.5,'word[0:4]  ->  "Data"      word[-3:]  ->  "Sci"      word[::-1]  ->  "icSataD"',
        fontsize=11.5,color=INK,family="monospace")
ax.text(0.4,-0.2,'Handy methods:  .upper()  .lower()  .strip()  .replace("a","@")  .split(",")  .startswith("Data")',
        fontsize=10.5,color=INK_SOFT,family="monospace")
ax.set_title("A string is a sequence of characters — index and slice it like a list",loc="left",fontsize=13.5)
save(fig,"s_py_string_anatomy.png")
print("STR FIX DONE")
