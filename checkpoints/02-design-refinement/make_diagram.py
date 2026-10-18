"""Draws the Checkpoint 2.1 architecture diagram (architecture.png): ReAct loop, tools, memory."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

AGENT, TOOL, MEM, HUMAN, OUT, LOOP = "#DCE8F7", "#FCE9D2", "#DFF1E1", "#ECECEC", "#EADFF5", "#FFF6D6"
EDGE = {AGENT: "#2F5D9E", TOOL: "#B86A12", MEM: "#2E7D3A", HUMAN: "#555555", OUT: "#6A3FA0", LOOP: "#A08400"}
RED, GREY, DARK = "#B03030", "#555555", "#333333"

fig, ax = plt.subplots(figsize=(11, 6.8), dpi=200)
ax.set_xlim(0, 100); ax.set_ylim(-1, 64); ax.axis("off")


def box(x, y, w, h, color, title, body="", fs=8.5, lw=1.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2",
                                fc=color, ec=EDGE[color], lw=lw))
    if body:
        ax.text(x + w / 2, y + h - 2.0, title, ha="center", va="center", fontsize=fs + 1, weight="bold")
        ax.text(x + w / 2, y + (h - 3.2) / 2, body, ha="center", va="center", fontsize=fs - 0.5,
                linespacing=1.3)
    elif title:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=fs + 1, weight="bold")


def arrow(p1, p2, label="", rad=0.0, style="-|>", ls="-", color=DARK, lx=0, ly=0, fs=7.5):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=12, lw=1.2, color=color,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))
    if label:
        ax.text((p1[0] + p2[0]) / 2 + lx, (p1[1] + p2[1]) / 2 + ly, label, ha="center", va="center",
                fontsize=fs, style="italic", color=color, bbox=dict(fc="white", ec="none", pad=0.6))


ax.text(50, 63.2, "Process Window Scout: refined design with reasoning loop, tools and memory",
        ha="center", fontsize=12, weight="bold")

# Engineer + clarification
box(2, 50, 19, 10, HUMAN, "Engineer", "request · answers\nfeedback · approval")
box(26, 50, 22, 10, AGENT, "Step 0: Clarify", "grade? (316L / 304L / 17-4PH)\nmachine · layer thickness")
arrow((21.4, 56.5), (25.6, 56.5), "request", ly=1.6)
arrow((25.6, 52.5), (21.4, 52.5), "ask", ls="--", color=GREY, ly=-1.6)

# ReAct loop panel
box(2, 20, 62, 26, LOOP, "", lw=1.0)
ax.text(4, 21.8, "ReAct loop (steps capped per paper and per run)", fontsize=8.5, weight="bold",
        color=EDGE[LOOP], va="center")
box(5, 30, 16, 9, AGENT, "Thought", "what is known,\nwhat is missing")
box(25, 30, 16, 9, AGENT, "Action", "choose one\ntool call")
box(45, 30, 16, 9, AGENT, "Observation", "written by code,\nnever the model")
arrow((21.3, 34.5), (24.7, 34.5))
arrow((41.3, 34.5), (44.7, 34.5))
arrow((53, 29.7), (13, 29.7), "observation shapes the next thought", rad=-0.28, color=RED, lx=6, ly=-4.4)
arrow((37, 49.7), (13, 39.3), "clarified task", lx=-9, ly=0.5)

# Conflict resolution (inside loop panel, right)
box(66, 20, 32, 14, OUT, "Conflict resolution",
    "1 normalise units (tools)\n2 comparable? grade, powder, layer,\n   power, speed, method → else 'different regime'\n3 weigh: consensus · physics band · quality\n4 confidence + one-line reason", fs=7.6)
arrow((61.3, 33), (65.7, 30), "papers disagree", ly=2.4, fs=7)

# Tools
box(66, 38, 32, 22, TOOL, "Tools (deterministic Python)",
    "search_papers: retrieval\nfetch_and_parse · find_passage: grounding\n"
    "convert_units · energy_density: computation\nconsensus_lookup: many records\n"
    "melt_pool_band: new data (weak evidence)\nask_engineer: ambiguity", fs=7.8)
arrow((33, 39.3), (65.7, 46), "call", rad=-0.15, lx=4, ly=2)
arrow((65.7, 42), (55, 39.3), "result", rad=0.1, lx=1, ly=-1.4)

# Report
box(2, 6, 30, 11, OUT, "Report", "recommended window\ncited evidence\nexplained outliers + confidence", fs=7.8)
arrow((9, 20), (9, 17.9))
ax.plot([1, 1], [11.5, 51], ls="--", lw=1.2, color=GREY)
ax.plot([1.6, 1], [11.5, 11.5], ls="--", lw=1.2, color=GREY)
arrow((1, 51), (1.9, 51.5), ls="--", color=GREY)
ax.text(0.4, 33, "approve / correct", rotation=90, fontsize=7.2, style="italic", color=GREY,
        ha="center", va="center", bbox=dict(fc="white", ec="none", pad=0.5))

# Memory
box(36, 1.5, 28, 14, MEM, "Short-term memory",
    "working context: request + current\npassage + last few steps (8k to 16k tokens)\nrun summary: papers read,\nrecords kept / rejected", fs=7.6)
box(67, 1.5, 31, 14, MEM, "Long-term memory",
    "evidence store: verified data points\n+ source, page, conditions, confidence\nengineer feedback: constraints,\ncorrections, accept / reject + reason", fs=7.6)
arrow((50, 19.7), (50, 15.9), style="<|-|>", color=EDGE[MEM])
arrow((82, 19.7), (82, 15.9), style="<|-|>", color=EDGE[MEM])
ax.plot([17, 17, 70], [5.6, 0.3, 0.3], ls="--", lw=1.2, color=GREY)
arrow((70, 0.3), (70, 1.0), ls="--", color=GREY)
ax.text(44, 0.3, "engineer feedback stored", fontsize=7, style="italic", color=GREY, ha="center", va="center", bbox=dict(fc="white", ec="none", pad=0.5))

plt.savefig("architecture.png", bbox_inches="tight", facecolor="white")
print("saved architecture.png")
