# Build plan

The agent is built in small milestones that follow the course modules, so each concept is learned before
it is used. Each milestone is one Part of the project notebook and ends with working code, passing test cells,
a short demo and a commit.

## Code layout (notebook first)

```
notebooks/
  process_window_scout.ipynb   the whole project: one Part per milestone, each with explanation,
                               code, test cells and a demo; runs top to bottom on the laptop
data/                          cached papers, parsed text, evidence database, traces (gitignored)
```

The final project is one Jupyter notebook that runs on this laptop, so the code is written and tested in
the notebook itself, Part by Part, rather than in a separate package. Rules that keep it workable:
- **Restart & Run All must always pass.** Each Part ends with test cells (`check(...)` prints `ok` or stops).
- Slow steps (downloads, model calls) cache to `data/` and skip work that is already done.
- Later Parts reuse earlier functions; they never redefine them.
- The only extra file will be the MCP server (Part 6), written from the notebook with `%%writefile` because
  MCP runs it as a separate process.

## Milestones

| # | Milestone | Course link | Done when |
|---|---|---|---|
| M1 ✅ | Deterministic tools: `convert_units`, `energy_density`, `melt_pool_band` | Module 2 (tools) | Tools return sentences with inputs and units; test cells pass (done 2026-10-18) |
| M2 | LLM client (GLM-5.2, thinking on) + first ReAct agent using the M1 tools, with trace logging | Module 2 (ReAct) | Agent answers an energy-density question through tool calls; its reasoning is printed at every step; trace saved |
| M3 | Paper pipeline: OpenAlex search, PDF download, parsing, evidence store | Module 3 (RAG) | 15 to 20 open-access 316L papers ingested; records with citations in SQLite |
| M4 | Source check, consensus lookup and conflict check | Modules 3 to 4 | Each record verified against its passage; conflicts labelled with confidence |
| M5 | Tree of Thought for outlier explanations and window selection | Module 4 | Three candidate windows scored and one chosen with reasons |
| M6 | Reader and Checker agents; tools served over MCP | Module 5 | Two agents coordinate through shared tools |
| M7 | Guardrails, clarification step, engineer feedback memory | Module 6 | Unsafe or ambiguous requests handled; feedback changes a later run |
| M8 | Evaluation and final notebook: prompt-only baseline vs agent | Module 7 | Extraction accuracy and baseline comparison reported |

## Conventions
- Prefer established frameworks over hand-written code (LangGraph for the agent loop and multi-agent flow,
  LangChain tool wrappers, ChromaDB, fastmcp), but explain each concept in the notebook before using it.
- Tools are plain Python, tested in the notebook without a model before any agent uses them.
- The model never writes observations; code does.
- Every tool result states its inputs and units.
- No API keys or endpoint URLs in the repository; the LLM settings come from `.env` (`LLM_BASE_URL`,
  `LLM_MODEL`, `LLM_API_KEY`).
- Thinking mode on; the model's reasoning is printed at every agent step and saved in the trace.
