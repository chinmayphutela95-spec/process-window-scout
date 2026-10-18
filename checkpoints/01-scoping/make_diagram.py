"""Draws the Process Window Scout architecture diagram (architecture.png)."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

AGENT, TOOL, MEM, HUMAN, OUT, EXT = "#DCE8F7", "#FCE9D2", "#DFF1E1", "#ECECEC", "#EADFF5", "#F5F5F5"
EDGE = {AGENT: "#2F5D9E", TOOL: "#B86A12", MEM: "#2E7D3A", HUMAN: "#555555", OUT: "#6A3FA0", EXT: "#777777"}
RED, GREY = "#B03030", "#555555"

fig, ax = plt.subplots(figsize=(11, 6.6), dpi=200)
ax.set_xlim(0, 100); ax.set_ylim(0, 62); ax.axis("off")


def box(x, y, w, h, color, title, body="", fs=8.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2",
                                fc=color, ec=EDGE[color], lw=1.4))
    cy = y + h / 2
    if body:
        ax.text(x + w / 2, cy + h * 0.22, title, ha="center", va="center", fontsize=fs + 1, weight="bold")
        ax.text(x + w / 2, cy - h * 0.13, body, ha="center", va="center", fontsize=fs - 0.5, linespacing=1.25)
    else:
        ax.text(x + w / 2, cy, title, ha="center", va="center", fontsize=fs + 1, weight="bold")


def arrow(p1, p2, label="", rad=0.0, style="-|>", ls="-", color="#333333", lx=0, ly=0, fs=7.5):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=12, lw=1.2, color=color,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))
    if label:
        ax.text((p1[0] + p2[0]) / 2 + lx, (p1[1] + p2[1]) / 2 + ly, label, ha="center", va="center",
                fontsize=fs, style="italic", color=color, bbox=dict(fc="white", ec="none", pad=0.6))


# Row 1: human + orchestrator
box(3, 51, 20, 8, HUMAN, "Engineer (user)", "request · clarifications\n· final approval")
box(38, 51, 26, 8, AGENT, "Orchestrator", "plans the task · routes work\n· decides when to retry")
arrow((23.5, 56.5), (37.5, 56.5), "request")
arrow((37.5, 53), (23.5, 53), "clarify / approve", ls="--", color=GREY)

# Row 2: source + agents
box(2.5, 34, 12, 10, EXT, "OpenAlex", "open-access\npapers (PDF)")
box(19, 34, 20, 10, AGENT, "Reader", "search · parse (Docling)\nextract records + citations")
box(44, 34, 18, 10, AGENT, "Checker", "source check: re-reads\nthe cited passage")
box(67, 33, 30, 12, AGENT, "Plausibility reasoning", "outlier only if consensus AND whole\nphysics band disagree · explores\nexplanations (Tree of Thought)", fs=8)
arrow((14.8, 39), (18.7, 39))
arrow((39.3, 39), (43.7, 39))
arrow((62.3, 39), (66.7, 39), "verified", ly=1.9)
arrow((55, 50.7), (55, 44.3), "dispatches", lx=4.5)

# feedback loops
arrow((48, 44.3), (34, 44.3), "not in source → re-extract", rad=0.5, color=RED, ly=5.2)
arrow((74, 33.8), (27, 33.8), "too few comparable points → search again", rad=-0.18, color=RED, lx=-8, ly=-5.6)

# Row 3: tools (three signals) + report
box(62, 12, 37, 12, TOOL, "Tools (deterministic Python)",
    "units · energy density\nconsensus lookup (similar settings)\nmelt-pool model, absorptivity 0.3 to 0.7 → band", fs=8)
arrow((86, 33.6), (86, 24.4), style="<|-|>", color=EDGE[TOOL])
box(8, 12, 40, 12, OUT, "Report",
    "recommended process window\nsupporting evidence (cited)\noutliers + likely explanation + confidence", fs=8)
arrow((69, 32.6), (44, 24.4))

# approval path routed around the left edge
ax.plot([7.7, 0.8, 0.8], [18, 18, 55], ls="--", lw=1.2, color=GREY)
arrow((0.8, 55), (2.7, 55), ls="--", color=GREY)
ax.text(0.2, 30, "approval needed", rotation=90, fontsize=7.5, style="italic", color=GREY,
        ha="center", va="center", bbox=dict(fc="white", ec="none", pad=0.6))

# Row 4: memory
box(6, 2, 93, 7.5, MEM, "")
ax.text(8, 5.75, "Memory", fontsize=9.5, weight="bold", va="center")
ax.text(58, 5.75,
        "Vector DB (ChromaDB): paper chunks     |     Evidence DB (SQLite): cited data points"
        "     |     Run state (LangGraph)", fontsize=8, ha="center", va="center")

ax.text(50, 61.2, "Process Window Scout: initial agent architecture", ha="center", fontsize=12, weight="bold")
plt.savefig("architecture.png", bbox_inches="tight", facecolor="white")
print("saved architecture.png")
