from vstyle import *
dot('''
 users [label="All eligible users", fillcolor="#eef1fd", color="#cdd7fb"];
 rand  [label="Randomly assign\\neach user 50 / 50", shape=diamond, style="filled", fillcolor="#fbf3e0", color="#ecd9ad"];
 ctrl  [label="CONTROL (A)\\nsees the current version", fillcolor="#e9ecf6", color="#c7cee0"];
 treat [label="TREATMENT (B)\\nsees the new version", fillcolor="#eef1fd", color="#cdd7fb"];
 mp    [label="Measure the SAME\\nprimary metric for both", fillcolor="#e3f5f3", color="#bfe7e3"];
 mg    [label="Watch guardrail metrics\\n(latency, revenue, errors)", fillcolor="#fce8ee", color="#e7b9c6"];
 comp  [label="Compare: is B reliably\\nbetter, without breaking a guardrail?", fillcolor="#e6f5ec", color="#bfe0c8"];
 users -> rand;
 rand -> ctrl [label="50%"];
 rand -> treat [label="50%"];
 ctrl -> mp; treat -> mp;
 mp -> comp; mg -> comp;
 {rank=same; mp; mg;}
''', "s_ab_design.png", rd="TB", rs="0.5", ns="0.4")
print("saved s_ab_design.png")
