"""Draws the Checkpoint 4.1 Tree of Thought diagram (tot_tree.png)."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

AGENT, TOOL, MEM, OUT, CODE, PRUNED = "#DCE8F7", "#FCE9D2", "#DFF1E1", "#EADFF5", "#FFF6D6", "#EFEFEF"
EDGE = {AGENT: "#2F5D9E", TOOL: "#B86A12", MEM: "#2E7D3A", OUT: "#6A3FA0", CODE: "#A08400", PRUNED: "#9A9A9A"}
GREY, DARK, RED = "#777777", "#333333", "#B03030"

fig, ax = plt.subplots(figsize=(11, 7), dpi=200)
ax.set_xlim(0, 100); ax.set_ylim(0, 66); ax.axis("off")


def box(x, y, w, h, color, title, body="", fs=8.2, ls="-", tcolor="black"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.0",
                                fc=color, ec=EDGE[color], lw=1.3, linestyle=ls))
    if body:
        ax.text(x + w / 2, y + h - 1.9, title, ha="center", va="center", fontsize=fs + 0.8, weight="bold", color=tcolor)
        ax.text(x + w / 2, y + (h - 3.0) / 2, body, ha="center", va="center", fontsize=fs - 0.6, linespacing=1.25,
                color=tcolor)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=fs + 0.8, weight="bold", color=tcolor)


def arrow(p1, p2, label="", color=DARK, ls="-", lx=0, ly=0, fs=7, rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=10, lw=1.1, color=color, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))
    if label:
        ax.text((p1[0] + p2[0]) / 2 + lx, (p1[1] + p2[1]) / 2 + ly, label, ha="center", va="center", fontsize=fs,
                style="italic", color=color, bbox=dict(fc="white", ec="none", pad=0.5))


ax.text(50, 65, "Process Window Scout: Tree of Thought for conflicting results (beam width 2, depth 2)",
        ha="center", fontsize=11.5, weight="bold")

# root and pre-checks
box(2, 50, 33, 11, AGENT, "Root: flagged conflict",
    "A: best 97.76% at 140 W, 100 mm/s, 30 µm\nB: up to 99.97% at 190 W, 700 to 800 mm/s, 30 µm\nboth cited, same layer thickness")
box(39, 50, 30, 11, CODE, "Code checks first (free)",
    "value found verbatim in its passage\nenergy density recomputed: 389 J/mm³ = table\nunits and stated conditions present")
arrow((35.4, 55.5), (38.6, 55.5))

# level 1: five explanations
ax.text(2, 46, "Level 1: generator proposes up to 5 explanations; critic scores each with one tool call",
        fontsize=8.3, weight="bold", color=EDGE[AGENT], zorder=5, bbox=dict(fc="white", ec="none", pad=1.5))
names = [("Over-melting /\nkeyhole porosity", AGENT, "kept"), ("Specimen size\n(2 x 2 x 5 mm)", AGENT, "kept"),
         ("Density method", PRUNED, "pruned"), ("Powder", PRUNED, "pruned"), ("Reporting error", PRUNED, "pruned")]
xs = [2, 21.5, 41, 60.5, 80]
for (name, col, state), x in zip(names, xs):
    box(x, 32, 17.5, 10, col, name, "", fs=7.6, ls="-" if state == "kept" else "--",
        tcolor="black" if state == "kept" else GREY)
    arrow((54, 49.7), (x + 8.75, 42.4), color=DARK if state == "kept" else GREY, ls="-" if state == "kept" else "--")
ax.text(80 + 8.75, 30.6, "pruned: energy density matches table", ha="center", fontsize=6.6, style="italic", color=RED)
ax.text(51.2 + 8.75, 30.6, "pruned: outside beam or score <= 0", ha="center", fontsize=6.6, style="italic", color=GREY)

# level 2 follow-ups
ax.text(2, 27.5, "Level 2: one targeted follow-up per kept branch (search inside one paper, or a calculation)",
        fontsize=8.3, weight="bold", color=EDGE[AGENT], zorder=5, bbox=dict(fc="white", ec="none", pad=1.5))
box(2, 16, 17.5, 8.5, TOOL, "melt_pool_band", "depth 101 to 170 µm vs\n52 to 81 µm (weak)", fs=7.4)
box(21.5, 16, 17.5, 8.5, TOOL, "search_passages", "specimen geometry and\ndensity method in A", fs=7.4)
arrow((10.75, 31.7), (10.75, 24.9)); arrow((30.25, 31.7), (30.25, 24.9))

# output
box(2, 2, 37, 10.5, OUT, "Output to the engineer",
    "both values kept, best-supported explanation,\nevidence quotes, confidence (high / medium / low)\nor 'unresolved' if no branch reaches 3 points")
arrow((10.75, 15.7), (16, 12.9)); arrow((30.25, 15.7), (25, 12.9))

# right panel: rubric + roles
box(44, 2, 54, 22.5, MEM, "", "")
ax.text(46, 22.3, "Roles and tools", fontsize=9, weight="bold", color=EDGE[MEM])
roles = [("Generator", "LangChain prompt, GLM-5.2, structured output"),
         ("Critic", "separate GLM-5.2 call + evidence tools over MCP"),
         ("Controller", "LangGraph: beam, thresholds, termination, approval"),
         ("State", "LangGraph state + SQLite checkpointer; MCP evidence store")]
for i, (r, t) in enumerate(roles):
    ax.text(46, 19 - i * 2.6, f"{r}:", fontsize=7.6, weight="bold")
    ax.text(56, 19 - i * 2.6, t, fontsize=7.4)
ax.text(46, 7.6, "Rubric (critic judges, code adds): text supports +3, code check agrees +2,", fontsize=7.2)
ax.text(46, 5.6, "consensus +2, physics band +1 (withheld out of range), contradicted -3,", fontsize=7.2)
ax.text(46, 3.6, "assumption only -2. Stop at >= 6 points with a lead >= 2, or at depth 2.", fontsize=7.2)

ax.text(50, 0.2, "Planned tree for the test case: which branches survive will be measured in the notebook, not assumed.",
        ha="center", fontsize=7, style="italic", color=GREY)
plt.savefig("tot_tree.png", bbox_inches="tight", facecolor="white")
print("saved tot_tree.png")
