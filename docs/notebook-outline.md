# Notebook outline and concept map

The final notebook tells one story: from an engineer's request to an approved, cited process window.
Each Part is one logical step that builds on the previous one, and each Part states:

- **Question:** what this step answers, in one sentence.
- **Course concept:** which module idea it applies.
- **Framework feature:** the LangChain or LangGraph component that implements it (hand-written code
  only where no framework piece fits, and then say why).
- **Evidence:** the checks and outputs that prove it works (these feed `capabilities.md`, the report
  and the video).

Agreed 2026-11-07: use LangChain and LangGraph capabilities as fully as is sensible, and make every
course concept visible somewhere in the notebook.

| Part | Step (question it answers) | Course concept | LangChain / LangGraph feature | Capabilities |
|---|---|---|---|---|
| 0 | Setup: settings, test helper, cache and trace for every model call | Harness, observability (M4) | `set_llm_cache`, callback handler for traces (LangSmith optional) | 33 |
| 1 | Which calculations must never be left to the model? | Tool use, LLMs are weak at arithmetic (M1, M2) | `@tool` with docstring schemas: `convert_units`, `energy_density`, `melt_pool_band`, `consensus_lookup` | 9, 10 |
| 2 | How do we talk to the model reliably? | Prompting, structured output, function calling (M1, M2) | `ChatOpenAI` for GLM-5.2 with reasoning shown, `ChatPromptTemplate`, `with_structured_output` (Pydantic), `bind_tools` | 33 |
| 3 | Where does the knowledge come from? (RAG) | Retrieval, chunking, embeddings, vector store, MMR, metadata filters, grounding (M3) | Text splitters, `Chroma` vector store, MMR retriever with alloy filter, LCEL grounded-answer chain; chunking experiment | 1 to 8 |
| 4 | Can one agent answer with tools? (single-agent baseline) | ReAct loop, observations written by code (M2) | `create_agent` / prebuilt ReAct agent with the Part 1 and Part 3 tools | 30, 32 |
| 5 | What exactly does each paper report? (Reader) | Structured extraction, "the model reads, code decides", context budget (M5) | `with_structured_output(Record)` per paper | 13, 34 |
| 6 | Which records can we trust? (Checker) | Verification, evaluator, consensus, physics as weak evidence | Plain code checks wrapped as tools; consensus and physics band; outlier rule | 11, 14, 15, 17, 18 |
| 7 | Why do comparable studies disagree? (Analyst) | Tree of Thought: generator, critic, beam, rubric, pruning (M4) | LangGraph subgraph, `Send` for branches, structured critic output | 19, 20, 31 |
| 8 | How do the agents work together? | Multi-agent coordination and communication (M5), MCP (M2, M4) | `StateGraph`, reducers, `Send`, conditional edges, `RetryPolicy`, `recursion_limit`; tools served with fastmcp over HTTP and wrapped as LangChain tools (`langchain-mcp-adapters` needs mcp below 2.0, see 8.15) | 12, 16, 21, 26 |
| 9 | When must a human decide? (guardrails) | Human in the loop, guardrails, memory types (M2, M6) | `interrupt` and `Command(resume=...)` for clarification and approval, SQLite checkpointer, LangGraph `Store` for engineer feedback | 22 to 25 |
| 10 | Does it actually work? (evaluation) | Benchmarking, baselines, "did the extra coordination pay for itself?" (M5) | Traces and cache for cost and latency; scoring against the answer key | 27 to 32 |
| 11 | End-to-end demo for the video | All of the above | One request through the full graph, trace shown | 34 |

Notes:
- The current Part 5 skeleton (stub agents, made-up papers) becomes Part 8 once the real agents exist.
  The made-up papers stay as offline wiring tests.
- Part 3 was submitted with Checkpoint 3.1 using hand-written chunking and MMR. Keep those results
  reproducible, add the LangChain equivalents next to them, and let the chunking experiment compare them.
- Fine-tuning (Module 5) is not used: one paragraph in Part 10 explains why RAG fits changing literature
  better than tuning.

## Documentation standard (agreed 2026-11-07, shortened 2026-11-08)

The notebook reads as one short argument from request to approved window, in Chinmay's voice (an AM engineer explaining
his own tool to another engineer: first person, plain words, short sentences, no em or en dashes, no semicolons, no
filler words). About 6,000 to 7,000 words of markdown in total.

- **Each Part opens** with one sentence linking it to the previous Part (what that Part left open), then four one-line
  bullets: Question, Course concept, Framework feature, Evidence.
- **Each subsection** has at most about 60 to 80 words: what this step does, why, and what to look at in the output.
  An agent term is explained the first time it appears.
- **Every rule keeps its reason** in one sentence. Long implementation detail lives in `docs/decisions.md`, with a
  one-line pointer such as "details: decisions.md, 2026-11-07".
- **Failures stay**, each told in a few lines (L04 vs L07, the L08 Table 4 skip, the baseline's older label, the
  Reader's repeatability).
- **Each Part ends** with "what this showed" in two lines.
- **Part 0 holds** the "how the pieces fit" list (one line per step), the rules table (rule, value, short reason,
  where, decision date), a glossary of about ten agent words and a 15-minute reading guide.
