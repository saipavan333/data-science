# -*- coding: utf-8 -*-
import numpy as np, matplotlib.pyplot as plt, subprocess, os
from vstyle import dot, save, despine, GV, INDIGO, TEAL, AMBER, ROSE, GREEN, INK, INK_SOFT, INK_FAINT
from PIL import Image
IMG="/sessions/zen-pensive-thompson/mnt/data-science-academy/assets/img"

def dot_tmp(body,path,rd="TB",rs="0.6",ns="0.4",nc="#cdd7fb",nf="#eef1fd"):
    src=GV.format(rd=rd,rs=rs,ns=ns,nc=nc,nf=nf,body=body)
    p=subprocess.run(["dot","-Tpng","-Gdpi=170"],input=src.encode(),capture_output=True)
    if p.returncode!=0: raise RuntimeError(p.stderr.decode())
    open(path,"wb").write(p.stdout)

# 7.1 — confounding triangle
dot(r'''
 Z [label="Z  —  confounder\n(e.g. hot weather)", fillcolor="#fbf3e0", color="#e9cf9a"];
 X [label="X  —  treatment\n(ice-cream sales)", fillcolor="#eef1fd", color="#cdd7fb"];
 Y [label="Y  —  outcome\n(drownings)", fillcolor="#e6f5ec", color="#b0dcc0"];
 Z -> X [color="#c2305a", penwidth=2.0];
 Z -> Y [color="#c2305a", penwidth=2.0];
 X -> Y [label="  real effect? ", style=dashed, color="#79808f", fontcolor="#79808f"];
 {rank=same; X; Y;}
''', "s_causal_confound.png", rd="TB", rs="0.9", ns="1.4")

# 7.2 — three DAG archetypes -> /tmp, then stitch
dot_tmp(r'''
 label="FORK  (confounder)"; labelloc="t"; fontname="Helvetica-Bold"; fontsize=15; fontcolor="#2a3da6";
 Z [label="Z", fillcolor="#fbf3e0", color="#e9cf9a"];
 X [label="X", fillcolor="#eef1fd", color="#cdd7fb"]; Y [label="Y", fillcolor="#e6f5ec", color="#b0dcc0"];
 Z -> X [color="#c2305a", penwidth=1.9]; Z -> Y [color="#c2305a", penwidth=1.9]; {rank=same; X; Y;}
''', "/tmp/_dag_fork.png", rd="TB", rs="0.8", ns="1.1")
dot_tmp(r'''
 label="CHAIN  (mediator)"; labelloc="t"; fontname="Helvetica-Bold"; fontsize=15; fontcolor="#2a3da6";
 X [label="X", fillcolor="#eef1fd", color="#cdd7fb"]; M [label="M", fillcolor="#fbf3e0", color="#e9cf9a"];
 Y [label="Y", fillcolor="#e6f5ec", color="#b0dcc0"];
 X -> M [color="#0e8f8a", penwidth=1.9]; M -> Y [color="#0e8f8a", penwidth=1.9];
''', "/tmp/_dag_chain.png", rd="LR", rs="0.7", ns="0.5")
dot_tmp(r'''
 label="COLLIDER  (common effect)"; labelloc="t"; fontname="Helvetica-Bold"; fontsize=15; fontcolor="#2a3da6";
 X [label="X", fillcolor="#eef1fd", color="#cdd7fb"]; Y [label="Y", fillcolor="#e6f5ec", color="#b0dcc0"];
 C [label="C", fillcolor="#fce8ee", color="#eab6c6"];
 X -> C [color="#79808f", penwidth=1.9]; Y -> C [color="#79808f", penwidth=1.9]; {rank=same; X; Y;}
''', "/tmp/_dag_collider.png", rd="TB", rs="0.8", ns="1.1")
ims=[Image.open(p).convert("RGB") for p in ["/tmp/_dag_fork.png","/tmp/_dag_chain.png","/tmp/_dag_collider.png"]]
H=max(i.height for i in ims); gap=46; W=sum(i.width for i in ims)+gap*(len(ims)-1)
canvas=Image.new("RGB",(W,H),"white"); x=0
for i in ims:
    canvas.paste(i,(x,(H-i.height)//2)); x+=i.width+gap
canvas.save(os.path.join(IMG,"s_causal_dags.png")); print("diagram -> s_causal_dags.png")

# 7.3 — difference-in-differences
fig,ax=plt.subplots(figsize=(7.6,4.7))
t=[0,1]; ctrl=[40,46]; treat=[52,66]; cf=[52,58]
ax.plot(t,ctrl,'-o',color=INK_SOFT,lw=2.4,ms=8,label="Control (never treated)")
ax.plot(t,treat,'-o',color=INDIGO,lw=2.8,ms=9,label="Treatment (observed)")
ax.plot(t,cf,'--o',color=ROSE,lw=2.2,ms=7,mfc="white",label="Treatment counterfactual\n(if it had followed control's trend)")
ax.annotate("", xy=(1,66), xytext=(1,58), arrowprops=dict(arrowstyle="<->",color=GREEN,lw=2.4))
ax.text(1.03,62,"causal effect\n(diff-in-diff)",color=GREEN,fontweight="bold",fontsize=12,va="center")
ax.axvline(0.5,color=INK_FAINT,ls=":",lw=1.4)
ax.text(0.5,32.2,"intervention",color=INK_FAINT,fontsize=10.5,ha="center",style="italic")
ax.set_xticks([0,1]); ax.set_xticklabels(["Before","After"])
ax.set_ylim(30,72); ax.set_xlim(-0.12,1.62)
ax.set_ylabel("Outcome metric"); ax.set_title("Difference-in-differences: the counterfactual is the control's trend")
ax.legend(loc="upper left",frameon=False,fontsize=10.2); despine(ax)
save(fig,"s_causal_did.png")
for p in ["/tmp/_dag_fork.png","/tmp/_dag_chain.png","/tmp/_dag_collider.png"]:
    try: os.remove(p)
    except OSError: pass
print("done")
