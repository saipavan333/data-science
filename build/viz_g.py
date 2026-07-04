import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from vstyle import *
KW="#a050c0"; STR="#1f8a4c"; NUM="#c2305a"; NAME=INK; BI="#0e7c8a"

def code_line(ax, tokens, x0, y, charw=0.205, fs=15.5):
    x=x0; centers={}
    for key,txt,col in tokens:
        ax.text(x,y,txt,ha="left",va="center",family="monospace",fontsize=fs,color=col)
        centers[key]=x+len(txt)*charw/2.0
        x+=len(txt)*charw
    return centers,x

# ---------- s_py_forloop ----------
fig,ax=plt.subplots(figsize=(11,5.2)); ax.axis("off"); ax.set_xlim(0,12.5); ax.set_ylim(-0.4,6)
c1,_=code_line(ax,[("for","for ",KW),("var","n ",NAME),("in","in ",KW),
                   ("seq","[10, 20, 30]",NUM),("colon",":",NAME)], 0.5, 5.2)
c2,_=code_line(ax,[("ind","    ",NAME),("p","print",BI),("rest","(n * 2)",NAME)], 0.5, 4.55)
# annotations
ax.annotate("keywords that\nstart the loop", xy=(c1["for"],5.45), xytext=(0.7,6.0),
            fontsize=10, color=KW, ha="center", arrowprops=dict(arrowstyle="->",color=KW,lw=1.2))
ax.annotate("loop variable:\ntakes each value in turn", xy=(c1["var"],4.95), xytext=(2.0,3.7),
            fontsize=10, color=INK_SOFT, ha="center", arrowprops=dict(arrowstyle="->",color=INK_FAINT,lw=1.2))
ax.annotate("the sequence\nto loop over", xy=(c1["seq"],5.45), xytext=(6.4,6.0),
            fontsize=10, color=NUM, ha="center", arrowprops=dict(arrowstyle="->",color=NUM,lw=1.2))
ax.annotate("colon + indented line\n= the loop body\n(runs once per value)", xy=(c2["p"],4.3),
            xytext=(8.7,3.7), fontsize=10, color=INK_SOFT, ha="center",
            arrowprops=dict(arrowstyle="->",color=INK_FAINT,lw=1.2))
# iteration trace
ax.add_patch(FancyBboxPatch((0.5,0.2),11.4,2.7,boxstyle="round,pad=0.05",facecolor="#f7f8fa",edgecolor="#e0e3ea",lw=1.2))
ax.text(0.8,2.6,"What actually happens — the loop runs its body three times:",fontsize=11,color=INK,fontweight="bold")
rounds=[("Round 1","n = 10","print(10 * 2)","20"),("Round 2","n = 20","print(20 * 2)","40"),
        ("Round 3","n = 30","print(30 * 2)","60")]
for i,(r,nv,expr,out) in enumerate(rounds):
    y=2.0-i*0.62
    ax.text(0.9,y,r,fontsize=10.5,color=INDIGO_DK,fontweight="bold")
    ax.text(2.5,y,nv,fontsize=10.5,color=INK,family="monospace")
    ax.text(4.3,y,"→  "+expr,fontsize=10.5,color=INK_SOFT,family="monospace")
    ax.text(8.6,y,"→  prints "+out,fontsize=10.5,color=STR,family="monospace")
ax.set_title("Anatomy of a for loop: do something once for each item", loc="left", fontsize=14)
save(fig,"s_py_forloop.png")

# ---------- s_py_ifelse (graphviz) ----------
dot('''
 s [label="temperature?", shape=box, style="rounded,filled", fillcolor="#eef1fd", color="#cdd7fb"];
 q1 [label="temp >= 30 ?", shape=diamond, style="filled", fillcolor="#fbf3e0", color="#ecd9ad"];
 q2 [label="temp >= 15 ?", shape=diamond, style="filled", fillcolor="#fbf3e0", color="#ecd9ad"];
 hot  [label="say 'Hot'", fillcolor="#fce8ee", color="#e7b9c6"];
 mild [label="say 'Mild'", fillcolor="#e6f5ec", color="#bfe0c8"];
 cold [label="say 'Cold'", fillcolor="#e3f5f3", color="#bfe7e3"];
 s -> q1;
 q1 -> hot [label="True  (if)"];
 q1 -> q2  [label="False (elif)"];
 q2 -> mild [label="True"];
 q2 -> cold [label="False (else)"];
''', "s_py_ifelse.png", rd="TB", rs="0.5", ns="0.5")

# ---------- s_py_func ----------
fig,ax=plt.subplots(figsize=(11,4.8)); ax.axis("off"); ax.set_xlim(0,12.5); ax.set_ylim(-0.5,5.2)
c1,_=code_line(ax,[("def","def ",KW),("name","to_celsius",BI),("param","(f)",NAME),("colon",":",NAME)],0.5,4.6)
c2,_=code_line(ax,[("ind","    ",NAME),("ret","return ",KW),("expr","(f - 32) * 5 / 9",NUM)],0.5,3.95)
ax.annotate("def = define\na function", xy=(c1["def"],4.85), xytext=(0.8,5.15),
            fontsize=10, color=KW, ha="center", arrowprops=dict(arrowstyle="->",color=KW,lw=1.2))
ax.annotate("its name\n(how you call it)", xy=(c1["name"],4.85), xytext=(3.3,5.15),
            fontsize=10, color=BI, ha="center", arrowprops=dict(arrowstyle="->",color=BI,lw=1.2))
ax.annotate("parameter:\nthe input it needs", xy=(c1["param"],4.35), xytext=(6.6,4.95),
            fontsize=10, color=INK_SOFT, ha="center", arrowprops=dict(arrowstyle="->",color=INK_FAINT,lw=1.2))
ax.annotate("return: send a\nvalue back out", xy=(c2["ret"],3.7), xytext=(3.0,3.0),
            fontsize=10, color=KW, ha="center", arrowprops=dict(arrowstyle="->",color=KW,lw=1.2))
# input -> box -> output
y=1.4
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
ax.set_title("Anatomy of a function: name some reusable logic, feed it input, get output back", loc="left", fontsize=13.5)
save(fig,"s_py_func.png")
print("VIZ G DONE")
