# -*- coding: utf-8 -*-
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from vstyle import save, despine, INDIGO, INDIGO_BG, TEAL, TEAL_BG, AMBER, AMBER_BG, ROSE, ROSE_BG, GREEN, GREEN_BG, INK, INK_SOFT, INK_FAINT
IMG="/sessions/zen-pensive-thompson/mnt/data-science-academy/assets/img"

# 10.1 — confusion matrix (spam example)
TP,FN,FP,TN = 80,20,10,890
fig,ax=plt.subplots(figsize=(6.6,5.4))
cells=[((0,1),TP,"True Positive",GREEN,GREEN_BG),
       ((1,1),FP,"False Positive\n(Type I)",ROSE,ROSE_BG),
       ((0,0),FN,"False Negative\n(Type II)",AMBER,AMBER_BG),
       ((1,0),TN,"True Negative",TEAL,TEAL_BG)]
for (cx,cy),val,lab,col,bg in cells:
    ax.add_patch(FancyBboxPatch((cx+0.03,cy+0.03),0.94,0.94,boxstyle="round,pad=0.0,rounding_size=0.04",
                 mutation_aspect=1,fc=bg,ec=col,lw=2.2))
    ax.text(cx+0.5,cy+0.62,str(val),ha="center",va="center",fontsize=27,fontweight="bold",color=INK)
    ax.text(cx+0.5,cy+0.28,lab,ha="center",va="center",fontsize=10.5,color=col,fontweight="bold")
ax.set_xlim(0,2); ax.set_ylim(0,2); ax.set_aspect("equal"); ax.axis("off")
ax.text(0.5,2.14,"Predicted:\nSpam",ha="center",fontsize=11,color=INK_SOFT,fontweight="bold")
ax.text(1.5,2.14,"Predicted:\nNot spam",ha="center",fontsize=11,color=INK_SOFT,fontweight="bold")
ax.text(-0.16,1.5,"Actual:\nSpam",ha="center",va="center",fontsize=11,color=INK_SOFT,fontweight="bold",rotation=90)
ax.text(-0.16,0.5,"Actual:\nNot spam",ha="center",va="center",fontsize=11,color=INK_SOFT,fontweight="bold",rotation=90)
ax.text(1.0,-0.28,"Precision = TP/(TP+FP) = 80/90 = 0.89     Recall = TP/(TP+FN) = 80/100 = 0.80",
        ha="center",fontsize=10.6,color=INK)
ax.text(1.0,-0.52,"Accuracy = 970/1000 = 0.97  —  high, yet it misses 20% of spam!",
        ha="center",fontsize=10.6,color=ROSE,fontweight="bold")
ax.set_title("The confusion matrix: accuracy can hide what matters",fontsize=13,pad=30)
save(fig,"s_eval_confusion.png")

# 10.2 — ROC curve
fig,ax=plt.subplots(figsize=(6.0,5.4))
fpr=np.linspace(0,1,200)
tpr=fpr**0.35                        # a good classifier: concave, above diagonal
ax.plot([0,1],[0,1],"--",color=INK_FAINT,lw=1.8,label="Random (AUC = 0.5)")
ax.plot(fpr,tpr,color=INDIGO,lw=3,label="Model (AUC ≈ 0.85)")
ax.fill_between(fpr,fpr,tpr,color=INDIGO,alpha=0.10)
ax.scatter([0.18],[0.18**0.35],s=90,color=ROSE,zorder=5)
ax.annotate("one threshold\n= one point",(0.18,0.18**0.35),xytext=(0.34,0.52),fontsize=10,color=ROSE,
            arrowprops=dict(arrowstyle="->",color=ROSE,lw=1.6))
ax.set_xlabel("False Positive Rate"); ax.set_ylabel("True Positive Rate (Recall)")
ax.set_xlim(0,1); ax.set_ylim(0,1.02)
ax.set_title("ROC curve: every threshold, one picture",fontsize=13)
ax.legend(loc="lower right",frameon=False,fontsize=10.5); despine(ax)
save(fig,"s_eval_roc.png")

# 10.3 — calibration / reliability diagram
fig,ax=plt.subplots(figsize=(6.0,5.4))
x=np.linspace(0,1,11)
over = np.clip(x + 0.18*np.sin(np.pi*x), 0, 1)*0  # placeholder
# overconfident model: predicts extreme probs; actual freq less extreme -> S under/over diagonal
pred=np.linspace(0.05,0.95,10)
actual=np.clip(0.5 + (pred-0.5)*0.55, 0, 1)   # regression toward 0.5 -> overconfident
ax.plot([0,1],[0,1],"--",color=INK_FAINT,lw=1.8,label="Perfectly calibrated")
ax.plot(pred,actual,"-o",color=ROSE,lw=2.6,ms=7,label="Overconfident model")
ax.fill_between(pred,actual,pred,color=ROSE,alpha=0.08)
ax.annotate("says 90% sure,\nright only ~72%",(0.9,0.72),xytext=(0.42,0.86),fontsize=9.8,color=ROSE,
            arrowprops=dict(arrowstyle="->",color=ROSE,lw=1.5))
ax.set_xlabel("Predicted probability"); ax.set_ylabel("Actual frequency")
ax.set_xlim(0,1); ax.set_ylim(0,1)
ax.set_title("Calibration: does 'p = 0.9' happen 90% of the time?",fontsize=12.5)
ax.legend(loc="lower right",frameon=False,fontsize=10.5); despine(ax)
save(fig,"s_eval_calibration.png")
print("done")
