import numpy as np, matplotlib.pyplot as plt
from vstyle import *
np.random.seed(3)

# 3.1 EDA first-hour checklist (graphviz)
dot('''
 D [label="A new dataset lands", fillcolor="#e9ecf6", color="#c7cee0"];
 S [label="1. Shape & types\\n.shape  .dtypes  .head()", fillcolor="#eef1fd", color="#cdd7fb"];
 M [label="2. Missingness & duplicates\\n.isna().sum()  .duplicated()", fillcolor="#eef1fd", color="#cdd7fb"];
 U [label="3. Univariate\\none variable at a time:\\ndistributions & outliers", fillcolor="#e3f5f3", color="#bfe7e3"];
 B [label="4. Bivariate\\nrelationships between\\npairs of variables", fillcolor="#e3f5f3", color="#bfe7e3"];
 H [label="5. Form hypotheses\\nquestions worth testing", fillcolor="#e6f5ec", color="#bfe0c8"];
 D -> S -> M -> U -> B -> H;
 H -> U [label=" dig deeper", style=dashed, constraint=false, color="#b6bccb"];
''', "s_eda_workflow.png", rd="TB", rs="0.34", ns="0.4")

# 3.2 chart chooser (graphviz)
dot('''
 q [label="What is your question\\nabout the data?", shape=diamond, style="filled", fillcolor="#e9ecf6", color="#c7cee0"];
 dist [label="DISTRIBUTION\\nof one variable?", shape=box, style="rounded,filled", fillcolor="#e3f5f3", color="#bfe7e3"];
 comp [label="COMPARISON\\nacross groups?", shape=box, style="rounded,filled", fillcolor="#e3f5f3", color="#bfe7e3"];
 rel  [label="RELATIONSHIP\\nbetween two numbers?", shape=box, style="rounded,filled", fillcolor="#e3f5f3", color="#bfe7e3"];
 trend[label="TREND\\nover time?", shape=box, style="rounded,filled", fillcolor="#e3f5f3", color="#bfe7e3"];
 comp2[label="COMPOSITION\\nparts of a whole?", shape=box, style="rounded,filled", fillcolor="#e3f5f3", color="#bfe7e3"];
 h [label="histogram\\n(boxplot for outliers)", fillcolor="#eef1fd", color="#cdd7fb"];
 b [label="bar chart\\n(boxplots to compare spread)", fillcolor="#eef1fd", color="#cdd7fb"];
 sc[label="scatter plot", fillcolor="#eef1fd", color="#cdd7fb"];
 ln[label="line chart", fillcolor="#eef1fd", color="#cdd7fb"];
 st[label="stacked / grouped bar\\n(avoid pie)", fillcolor="#fbf3e0", color="#ecd9ad"];
 q -> dist; q -> comp; q -> rel; q -> trend; q -> comp2;
 dist -> h; comp -> b; rel -> sc; trend -> ln; comp2 -> st;
''', "s_eda_chooser.png", rd="TB", rs="0.5", ns="0.3")

# 3.2 gallery of chart types
fig, ax = plt.subplots(2,3, figsize=(11.5,6.4))
# histogram
v=np.random.lognormal(3.6,0.5,2000); ax[0,0].hist(v,bins=40,color=INDIGO_BG,edgecolor=INDIGO,lw=.4)
ax[0,0].set_title("Histogram",color=INDIGO_DK); ax[0,0].set_xlabel("distribution of one variable"); ax[0,0].set_yticks([]); despine(ax[0,0],left=False)
# bar
cats=["Elec","Home","App","Beauty","Sport"]; vals=[399,118,125,47,113]
ax[0,1].bar(cats,vals,color=TEAL); ax[0,1].set_title("Bar chart",color=TEAL); ax[0,1].set_xlabel("comparison across groups"); despine(ax[0,1])
# scatter
x=np.random.normal(0,1,150); y=0.7*x+np.random.normal(0,0.6,150)
ax[0,2].scatter(x,y,s=12,color=AMBER,alpha=.6,edgecolors="none"); ax[0,2].set_title("Scatter plot",color=AMBER); ax[0,2].set_xlabel("relationship between two numbers"); ax[0,2].set_xticks([]); ax[0,2].set_yticks([]); despine(ax[0,2])
# line
m=np.arange(1,13); rev=[48,46,53,55,63,49,54,59,70,73,115,121]
ax[1,0].plot(m,rev,color=ROSE,lw=2.2,marker="o",ms=4); ax[1,0].set_title("Line chart",color=ROSE); ax[1,0].set_xlabel("trend over time (months)"); ax[1,0].set_yticks([]); despine(ax[1,0],left=False)
# boxplot
data=[np.random.normal(m_,8,200) for m_ in (40,55,62)]
bp=ax[1,1].boxplot(data,patch_artist=True,labels=["A","B","C"])
for b_ in bp['boxes']: b_.set(facecolor=GREEN_BG,edgecolor=GREEN)
for med in bp['medians']: med.set(color=GREEN,lw=2)
ax[1,1].set_title("Boxplot",color=GREEN); ax[1,1].set_xlabel("spread & outliers by group"); despine(ax[1,1])
# note cell
ax[1,2].axis("off")
ax[1,2].text(0.5,0.55,"Pick the chart that\nanswers your QUESTION,\nnot the one that\nlooks fanciest.",ha="center",va="center",fontsize=12.5,color=INK,fontweight="bold")
ax[1,2].text(0.5,0.12,"(decision tree above)",ha="center",fontsize=10,color=INK_FAINT,style="italic")
fig.suptitle("Five charts that answer five kinds of question",fontsize=14,fontweight="bold",y=1.0,color=INK)
save(fig,"s_eda_gallery.png")

# 3.2 pie vs bar
fig, ax = plt.subplots(1,2, figsize=(10.5,4.4))
labels=["A","B","C","D","E"]; sizes=[23,21,20,19,17]; cols=[INDIGO,TEAL,AMBER,ROSE,GREEN]
ax[0].pie(sizes,labels=labels,colors=[c for c in cols],autopct="%d%%",startangle=90,
          wedgeprops=dict(edgecolor="white",linewidth=1.5),textprops=dict(fontsize=10))
ax[0].set_title("Pie: which slice is biggest?",color=ROSE,fontsize=12.5)
order=np.argsort(sizes)[::-1]
ax[1].bar([labels[i] for i in order],[sizes[i] for i in order],color=TEAL)
ax[1].set_title("Bar: instantly obvious (and sorted)",color=TEAL,fontsize=12.5)
ax[1].set_ylabel("share (%)"); despine(ax[1])
fig.suptitle("Why bars beat pies: humans compare lengths far better than angles",
    fontsize=13.5,fontweight="bold",y=1.02,color=INK)
save(fig,"s_eda_pie.png")
print("BATCH H DONE")
