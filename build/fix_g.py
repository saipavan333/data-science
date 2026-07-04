import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from vstyle import *
KW="#a050c0"; STR="#1f8a4c"; NUM="#c2305a"; NAME=INK; BI="#0e7c8a"

def code_line(ax, tokens, x0, y, charw=0.205, fs=15.5):
    x=x0
    for txt,col in tokens:
        ax.text(x,y,txt,ha="left",va="center",family="monospace",fontsize=fs,color=col)
        x+=len(txt)*charw
def brow(ax, y, token, tcol, role):
    ax.text(0.7,y,token,family="monospace",fontsize=12.5,color=tcol,va="center",fontweight="bold")
    ax.text(4.5,y,"→",fontsize=12,color=INK_FAINT,va="center",ha="center")
    ax.text(4.9,y,role,fontsize=11.5,color=INK_SOFT,va="center")

# ---------- for loop ----------
fig,ax=plt.subplots(figsize=(11,5.8)); ax.axis("off"); ax.set_xlim(0,12.2); ax.set_ylim(0,7.4)
ax.add_patch(FancyBboxPatch((0.45,6.0),7.4,1.15,boxstyle="round,pad=0.05",facecolor="#1d2330",edgecolor="#2a3142",lw=1.2))
code_line(ax,[("for ",("#c792ea")),("n ",("#e7ebf3")),("in ",("#c792ea")),("[10, 20, 30]",("#f78c6c")),(":",("#e7ebf3"))],0.75,6.85,fs=15)
code_line(ax,[("    ",("#e7ebf3")),("print",("#82aaff")),("(n * 2)",("#e7ebf3"))],0.75,6.3,fs=15)
ax.text(0.5,5.6,"Each part, explained:",fontsize=11.5,color=INK,fontweight="bold")
brow(ax,5.15,"for ... in","#a050c0","keywords that begin the loop")
brow(ax,4.7,"n","#3b53d6","the loop variable — holds each item in turn")
brow(ax,4.25,"[10, 20, 30]","#c2305a","the list of values to loop over")
brow(ax,3.8,": + indent","#4a5160","the body — runs once for every value")
ax.add_patch(FancyBboxPatch((0.45,0.25),11.3,2.95,boxstyle="round,pad=0.05",facecolor="#f7f8fa",edgecolor="#e0e3ea",lw=1.2))
ax.text(0.8,2.85,"What actually happens — the body runs three times:",fontsize=11,color=INK,fontweight="bold")
for i,(r,nv,expr,out) in enumerate([("Round 1","n = 10","print(10 * 2)","20"),
        ("Round 2","n = 20","print(20 * 2)","40"),("Round 3","n = 30","print(30 * 2)","60")]):
    y=2.25-i*0.6
    ax.text(0.9,y,r,fontsize=10.5,color=INDIGO_DK,fontweight="bold")
    ax.text(2.6,y,nv,fontsize=10.5,color=INK,family="monospace")
    ax.text(4.5,y,"→  "+expr,fontsize=10.5,color=INK_SOFT,family="monospace")
    ax.text(8.8,y,"→  prints "+out,fontsize=10.5,color=STR,family="monospace")
ax.set_title("Anatomy of a for loop: do something once for each item", loc="left", fontsize=14, pad=10)
save(fig,"s_py_forloop.png")

# ---------- function ----------
fig,ax=plt.subplots(figsize=(11,5.4)); ax.axis("off"); ax.set_xlim(0,12.2); ax.set_ylim(0,7.0)
ax.add_patch(FancyBboxPatch((0.45,5.55),8.6,1.15,boxstyle="round,pad=0.05",facecolor="#1d2330",edgecolor="#2a3142",lw=1.2))
code_line(ax,[("def ",("#c792ea")),("to_celsius",("#82aaff")),("(f)",("#e7ebf3")),(":",("#e7ebf3"))],0.75,6.4,fs=15)
code_line(ax,[("    ",("#e7ebf3")),("return ",("#c792ea")),("(f - 32) * 5 / 9",("#f78c6c"))],0.75,5.85,fs=15)
ax.text(0.5,5.15,"Each part, explained:",fontsize=11.5,color=INK,fontweight="bold")
brow(ax,4.7,"def","#a050c0","defines a new, reusable function")
brow(ax,4.25,"to_celsius","#0e7c8a","its name — how you call it later")
brow(ax,3.8,"(f)","#4a5160","parameter: the input it receives")
brow(ax,3.35,"return","#a050c0","sends a value back out to the caller")
y=1.5
ax.add_patch(FancyBboxPatch((0.8,y-0.4),2.0,0.8,boxstyle="round,pad=0.03",facecolor=AMBER_BG,edgecolor=AMBER,lw=1.5))
ax.text(1.8,y,"98.6",ha="center",va="center",fontsize=13,color=INK,family="monospace")
ax.text(1.8,y+0.62,"input",ha="center",fontsize=10,color=AMBER)
ax.annotate("",xy=(4.5,y),xytext=(2.85,y),arrowprops=dict(arrowstyle="->",color=INK_FAINT,lw=1.6))
ax.add_patch(FancyBboxPatch((4.6,y-0.45),3.3,0.9,boxstyle="round,pad=0.03",facecolor=INDIGO_BG,edgecolor=INDIGO,lw=1.6))
ax.text(6.25,y,"to_celsius(98.6)",ha="center",va="center",fontsize=12,color=INK,family="monospace")
ax.text(6.25,y+0.66,"the function runs",ha="center",fontsize=10,color=INDIGO_DK)
ax.annotate("",xy=(9.6,y),xytext=(7.95,y),arrowprops=dict(arrowstyle="->",color=INK_FAINT,lw=1.6))
ax.add_patch(FancyBboxPatch((9.7,y-0.4),2.0,0.8,boxstyle="round,pad=0.03",facecolor=GREEN_BG,edgecolor=GREEN,lw=1.5))
ax.text(10.7,y,"37.0",ha="center",va="center",fontsize=13,color=INK,family="monospace")
ax.text(10.7,y+0.62,"returned output",ha="center",fontsize=10,color=GREEN)
ax.set_title("Anatomy of a function: package reusable logic, feed it input, get output back", loc="left", fontsize=13.5, pad=10)
save(fig,"s_py_func.png")
print("FIX G DONE")
