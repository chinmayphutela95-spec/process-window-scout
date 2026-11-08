# Build plan

The agent is built in small milestones that follow the course modules, so each concept is learned before
it is used. Each milestone is one Part of the project notebook and ends with working code, passing test cells,
a short demo and a commit.

## Code layout (notebook first)

```
notebooks/
  process_window_scout.ipynb   the whole project: one Part per milestone, each with explanation,
                               code, test cells and a demo; runs top to bottom on the laptop
data/                          cached papers, parsed text, vector and evidence databases, traces (gitignored)
```

The final project is one Jupyter notebook that runs on this laptop, so the code is written and tested in
the notebook itself, Part by Part, rather than in a separate package. Rules that keep it workable:
- **Restart & Run All must always pass.** Each Part ends with test cells (`check(...)` prints `ok` or stops).
- Slow steps (downloads, model calls) cache to `data/` and skip work that is already done.
- Later Parts reuse earlier functions; they never redefine them.
- Extra files only where a separate process needs them: the MCP server (Part 8.15), written from the notebook
  with `%%writefile` to `data/mcp/` (gitignored, regenerated on every run), and the small Streamlit UI in `app/` (Part 12).
  The UI holds page code only: `app/notebook_core.py` runs the notebook's cells tagged `core`, so the logic stays in one place.

## Milestones (updated 2026-10-30 after the Checkpoint 4.1 design)

| # | Part | Milestone | Checkpoint | Status / done when |
|---|---|---|---|---|
| M1 | 1 | Deterministic tools: `convert_units`, `energy_density`, `melt_pool_band` | 2.1 | ✅ 2026-10-18 |
| M2a | 2 | GLM-5.2 client (`ask_llm`, thinking on, reasoning printed). Then (2.2 to 2.4) `ChatGLM` for LangChain, cache (`set_llm_cache`) and trace (callback handler) for every model call, spike on structured output and tool calls | 3.1 | ✅ 2026-10-24, LangChain layer ✅ 2026-11-07 |
| M3a | 3a | Retrieval: Europe PMC library (5 x 316L + 1 distractor), chunks, Qwen3 embeddings in ChromaDB, `search_passages` (MMR, alloy filter, max 2 per paper), `stated_conditions`, with/without demo. Then (3a.9 to 3a.11) the frozen library v2 (10 x 316L + distractor) with LangChain splitter, Chroma and MMR retriever, and answer-key review sheets | 3.1 | ✅ 2026-10-24, library v2 ✅ 2026-11-07 |
| M2b | 2 | ReAct agent in **LangGraph** (`langchain-openai` to install; check that GLM's reasoning survives the wrapper) with tools: `search_passages`, `stated_conditions`, Part 1 tools; reasoning printed at every step; trace saved | 4.1 | ✅ 2026-11-07 as the single-agent baseline (notebook Part 4: `create_agent` with four tools) |
| M3b | 3b | **Evidence table + automated checks** (graders' main ask): extract records (alloy, process, power, speed, hatch, layer, density, method, source passage) with structured output into SQLite; code checks: value verbatim in its passage, energy density recomputed vs reported, required conditions present, primary vs quoted data | 4.1 | ✅ 2026-11-07 (Parts 5 and 6: Reader with reading units, code Checker with the column check, planted errors 5 of 5, SQLite evidence table in 9.1) |
| M4 | 4 | **Tree of Thought for conflicts** (LangGraph subgraph): conflict flagging on comparable records; generator, critic with the rubric (model judges, code sums), beam 2, depth 2, evidence-gated scoring; test case 97.76% vs 99.97% at 30 µm | 4.1 | ✅ 2026-11-07 (Part 7, run in the graph in 8.11). Session D: quote per side, code facts only when they test the cause, both papers' method sentences for every branch, gate fixed. Open: the critic still judges whether a quote supports the cause |
| M5 | 5 | Multi-agent graph (design in Checkpoint 5.1): Coordinator in code + Reader (parallel, `Send`), Checker, Analyst sharing one evidence table (`operator.add` reducer); one retry then "not verified"; `recursion_limit` and `max_concurrency` set; tools over MCP with fastmcp, each agent only its own. Skeleton with stub nodes and a scripted fake model can be built first and filled by M2b, M3b, M4 | 5.1 | ✅ 2026-11-07 with the real Reader, Checker and Tree of Thought Analyst (Part 8), and since Session D conflicts at every layer, windows per density method, widening (8.14) and tools over MCP (8.15). Still: multi vs single agent accuracy (needs the answer key) |
| M6 | 6 | Guardrails: clarification step (alloy grade, machine, layer thickness), human approval with a LangGraph interrupt, engineer-feedback memory | 6.1 | ✅ 2026-11-07 (Part 9: clarification interrupt, SQLite checkpointer, SqliteStore feedback memory) |
| M7 | 7 | Evaluation: frozen test set (frozen before tuning), extraction accuracy per (paper, field), prompt-only baseline vs agent, ToT vs single call; optional Streamlit UI; demo video recorded separately | final | ✅ 2026-11-08: Part 10 per question, scored on the checked answer key (93 rows): accuracy per paper and field, multi against single agent, chunking on the real key. Part 11 demo built. Streamlit UI ✅ 2026-11-08 (Part 12, `app/`, app test in `tests/test_app.py`). Next: the online rerun (new tree answers after the clarity gate), then the report and video |

**Scope guard:** MVP library of 5 to 10 papers, ToT on 2 to 3 real conflicts. A small system that works and
is measured honestly beats a large unfinished one.

The target structure of the final notebook (Parts 0 to 12, each with question, course concept and framework
feature) is in `docs/notebook-outline.md`, with the documentation standard agreed on 2026-11-07.

## Conventions
- Prefer established frameworks over hand-written code (LangGraph for the agent loop and multi-agent flow,
  LangChain tool wrappers, ChromaDB, fastmcp), but explain each concept in the notebook before using it.
- Tools are plain Python, tested in the notebook without a model before any agent uses them.
- The model never writes observations; code does. The model never does arithmetic; code does.
- Every tool result states its inputs and units.
- No API keys or endpoint URLs in the repository; the server address and key come from `.env`
  (see `.env.example`); the model name `GLM-5.2` is set in the code.
- Thinking mode on; the model's reasoning is printed at every agent step and saved in the trace.
