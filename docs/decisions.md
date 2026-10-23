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
- **2026-10-09** · Physics = weak evidence only: Rosenthal/Eagar-Tsai at absorptivity 0.3/0.5/0.7 → band;
  outlier only if consensus AND whole band disagree. · Analytical melt-pool models are not accurate
  enough to verify papers on their own.
- **2026-10-09** · Scope cut for learning: no regression fit, no DOE proposals, no gap detection;
  15 to 20 papers; start with ONE ReAct agent, split into Reader/Checker only in the multi-agent week.
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

- **2026-10-18** · Notebook-first build: the whole project lives in `notebooks/process_window_scout.ipynb`,
  one Part per milestone, with test cells after each piece instead of a `src/` package and pytest. · The
  final deliverable is a notebook run on this laptop; building and testing in the same place is easier to
  follow while learning. Cost: the notebook gets long, so Restart & Run All must stay green and slow steps
  cache to `data/`. The MCP server is the one file written out (`%%writefile`), since it runs as its own process.
- **2026-10-18** · Melt-pool tool = Rosenthal point source solved exactly with the Lambert W function
  (scipy), 316L properties averaged after Mills (2002): k 22 W/mK, rho 7800 kg/m3, cp 600 J/kgK,
  Tm 1700 K, T0 300 K. Checked against the high-speed closed form (within 1.5 % at 800 mm/s). · Simple,
  transparent, and depth = width / 2 is a known limitation that the band treatment already accepts.
- **2026-10-22** · LLM = GLM-5.2 (FP8, about 450k token context) on a hosted vLLM server I have access to,
  called through its OpenAI-compatible API. Replaces the 2026-10-09 "local models only (Ollama)" decision.
  Endpoint URL, model name and key live only in `.env` (`LLM_BASE_URL`, `LLM_MODEL`, `LLM_API_KEY`). · Far
  stronger than any model that fits in 8 GB VRAM, and the context is large enough for whole papers; no cost
  to me. Costs: needs the network, and paper text leaves the laptop (the papers are open access, so that is
  acceptable).
- **2026-10-22** · Thinking mode ON for every call, and the agent prints the model's reasoning at every step
  (also saved in the trace). · Seeing why the agent picked a tool or a value is the point of the project for
  me and the best debugging aid. Cost: tested on a five-word reply, 270 of 279 output tokens were reasoning,
  so calls are slower and `max_tokens` must be generous or the answer comes back empty.
- **2026-10-23** · Conflict check (M4) uses an explicit scoring rubric. The model judges each criterion and
  returns its verdicts as structured fields with a short reason; code adds up the points and maps the total
  to high, medium or low confidence. The rubric (criteria and weights) is written in the prompt so the
  model knows what it is judging, and printed with every result so the engineer can audit it. · Checkpoint
  2.1 feedback suggested a rubric to make the judgement transparent and repeatable. Summing in code rather
  than letting the model add points keeps to the rule that the LLM never does arithmetic, and the same
  verdicts always give the same score. Draft criteria: comparable supporting papers (+), contradicting
  comparable papers (-), result inside the physics band at all absorptivities (+, small weight because the
  model is approximate), measurement method and replicates reported (+), physics estimate outside its
  valid range or based on broad assumptions (- for the physics term only). Weights to be tuned on test cases.

## Model-choice log
| Date | Role | Candidates | Result | Choice |
|---|---|---|---|---|
| 2026-10-09 | (plan) Extractor / Analyst | Qwen3-8B Q4 | not yet tested | first candidate |
| 2026-10-09 | (plan) Checker | different family ~4B (e.g. Gemma) vs Qwen3-8B self-check; Prof's AdditiveLLM2-OA | not yet tested | pending |
| 2026-10-09 | (plan) Embeddings | Qwen3-Embedding-0.6B, bge-m3 | not yet tested | pending |
| 2026-10-22 | All agent roles (Extractor, Checker, Analyst) | GLM-5.2 hosted vs local Qwen3-8B Q4 | GLM-5.2 reachable, key valid, thinking on/off both work | GLM-5.2, thinking on; replaces the local plan above |

Original constraint (local plan, now superseded for the LLM): 8 GB VRAM → ~4-bit quantised models ≤ ~8B;
usable context about 8k to 16k tokens. Still relevant if embeddings run locally.
