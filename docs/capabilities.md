# Capability ledger

Every capability promised in the course checkpoints, where it lives in the notebook, and the evidence that
shows it works. The final report and video should point to the "Evidence" column. Status: ✅ built and tested
on real data, 🟡 built but only on made-up data or partly, ⬜ not built yet.

Last updated 2026-11-07.

## Library and retrieval

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 1 | Find open-access PBF-LB papers automatically (OpenAlex, Europe PMC full text) | 1.1, 3.1 | 3a, 3a.9 | Paper table with licences | ✅ v1: 5 x 316L + 1 distractor (3.1). Frozen library v2 (11-07): 10 x 316L (20 to 50 µm, 1 review) + 1 distractor, all CC BY, from about 400 search hits. 1.1 said 15 to 20 papers, scope guard says 5 to 10 |
| 2 | Parse full text including tables | 3.1 | 3a, 3a.11 | Parsed table next to the original | ✅ tables also rendered to HTML with merged cells for the answer-key sheets |
| 3 | Alloy label + metadata filter (similarity trap) | 3.1 | 3a.6 | Distractor ranks 7th without the filter | ✅ |
| 4 | Chunking (250 words, 50 overlap, tables whole) | 3.1 | 3a.3 | Chunk counts | ✅ |
| 5 | Chunking experiment (chunk size, tables whole vs split) | new | 3a.3, 3a.10 | Retrieval recall@5 against the answer key | ⬜ both chunkers now exist (v1 fixed windows, v2 LangChain recursive splitter), comparison needs the answer key |
| 6 | Qwen3 embeddings, ChromaDB, MMR, max 2 per paper | 3.1 | 3a.4, 3a.5, 3a.10 | MMR changed 8 of 8 result lists | ✅ v1 hand-written. v2 with LangChain `Chroma` + MMR retriever + alloy filter, cap applied after MMR |
| 7 | Stated-conditions lookup (layer thickness) | 3.1 | 3a.7, 3a.9 | Conditions printed per paper | ✅ works on both libraries |
| 8 | With vs without retrieval, invented citations caught | 2.1, 3.1 | 3a.8 | Two answers side by side; citation check | 🟡 submitted run now replayed from its trace (same passages checked). Citation check was done by hand, make it a code cell |

## Tools

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 9 | `convert_units`, `energy_density`, `melt_pool_band` | 2.1 | 1 | 26 checks, depth band plot | ✅ |
| 10 | `consensus_lookup` (records at similar settings) | 2.1 | | Query result for a test record | ⬜ |
| 11 | Source check (value verbatim in its passage) | 2.1, 5.1 | 5.4, 3b.5 to 3b.7 | Pass and fail cases | ✅ 190 real records, plus the same-row check. Planted: value not in passage and value from another sample caught |
| 12 | Tools served over MCP (fastmcp), each agent only its own | 2.x, 5.1 diagram | | Agent calling a tool through the MCP server | ⬜ |

## Agents and coordination

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 13 | Reader: structured extraction with citation, reasoning printed | 1.1, 5.1 | 3b.1 to 3b.4 | Records for the real papers with passage IDs | ✅ 190 records from L01 to L10 with chunk ids (24 calls, reasoning traced), traps table, `data/extraction/reader_records.csv`. Accuracy: see 28 |
| 14 | Checker: energy density recomputed vs reported | 4.1, decisions 10-30 | 3b.5, 3b.6 | 389 J/mm³ case passes, corrupted record fails | ✅ 52 pass, 1 fail on real records. Range check added: 32 unit slips caught |
| 15 | Checker: required conditions present, primary vs quoted, same process | decisions 10-30 | 3b.5, 3b.6 | Pass/fail table per record | ✅ 14 incomplete, 21 quoted, 1 DED row on real records |
| 16 | One retry with the reason, then "not verified" | 5.1 | 5.4, 5.7, 5.11 | Run log | ✅ real run: 33 records sent back from 4 papers, 31 fixed, 2 not verified |
| 17 | Comparability rule and conflict flag | 2.1, 4.1 | 5.5, 5.11 | Flagged pairs | 🟡 provisional rule flags 70 pairs on real records (22 inside one paper). Needs Chinmay's decision |
| 18 | Outlier only if consensus AND the whole physics band disagree | 1.1, 2.1 | | Outlier table with both signals | ⬜ |
| 19 | Analyst: Tree of Thought (generator, critic, rubric, beam 2, depth 2, evidence-gated) | 4.1 | 5.5 stub | Tree printout for the 97.76 % vs 99.97 % case | ⬜ needs VPN |
| 20 | Outcome bands and evidence tiers | decisions 11-06 | | Resolved / Competing / Unresolved per conflict | ⬜ |
| 21 | Coordinator in code, parallel Readers, conditional Analyst, limits | 5.1 | 5.6 to 5.11 | Graph drawing, run log, timeline | ✅ with the real Reader and Checker (5.11). Analyst still a stand-in |

## Memory and guardrails

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 22 | Clarification step (grade, machine, layer thickness) | 2.1 | | "Stainless steel" request asks back | ⬜ |
| 23 | Human approval interrupt, resume, reject | 5.1 | 5.8, 5.9 | Paused state, approve and reject runs | ✅ wiring |
| 24 | Persistent state (SQLite checkpointer), evidence store across runs | 2.1, 5.1 | | Resume after kernel restart | ⬜ install `langgraph-checkpoint-sqlite` |
| 25 | Engineer-feedback memory changes a later run | 2.1 | | Constraint (e.g. 400 W limit) filters run 2 | ⬜ |
| 26 | Widen to neighbouring layer thickness, mark "adjacent" | 2.1 | | Sparse request widened | ⬜ |

## Evaluation and traceability

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 27 | Hand-checked answer key | 1.1 | 3a.11, `eval/` | CSV, checked by Chinmay | 🟡 review sheets (HTML) and empty template ready 11-07. Chinmay fills it offline |
| 28 | Extraction accuracy per field | 1.1, 5.1 | | Accuracy table | ⬜ needs 13 + 27 |
| 29 | Planted (corrupted) records caught | 1.1, 5.1 | 3b.7 | Caught / missed table | ✅ 4 of 5 caught. Missed: speed and hatch swapped with both in range |
| 30 | Prompt-only baseline vs agent | 2.1 | 3a.8 partly | Same questions, both scored | 🟡 |
| 31 | Tree of Thought vs single thinking call | 4.1 | | 2 to 3 conflicts compared | ⬜ |
| 32 | Multi-agent vs single agent (accuracy, calls, run time) | 5.1 | | Comparison table | ⬜ |
| 33 | Every model call traced (prompt, reasoning, answer, tokens, time) and cached | conventions | 2.2, 2.3, 2.4 | Trace viewer cell | ✅ `ChatGLM` + `set_llm_cache` (SQLite backend) + `TraceRecorder` callback, JSONL per run, `show_trace`. Graph nodes are named automatically once real agents use `glm` |
| 34 | Every value in the recommendation links to paper and passage | 1.1 | 5.11 | Recommendation with citations | 🟡 window cites record ids, each with its chunk ids. Not yet shown to the engineer as paper and passage |

Count on 2026-11-07 (after Session B): 16 ✅, 5 🟡, 13 ⬜.
