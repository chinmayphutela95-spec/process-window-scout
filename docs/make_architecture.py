"""Draws the Process Window Scout architecture as built (docs/architecture.png). Run from docs/."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

AGENT, CODE, HUMAN, MEM, TOT = "#DCE8F7", "#EEEEEE", "#FDE2C4", "#DFF1E1", "#EADFF5"
EDGE = {AGENT: "#2F5D9E", CODE: "#777777", HUMAN: "#B86A12", MEM: "#2E7D3A", TOT: "#6A3FA0"}
RED, GREY, DARK, GREEN, PURPLE = "#B03030", "#666666", "#333333", "#2E7D3A", "#6A3FA0"

fig, ax = plt.subplots(figsize=(12.5, 7.8), dpi=200)
ax.set_xlim(-1, 103); ax.set_ylim(-9, 68); ax.axis("off")


def box(x, y, w, h, color, title, body="", fs=8.2, lw=1.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2",
                                fc=color, ec=EDGE[color], lw=lw))
    ax.text(x + w / 2, y + h - 1.9, title, ha="center", va="center", fontsize=fs + 0.8, weight="bold")
    if body:
        ax.text(x + w / 2, y + (h - 3.2) / 2, body, ha="center", va="center", fontsize=fs - 1.2, linespacing=1.3)


def arrow(p1, p2, label="", rad=0.0, ls="-", color=DARK, lx=0, ly=0, fs=6.8, lw=1.2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=11, lw=lw, color=color, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))
    if label:
        ax.text((p1[0] + p2[0]) / 2 + lx, (p1[1] + p2[1]) / 2 + ly, label, ha="center", va="center", fontsize=fs,
                style="italic", color=color, bbox=dict(fc="white", ec="none", pad=0.4))


def path(points, color=DARK, ls="-", lw=1.2):
    xs, ys = zip(*points[:-1])
    ax.plot(xs, ys, color=color, ls=ls, lw=lw)
    arrow(points[-2], points[-1], color=color, ls=ls, lw=lw)


ax.text(39, 66, "Process Window Scout: the system as built (one LangGraph state graph)", ha="center", fontsize=12.5,
        weight="bold")

# Row 1: request to checked records
R1 = 50
box(0, R1, 11, 12, HUMAN, "Engineer", "request:\nalloy, layer,\nmachine, target")
box(14, R1, 14, 12, CODE, "Clarify", "asks back if the\ngrade, layer or machine\npower is missing")
box(31, R1, 14, 12, CODE, "Coordinator", "picks the tables and\ntext of 23 CC BY\n316L papers")
for d in (1.6, 0.8):
    ax.add_patch(FancyBboxPatch((48 + d, R1 + d), 14, 12, boxstyle="round,pad=0.3,rounding_size=1.2", fc=AGENT,
                                ec=EDGE[AGENT], lw=1.0))
box(48, R1, 14, 12, AGENT, "Readers", "GLM-5.2, in parallel,\none per table or text,\nrecords with citations")
box(66, R1, 13, 12, CODE, "Checker", "17 code checks:\nvalue in its passage,\nrow, column, sample,\ncondition, units", fs=7.9)
arrow((11.4, R1 + 6), (13.6, R1 + 6))
arrow((28.4, R1 + 6), (30.6, R1 + 6))
arrow((45.4, R1 + 6), (47.6, R1 + 6), "Send", ly=1.4)
arrow((62.6, R1 + 8.5), (65.6, R1 + 8.5))
arrow((65.6, R1 + 2.5), (62.6, R1 + 2.5), color=RED)
ax.text(63.6, R1 - 3.0, "fail: one retry with the\nreason, then \"not verified\"", ha="center", fontsize=6.3,
        style="italic", color=RED)

# Row 2: gates, conflicts and the Analyst
R2 = 25
box(0, R2, 14, 12, CODE, "Clarity gate", "sets aside papers\nwith approximate\ndensities")
box(17, R2, 15, 12, CODE, "Widen", "under 10 records:\none search at the\nneighbouring layers,\nmarked adjacent", fs=7.9)
box(35, R2, 15, 12, CODE, "Find conflicts", "comparable pairs\nacross papers,\nat most 3")
box(54, R2 - 3, 25, 16, TOT, "Analyst (Tree of Thought)", "")
ax.text(66.5, R2 + 9.2, "only when code finds a conflict", ha="center", fontsize=6.6, color=PURPLE)
box(55.5, R2 + 1.6, 10, 5.4, AGENT, "Generator", "", fs=7.2)
box(67.5, R2 + 1.6, 10, 5.4, AGENT, "Critic", "", fs=7.2)
arrow((65.9, R2 + 4.3), (67.1, R2 + 4.3), color=PURPLE, ls=":")
ax.text(66.5, R2 - 1.0, "GLM-5.2, beam 2, depth 2, outcome band\nand evidence tier scored by code",
        ha="center", fontsize=6.3, style="italic", color=PURPLE)
path([(72.5, R1 - 0.4), (72.5, R1 - 6.8), (7, R1 - 6.8), (7, R2 + 12.4)])
ax.text(40, R1 - 6.8, "all records checked", ha="center", va="center", fontsize=6.6, style="italic", color=DARK,
        bbox=dict(fc="white", ec="none", pad=0.4))
arrow((14.4, R2 + 6), (16.6, R2 + 6))
arrow((32.4, R2 + 6), (34.6, R2 + 6))
arrow((50.4, R2 + 6), (53.6, R2 + 6), "conflict", ly=1.4)

# Row 3: window, answer, approval
R3 = -1
box(0, R3, 24, 13, CODE, "Recommend", "windows per density method from\nverified as-built records, power\nlimits, evidence line per window,\nthin-evidence flag", fs=7.9)
box(28, R3, 18, 13, AGENT, "Writer", "GLM-5.2, a short answer,\nevery number and paper\nchecked by code,\ncode template as fallback", fs=7.9)
box(50, R3, 19, 13, HUMAN, "Approval (interrupt)", "the graph pauses,\napprove, or reject\nwith a reason,\nlimits remembered", fs=7.9)
path([(42.5, R2 - 0.4), (42.5, R2 - 5), (12, R2 - 5), (12, R3 + 13.4)])
ax.text(27, R2 - 5, "no conflict", ha="center", va="center", fontsize=6.6, style="italic", color=DARK,
        bbox=dict(fc="white", ec="none", pad=0.4))
path([(66.5, R2 - 3.4), (66.5, R2 - 8.5), (18, R2 - 8.5), (18, R3 + 13.4)], color=PURPLE)
ax.text(54, R2 - 8.5, "explanations", ha="center", va="center", fontsize=6.6, style="italic", color=PURPLE,
        bbox=dict(fc="white", ec="none", pad=0.4))
arrow((24.4, R3 + 6.5), (27.6, R3 + 6.5))
arrow((46.4, R3 + 6.5), (49.6, R3 + 6.5))
path([(69.4, R3 + 4), (75, R3 + 4), (75, R3 - 3.8), (-0.5, R3 - 3.8), (-0.5, R1 + 6), (-0.1, R1 + 6)], color=GREY,
     ls="--")
ax.text(37, R3 - 3.8, "decision, and power limits stored for the next run", ha="center", va="center", fontsize=6.6,
        style="italic", color=GREY, bbox=dict(fc="white", ec="none", pad=0.4))

# Side panel
X = 84
box(X, 48, 17, 15, MEM, "State and memory", "evidence table in the\ngraph state, saved after\nevery step (SQLite\ncheckpointer), machine\nlimits (SqliteStore)", fs=7.6)
box(X, 30, 17, 14, MEM, "Observability", "every model call traced:\nprompt, reasoning,\ntokens, time, and a\nSQLite cache that\nreplays known answers", fs=7.6)
box(X, 13, 17, 13, CODE, "Tools (code only)", "energy_density,\nmelt_pool_band,\nconsensus_lookup,\nsearch_passages", fs=7.6)
box(X, -2, 17, 12, CODE, "Front end", "Streamlit app runs\nthe notebook's\ncore cells", fs=7.6)

# Legend
items = [(AGENT, "model agent (GLM-5.2)"), (CODE, "code, no model"), (HUMAN, "engineer"), (MEM, "memory and tracing"),
         (TOT, "Tree of Thought")]
for i, (c, txt) in enumerate(items):
    x0 = 0 + i * 17.5
    ax.add_patch(FancyBboxPatch((x0, -8.6), 2.6, 1.8, boxstyle="round,pad=0.1", fc=c, ec=EDGE[c], lw=1))
    ax.text(x0 + 3.4, -7.7, txt, fontsize=7.2, va="center")

plt.savefig("architecture.png", bbox_inches="tight", facecolor="white")
print("saved architecture.png")
