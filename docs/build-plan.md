# Build plan

The agent is built in small milestones that follow the course modules, so each concept is learned before
it is used. Each milestone ends with working, tested code, a short demo section in the project notebook,
and a commit.

## Code layout

```
src/pws/
  tools/        deterministic tools (units, energy density, melt-pool band, consensus, papers)
  agent.py      ReAct loop
  llm.py        model client (Ollama), one place to swap models
  memory.py     run summary, evidence store, engineer feedback
  trace.py      logging of every thought, tool call and observation
  mcp_server.py tools exposed over MCP (fastmcp)
tests/          pytest tests for every tool (run without any model)
notebooks/
  process_window_scout.ipynb   the project notebook: explanation + live demos, imports from src/pws
```

Logic lives in `src/pws`; the notebook only explains and demonstrates. This keeps the code testable and
the notebook readable, in the style of the course lab notebooks.

## Milestones

| # | Milestone | Course link | Done when |
|---|---|---|---|
| M1 | Deterministic tools: `convert_units`, `energy_density`, `melt_pool_band` | Module 2 (tools) | Tools return sentences with inputs and units; pytest passes |
| M2 | Ollama + first ReAct agent using the M1 tools, with trace logging | Module 2 (ReAct) | Agent answers an energy-density question through tool calls; trace saved |
| M3 | Paper pipeline: OpenAlex search, PDF download, parsing, evidence store | Module 3 (RAG) | 15 to 20 open-access 316L papers ingested; records with citations in SQLite |
| M4 | Source check, consensus lookup and conflict check | Modules 3 to 4 | Each record verified against its passage; conflicts labelled with confidence |
| M5 | Tree of Thought for outlier explanations and window selection | Module 4 | Three candidate windows scored and one chosen with reasons |
| M6 | Reader and Checker agents; tools served over MCP | Module 5 | Two agents coordinate through shared tools |
| M7 | Guardrails, clarification step, engineer feedback memory | Module 6 | Unsafe or ambiguous requests handled; feedback changes a later run |
| M8 | Evaluation and final notebook: prompt-only baseline vs agent | Module 7 | Extraction accuracy and baseline comparison reported |

## Conventions
- Tools are plain Python, tested without a model before any agent uses them.
- The model never writes observations; code does.
- Every tool result states its inputs and units.
- No API keys in the repository; local models only.
