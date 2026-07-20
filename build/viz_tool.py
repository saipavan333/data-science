# -*- coding: utf-8 -*-
from vstyle import dot, INDIGO_BG, TEAL_BG, AMBER_BG, ROSE_BG, GREEN_BG

# 3.2 Git — the three areas + remote (the core mental model)
dot(r'''
 wd  [label="Working\nDirectory\n(your edits)", fillcolor="#fbf3e0", color="#e9cf9a"];
 st  [label="Staging\nArea\n(staged)", fillcolor="#e3f5f3", color="#a9ddd8"];
 lr  [label="Local\nRepository\n(history)", fillcolor="#eef1fd", color="#cdd7fb"];
 rm  [label="Remote\n(GitHub)", fillcolor="#e6f5ec", color="#b0dcc0"];
 wd -> st [label="git add"];
 st -> lr [label="git commit"];
 lr -> rm [label="git push"];
 rm -> lr [label="git pull", constraint=false, style=dashed];
''', "s_tool_git.png", rd="LR", rs="0.7", ns="0.5")

# 3.3 Environments — isolation prevents version conflicts
dot(r'''
 subgraph cluster_a {label="Project A  (env: ds-a)"; style="rounded,filled"; fillcolor="#eef1fd"; color="#cdd7fb"; fontname="Helvetica"; fontsize=12; fontcolor="#2a3da6";
   a1 [label="pandas 1.5", fillcolor="white", color="#cdd7fb"];
   a2 [label="numpy 1.24", fillcolor="white", color="#cdd7fb"];
   a3 [label="python 3.10", fillcolor="white", color="#cdd7fb"];
 }
 subgraph cluster_b {label="Project B  (env: ds-b)"; style="rounded,filled"; fillcolor="#e3f5f3"; color="#a9ddd8"; fontname="Helvetica"; fontsize=12; fontcolor="#0e8f8a";
   b1 [label="pandas 2.2", fillcolor="white", color="#a9ddd8"];
   b2 [label="numpy 2.0", fillcolor="white", color="#a9ddd8"];
   b3 [label="python 3.12", fillcolor="white", color="#a9ddd8"];
 }
''', "s_tool_env.png", rd="LR", rs="0.5", ns="0.3")
print("done")
