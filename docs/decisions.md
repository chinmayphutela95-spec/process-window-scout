# Decisions log

Newest at the bottom. Each entry: date · decision · why. The model-choice log at the end feeds the
"why these models" section of the final report.

## Design decisions
- **2026-09-29** · Project type = Research Assistant. · Matches background (AM) and the brief's
  "use tools to generate new data"; Personal Assistant judged too simple.
- **2026-10-09** · Topic = Process Window Scout (literature → process window for PBF-LB). · Low build
  effort, public data, strong domain fit; a closed-loop "self-driving print lab" was dropped (needs
  proprietary build data and printer time; the course allows public data only).
- **2026-10-09** · Paper retrieval automated via OpenAlex API (open-access + licence filter). · Tested:
  7,208 OA hits for 316L LPBF parameters; many CC-BY with PDF links. No manual collection.
- **2026-10-09** · Added analytical melt-pool tool so the agent generates new data. · Brief requires
  "generate new data".
- **2026-10-09** · Differentiate from Prof. Barati Farimani's two 2026 papers by cross-checking
  literature evidence against physics and other papers. · His group does literature mining and
  physics process maps separately.
- **2026-10-09** · Physics = weak evidence only: Rosenthal/Eagar–Tsai at absorptivity 0.3/0.5/0.7 → band;
  outlier only if consensus AND whole band disagree. · Analytical melt-pool models are not accurate
  enough to verify papers on their own.
- **2026-10-09** · Scope cut for learning: no regression fit, no DOE proposals, no gap detection;
  15–20 papers; start with ONE ReAct agent, split into Reader/Checker only in the multi-agent week.
- **2026-10-09** · Local models only (Ollama). · No paid API budget; the course expects free models;
  keeps data on the local machine.
- **2026-10-16** · Git repository = this folder only (code, docs, own checkpoint write-ups). · Course
  materials (transcripts, slides, lab notebooks, brief) are not ours to publish and stay outside the repo.

- **2026-10-17** · Tools exposed through MCP using the standalone `fastmcp` package (`from fastmcp import
  FastMCP`) on top of mcp 2.x. · Course instructor recommends always using MCP; the environment now has
  mcp 2.3 / fastmcp 4.1, and the old `mcp.server.fastmcp` import no longer exists in mcp 2.x.

- **2026-10-18** · Checkpoint 2.1 design refinements. · Responding to Checkpoint 1.1 feedback and Module 2:
  - Clarification step before searching (grade, machine, layer thickness): "stainless steel" may mean
    316L, 304L or 17-4PH, and a wrong grade spoils every later step.
  - Conflict check: normalise → compare conditions (grade and powder, layer thickness, power, speed first;
    then hatch, spot, machine, density method, heat treatment) → if different, label as different regimes;
    if comparable, weigh consensus, physics band and reporting quality → confidence with a reason.
  - Engineer feedback stored long-term as constraints (filters), corrections (down-weight records) and
    decisions with reasons (new ranking criteria, worked examples).
  - Prompt-only baseline to be run next to the agent in the final notebook (fabricated-citation failure).

## Model-choice log
| Date | Role | Candidates | Result | Choice |
|---|---|---|---|---|
| 2026-10-09 | (plan) Extractor / Analyst | Qwen3-8B Q4 | not yet tested | first candidate |
| 2026-10-09 | (plan) Checker | different family ~4B (e.g. Gemma) vs Qwen3-8B self-check; Prof's AdditiveLLM2-OA | not yet tested | — |
| 2026-10-09 | (plan) Embeddings | Qwen3-Embedding-0.6B, bge-m3 | not yet tested | — |

Constraint: 8 GB VRAM → ~4-bit quantised models ≤ ~8B; usable context ~8–16k tokens; one large model
loaded at a time (agents share it with different prompts).
