import os, subprocess
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
IMG = "/sessions/zen-pensive-thompson/mnt/data-science-academy/assets/img"
os.makedirs(IMG, exist_ok=True)
INDIGO, INDIGO_DK, INDIGO_BG = "#3b53d6", "#2a3da6", "#eef1fd"
TEAL, TEAL_BG = "#0e8f8a", "#e3f5f3"
AMBER, AMBER_BG = "#b7791f", "#fbf3e0"
ROSE, ROSE_BG = "#c2305a", "#fce8ee"
GREEN, GREEN_BG = "#1f8a4c", "#e6f5ec"
INK, INK_SOFT, INK_FAINT = "#1f2430", "#4a5160", "#79808f"
plt.rcParams.update({"figure.facecolor":"white","axes.facecolor":"white","font.size":12.5,
 "font.family":"DejaVu Sans","axes.edgecolor":INK_SOFT,"axes.linewidth":1.0,"axes.titlesize":14,
 "axes.titleweight":"bold","axes.titlecolor":INK,"axes.labelcolor":INK_SOFT,"xtick.color":INK_SOFT,
 "ytick.color":INK_SOFT,"axes.grid":True,"grid.color":"#edeff3","grid.linewidth":1,
 "axes.axisbelow":True,"figure.dpi":150,"savefig.dpi":150,"savefig.bbox":"tight"})
def despine(ax,left=True,bottom=True):
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(left); ax.spines["bottom"].set_visible(bottom)
def save(fig,name):
    fig.savefig(os.path.join(IMG,name),facecolor="white"); plt.close(fig); print("chart ->",name)
GV='''digraph G {{ graph [bgcolor="white",fontname="Helvetica",rankdir={rd},ranksep={rs},nodesep={ns},pad=0.25];
 node [shape=box,style="rounded,filled",fontname="Helvetica",fontsize=12,color="{nc}",fillcolor="{nf}",
 fontcolor="#1f2430",margin="0.20,0.12",penwidth=1.3];
 edge [color="#8a93a6",penwidth=1.4,arrowsize=0.85,fontname="Helvetica",fontsize=10.5,fontcolor="#4a5160"]; {body} }}'''
def dot(body,name,rd="TB",rs="0.55",ns="0.4",nc="#cdd7fb",nf=INDIGO_BG):
    src=GV.format(rd=rd,rs=rs,ns=ns,nc=nc,nf=nf,body=body)
    p=subprocess.run(["dot","-Tpng","-Gdpi=170"],input=src.encode(),capture_output=True)
    if p.returncode!=0: raise RuntimeError(p.stderr.decode())
    open(os.path.join(IMG,name),"wb").write(p.stdout); print("diagram ->",name)
