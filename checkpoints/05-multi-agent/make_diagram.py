"""Draws the Checkpoint 5.1 multi-agent architecture diagram (architecture.png)."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

AGENT, TOOL, MEM, HUMAN, CODE, TOT = "#DCE8F7", "#FCE9D2", "#DFF1E1", "#ECECEC", "#F3F3F3", "#EADFF5"
EDGE = {AGENT: "#2F5D9E", TOOL: "#B86A12", MEM: "#2E7D3A", HUMAN: "#555555", CODE: "#777777", TOT: "#6A3FA0"}
RED, GREY, DARK, GREEN, PURPLE = "#B03030", "#666666", "#333333", "#2E7D3A", "#6A3FA0"

fig, ax = plt.subplots(figsize=(11, 6.6), dpi=200)
ax.set_xlim(-1, 100); ax.set_ylim(-5, 64); ax.axis("off")


def box(x, y, w, h, color, title, body="", fs=8.5, lw=1.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2",
                                fc=color, ec=EDGE[color], lw=lw))
    if body:
        ax.text(x + w / 2, y + h - 2.0, title, ha="center", va="center", fontsize=fs + 1, weight="bold")
        ax.text(x + w / 2, y + (h - 3.4) / 2, body, ha="center", va="center", fontsize=fs - 0.6,
                linespacing=1.3)
    elif title:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=fs + 1, weight="bold")


def arrow(p1, p2, label="", rad=0.0, style="-|>", ls="-", color=DARK, lx=0, ly=0, fs=7.2, lw=1.2):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=12, lw=lw, color=color,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))
    if label:
        ax.text((p1[0] + p2[0]) / 2 + lx, (p1[1] + p2[1]) / 2 + ly, label, ha="center", va="center",
                fontsize=fs, style="italic", color=color, bbox=dict(fc="white", ec="none", pad=0.5))


def note(x, y, text, color, fs=6.7, ha="center"):
    ax.text(x, y, text, ha=ha, va="center", fontsize=fs, style="italic", color=color,
            bbox=dict(fc="white", ec="none", pad=0.3))


ax.text(50, 63, "Process Window Scout: planned multi-agent design (LangGraph state graph)",
        ha="center", fontsize=12, weight="bold")

# Engineer and Coordinator
box(1, 47, 15, 11, HUMAN, "Engineer", "request, answers,\napproval")
box(22, 47, 30, 11, CODE, "Coordinator (code, no LLM)",
    "checks the request is complete,\nplans searches, routes work,\nenforces limits")
arrow((16.4, 54.5), (21.6, 54.5), "request", ly=1.5)
arrow((21.6, 50.0), (16.4, 50.0), "ask", ls="--", color=GREY, ly=-1.5)

# MCP tool server
box(58, 47, 40, 11, TOOL, "MCP tool server (fastmcp)",
    "search_passages, stated_conditions, energy_density,\nconsensus_lookup, melt_pool_band\n"
    "each agent gets only its own tools", fs=8)

# Readers (parallel stack)
for dx in (2.4, 1.2):
    box(3 + dx, 31 + dx, 18, 8.5, AGENT, "", "")
box(3, 31, 18, 8.5, AGENT, "Reader (one per paper)", "extracts power, speed, hatch,\nlayer, density, passage",
    fs=7.2)
note(12, 29.3, "parallel, max 3 at a time", EDGE[AGENT])
arrow((28, 46.6), (14, 42.4), "paper IDs (one-way)", lx=-5, ly=0.8)

# Checker under the Readers, with the two-way validation loop between them
box(3, 13, 18, 10, AGENT, "Checker", "code checks + judgement,\nsees record and passage,\nnot Reader reasoning",
    fs=7.6)
arrow((7, 23.4), (7, 28.2), color=RED, lw=1.4)
arrow((17, 28.2), (17, 23.4), color=RED, lw=1.4)
note(12, 25.8, "fail: reason,\none retry", RED, fs=6.5)

# Shared evidence table
box(29, 13, 27, 26.5, MEM, "Evidence table (shared state)",
    "one row per record:\nID, values, passage ID,\ncheck results, status,\nexplanation, evidence tier\n\n"
    "kept by a SQLite\ncheckpointer", fs=8)
arrow((21.4, 35), (28.6, 35), "write", color=GREEN, ly=1.6)
arrow((21.4, 18), (28.6, 18), style="<|-|>", color=GREEN)
note(25, 20.2, "read, mark", GREEN, fs=6.5)
arrow((42.5, 39.9), (42.5, 46.6), color=GREEN)
note(43.5, 43.3, "fewer than 10 verified records:\none wider search", GREEN, ha="left")

# Analyst with Tree of Thought
box(63, 16, 35, 21, TOT, "", lw=1.4)
ax.text(80.5, 34.6, "Analyst (Tree of Thought)", ha="center", va="center", fontsize=9.5, weight="bold")
ax.text(80.5, 31.6, "only for conflicts flagged by code, max 3 per run", ha="center", fontsize=6.8,
        color=PURPLE)
box(66, 21, 12, 6.5, AGENT, "Generator", "", fs=7.5)
box(83, 21, 12, 6.5, AGENT, "Critic", "", fs=7.5)
arrow((78.4, 25.4), (82.6, 25.4), color=PURPLE, ls=":", lw=1.4)
arrow((82.6, 23.1), (78.4, 23.1), color=PURPLE, ls=":", lw=1.4)
ax.text(80.5, 18.2, "up to 5 explanations, beam 2, depth 2", ha="center", fontsize=6.8,
        style="italic", color=PURPLE)
arrow((56.4, 31), (62.6, 31), "conflict", color=DARK, ly=1.5, fs=6.6)
arrow((62.6, 20), (56.4, 20), "explanation,\nconfidence", color=GREEN, ly=-2.6, fs=6.6)

# Recommendation and approval gate
box(29, 0, 27, 9.5, CODE, "Recommend window (code)", "from verified records only,\nwith citations", fs=7.8)
arrow((42.5, 12.6), (42.5, 9.9))
box(3, 0, 18, 9.5, HUMAN, "Approval interrupt", "graph pauses, engineer\napproves or corrects", fs=7.4)
arrow((28.6, 4.75), (21.4, 4.75))
ax.plot([2.6, 0.2, 0.2], [4.75, 4.75, 52.5], ls="--", lw=1.2, color=GREY)
arrow((0.2, 52.5), (0.7, 52.5), ls="--", color=GREY)
ax.text(0.2, 27, "decision", rotation=90, fontsize=6.7, style="italic", color=GREY, ha="center", va="center",
        bbox=dict(fc="white", ec="none", pad=0.4))

# Limits
box(63, 0, 35, 13, CODE, "Limits set by the Coordinator",
    "one retry per failed record, then \"not verified\"\none extra search round\n"
    "max 3 conflicts per run, max 3 Readers at a time\nanything unexpected goes to the engineer", fs=7.4)

# Legend
lx, ly = 3, -3.6
for i, (c, ls, txt) in enumerate([(DARK, "-", "one-way handoff"), (RED, "-", "two-way validation"),
                                   (PURPLE, ":", "brainstorming"), (GREEN, "-", "shared state read / write")]):
    x0 = lx + i * 25
    ax.plot([x0, x0 + 4], [ly, ly], color=c, ls=ls, lw=1.6)
    ax.text(x0 + 5, ly, txt, fontsize=7.4, va="center", color=c)

plt.savefig("architecture.png", bbox_inches="tight", facecolor="white")
print("saved architecture.png")
