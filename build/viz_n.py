import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from vstyle import *

def cells(ax, vals, x0, y0, w=0.92, h=0.92, gap=0.12, fc=INDIGO_BG, ec=INDIGO, fs=15):
    for i,v in enumerate(vals):
        x=x0+i*(w+gap)
        ax.add_patch(Rectangle((x,y0),w,h,facecolor=fc,edgecolor=ec,lw=1.6))
        ax.text(x+w/2,y0+h/2,str(v),ha="center",va="center",fontsize=fs,color=INK,fontweight="bold")
    return

# 2.2 try/except flow (graphviz)
dot('''
 t [label="try:\\n  run risky code\\n(e.g. int(user_input))", fillcolor="#eef1fd", color="#cdd7fb"];
 q [label="did an error\\nhappen?", shape=diamond, style="filled", fillcolor="#fbf3e0", color="#ecd9ad"];
 ok [label="else:\\n  it worked — continue", fillcolor="#e6f5ec", color="#bfe0c8"];
 ex [label="except ValueError:\\n  handle it gracefully\\n(don't crash)", fillcolor="#fce8ee", color="#e7b9c6"];
 fin [label="finally:\\n  always runs\\n(clean up)", fillcolor="#e3f5f3", color="#bfe7e3"];
 done [label="program keeps going", fillcolor="#e9ecf6", color="#c7cee0"];
 t -> q;
 q -> ok [label="no"];
 q -> ex [label="yes"];
 ok -> fin; ex -> fin; fin -> done;
''', "s_py_tryexcept.png", rd="TB", rs="0.42", ns="0.45")

# 2.3 string anatomy
fig,ax=plt.subplots(figsize=(11,4.6)); ax.axis("off"); ax.set_xlim(0,12.5); ax.set_ylim(-1.2,3.2)
word="DataSci"
cells(ax, list(word), 0.4, 1.6)
for i in range(len(word)):
    x=0.4+i*(0.92+0.12)+0.46
    ax.text(x,1.4,str(i),ha="center",va="top",fontsize=11,color=INK_FAINT)
    ax.text(x,2.7,str(i-len(word)),ha="center",va="bottom",fontsize=10,color=AMBER)
ax.text(0.4,3.0,"negative index (from the end)",fontsize=10,color=AMBER)
ax.text(0.4,1.15,"position (from 0)",fontsize=10,color=INK_FAINT)
ax.text(0.4,0.5,'word[0:4]  ->  "Data"      word[-3:]  ->  "Sci"      word[::-1]  ->  "icSataD"',
        fontsize=11.5,color=INK,family="monospace")
ax.text(0.4,-0.2,'Handy methods:  .upper()  .lower()  .strip()  .replace("a","@")  .split(",")  .startswith("Data")',
        fontsize=10.5,color=INK_SOFT,family="monospace")
ax.set_title("A string is a sequence of characters — index and slice it like a list",loc="left",fontsize=13.5)
save(fig,"s_py_string_anatomy.png")

# 2.4 datetime parts
fig,ax=plt.subplots(figsize=(11,4.8)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,6)
ax.add_patch(FancyBboxPatch((3.6,4.4),4.8,1.0,boxstyle="round,pad=0.04",facecolor=INDIGO_BG,edgecolor=INDIGO,lw=1.8))
ax.text(6.0,4.9,"2025-03-14  09:30",ha="center",va="center",fontsize=15,color=INK,family="monospace",fontweight="bold")
ax.text(6.0,5.6,"one Timestamp",ha="center",fontsize=10.5,color=INDIGO_DK)
parts=[(".year",2025,1.3,2.7,TEAL),(".month",3,3.5,2.4,TEAL),(".day",14,5.7,2.2,TEAL),
       (".hour",9,7.9,2.4,AMBER),(".day_name()","'Friday'",10.1,2.7,AMBER),(".quarter","Q1",6.0,1.0,ROSE)]
for attr,val,x,y,c in parts:
    ax.add_patch(FancyBboxPatch((x-1.0,y-0.32),2.0,0.64,boxstyle="round,pad=0.02",facecolor="white",edgecolor=c,lw=1.4))
    ax.text(x,y+0.08,attr,ha="center",fontsize=10.5,color=c,family="monospace",fontweight="bold")
    ax.text(x,y-0.16,str(val),ha="center",fontsize=10,color=INK)
    ax.annotate("",xy=(x,y+0.34),xytext=(6.0,4.4),arrowprops=dict(arrowstyle="->",color="#c7cee0",lw=1.2))
ax.set_title("The .dt accessor: pull calendar parts out of a date column",loc="left",fontsize=13.5)
save(fig,"s_py_datetime_parts.png")

# 2.6 numpy axis
fig,ax=plt.subplots(figsize=(9.5,5.2)); ax.axis("off"); ax.set_xlim(-1.5,7); ax.set_ylim(-2.2,4.2)
M=np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
for r in range(4):
    for c in range(3):
        ax.add_patch(Rectangle((c,3-r),0.9,0.9,facecolor=INDIGO_BG,edgecolor=INDIGO,lw=1.3))
        ax.text(c+0.45,3-r+0.45,str(M[r,c]),ha="center",va="center",fontsize=12,color=INK)
ax.annotate("",xy=(1.4,-0.4),xytext=(1.4,3.9),arrowprops=dict(arrowstyle="->",color=ROSE,lw=2.2))
ax.text(-0.2,-1.2,"axis=0  (down the columns)",color=ROSE,fontsize=11,fontweight="bold")
colsum=M.sum(axis=0)
for c in range(3):
    ax.text(c+0.45,-0.7,str(colsum[c]),ha="center",color=ROSE,fontsize=12,fontweight="bold")
ax.annotate("",xy=(4.3,2.55),xytext=(-0.3,2.55),arrowprops=dict(arrowstyle="->",color=TEAL,lw=2.2))
ax.text(3.7,3.6,"axis=1\n(across rows)",color=TEAL,fontsize=11,fontweight="bold",ha="center")
rowsum=M.sum(axis=1)
for r in range(4):
    ax.text(4.5,3-r+0.45,str(rowsum[r]),ha="center",va="center",color=TEAL,fontsize=12,fontweight="bold")
ax.set_title("NumPy axis: the dimension that DISAPPEARS when you aggregate",loc="left",fontsize=13)
save(fig,"s_np_axis.png")

# 2.8 data I/O sources
dot('''
 csv [label="CSV", fillcolor="#eef1fd", color="#cdd7fb"];
 xls [label="Excel", fillcolor="#eef1fd", color="#cdd7fb"];
 jsn [label="JSON", fillcolor="#eef1fd", color="#cdd7fb"];
 sql [label="SQL database", fillcolor="#eef1fd", color="#cdd7fb"];
 api [label="web API", fillcolor="#eef1fd", color="#cdd7fb"];
 read [label="pd.read_csv / read_excel\\nread_json / read_sql", shape=box, style="rounded,filled", fillcolor="#fbf3e0", color="#ecd9ad"];
 df [label="DataFrame\\n(work here)", fillcolor="#e3f5f3", color="#bfe7e3"];
 save [label="df.to_csv / to_parquet\\nto_excel", shape=box, style="rounded,filled", fillcolor="#fbf3e0", color="#ecd9ad"];
 out [label="saved file\\n(share / reuse)", fillcolor="#e6f5ec", color="#bfe0c8"];
 csv -> read; xls -> read; jsn -> read; sql -> read; api -> read;
 read -> df -> save -> out;
 {rank=same; csv; xls; jsn; sql; api;}
''', "s_io_sources.png", rd="LR", rs="0.55", ns="0.18")
print("BATCH N DONE")
