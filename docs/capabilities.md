# Capability ledger

Every capability promised in the course checkpoints, where it lives in the notebook, and the evidence that
shows it works. The final report and video should point to the "Evidence" column. Status: ✅ built and tested
on real data, 🟡 built but only on made-up data or partly, ⬜ not built yet.

Last updated 2026-11-07. Notebook column uses the Parts of `docs/notebook-outline.md` (0 to 11).

## Library and retrieval

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 1 | Find open-access PBF-LB papers automatically (OpenAlex, Europe PMC full text) | 1.1, 3.1 | 3.2, 3.9 | Paper table with licences | ✅ v1: 5 x 316L + 1 distractor (3.1). Frozen library v2 (11-07): 10 x 316L (20 to 50 µm, 1 review) + 1 distractor, all CC BY, from about 400 search hits. 1.1 said 15 to 20 papers, scope guard says 5 to 10 |
| 2 | Parse full text including tables | 3.1 | 3.1, 3.11 | Parsed table next to the original | ✅ tables also rendered to HTML with merged cells for the answer-key sheets |
| 3 | Alloy label + metadata filter (similarity trap) | 3.1 | 3.6 | Distractor ranks 7th without the filter | ✅ |
| 4 | Chunking (250 words, 50 overlap, tables whole) | 3.1 | 3.3 | Chunk counts | ✅ |
| 5 | Chunking experiment (chunk size, tables whole vs split) | new | 3.3, 3.10 | Retrieval recall@5 against the answer key | ⬜ both chunkers now exist (v1 fixed windows, v2 LangChain recursive splitter), comparison needs the answer key |
| 6 | Qwen3 embeddings, ChromaDB, MMR, max 2 per paper | 3.1 | 3.4, 3.5, 3.10 | MMR changed 8 of 8 result lists | ✅ v1 hand-written. v2 with LangChain `Chroma` + MMR retriever + alloy filter, cap applied after MMR |
| 7 | Stated-conditions lookup (layer thickness) | 3.1 | 3.7, 3.9 | Conditions printed per paper | ✅ works on both libraries |
| 8 | With vs without retrieval, invented citations caught | 2.1, 3.1 | 3.8 | Two answers side by side; citation check | ✅ invented citations checked in code: none of the 4 studies exists in Crossref as written, every grounded citation points to a real passage |

## Tools

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 9 | `convert_units`, `energy_density`, `melt_pool_band` | 2.1 | 1 | 26 checks, depth band plot | ✅ |
| 10 | `consensus_lookup` (records at similar settings) | 2.1 | 6.6 | Query result for a test record | ✅ `consensus_lookup` as a LangChain tool on `comparable()` |
| 11 | Source check (value verbatim in its passage) | 2.1, 5.1 | 6.1 to 6.3, 8.4 | Pass and fail cases | ✅ 190 real records, plus the same-row check. Planted: value not in passage and value from another sample caught |
| 12 | Tools served over MCP (fastmcp), each agent only its own | 2.x, 5.1 diagram | | Agent calling a tool through the MCP server | ⬜ |

## Agents and coordination

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 13 | Reader: structured extraction with citation, reasoning printed | 1.1, 5.1 | 4.1, 5.1 to 5.3 | Records for the real papers with passage IDs | ✅ 190 records from L01 to L10 with chunk ids (24 calls, reasoning traced), traps table, `data/extraction/reader_records.csv`. Accuracy: see 28 |
| 14 | Checker: energy density recomputed vs reported | 4.1, decisions 10-30 | 6.1, 6.2 | 389 J/mm³ case passes, corrupted record fails | ✅ 52 pass, 1 fail on real records. Range check added: 32 unit slips caught |
| 15 | Checker: required conditions present, primary vs quoted, same process | decisions 10-30 | 6.1, 6.2 | Pass/fail table per record | ✅ 14 incomplete, 21 quoted, 1 DED row on real records |
| 16 | One retry with the reason, then "not verified" | 5.1 | 8.4, 8.7, 8.11 | Run log | ✅ real run: 33 records sent back from 4 papers, 31 fixed, 2 not verified |
| 17 | Comparability rule and conflict flag | 2.1, 4.1 | 6.5, 8.12 | Flagged pairs | ✅ strict rule active (Chinmay, 11-07): 1 cross-paper conflict and 9 method-spread pairs, against 70 pairs with the old rule |
| 18 | Outlier only if consensus AND the whole physics band disagree | 1.1, 2.1 | 6.6 | Outlier table with both signals | ✅ consensus AND the whole melt-pool band, shown on 36 real records (0 outliers with the strict rule), synthetic test |
| 19 | Analyst: Tree of Thought (generator, critic, rubric, beam 2, depth 2, evidence-gated) | 4.1 | 7, 8.11, 8.12 | Tree printout for the 97.76 % vs 99.97 % case | ✅ generator, critic, rubric, beam 2, depth 2, evidence gate. 2 known cases right, L04 vs L07 run inside the graph |
| 20 | Outcome bands and evidence tiers | decisions 11-06 | 7.1 | Resolved / Competing / Unresolved per conflict | ✅ Resolved / Competing / Unresolved with tiers A to D. Calibration open: method explanations cap at +5 |
| 21 | Coordinator in code, parallel Readers, conditional Analyst, limits | 5.1 | 8.6 to 8.11 | Graph drawing, run log, timeline | ✅ with the real Reader and Checker (5.11). Analyst still a stand-in |

## Memory and guardrails

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 22 | Clarification step (grade, machine, layer thickness) | 2.1 | 9.2 | "Stainless steel" request asks back | ✅ "stainless steel" request pauses and asks for grade, machine and layer thickness |
| 23 | Human approval interrupt, resume, reject | 5.1 | 8.8, 8.9 | Paused state, approve and reject runs | ✅ wiring |
| 24 | Persistent state (SQLite checkpointer), evidence store across runs | 2.1, 5.1 | 9.1 | Resume after kernel restart | ✅ SQLite checkpointer: paused run resumed by a fresh graph on a fresh connection. Evidence table in SQLite with SQL queries |
| 25 | Engineer-feedback memory changes a later run | 2.1 | 9.3 | Constraint (e.g. 400 W limit) filters run 2 | ✅ a 200 W limit from run 1 (LangGraph `SqliteStore`) filters run 2. A 400 W limit would change nothing |
| 26 | Widen to neighbouring layer thickness, mark "adjacent" | 2.1 | | Sparse request widened | ⬜ |

## Evaluation and traceability

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 27 | Hand-checked answer key | 1.1 | 3.11, `eval/` | CSV, checked by Chinmay | 🟡 sheets, template and scope ready (L08 only Table 5). Chinmay fills it |
| 28 | Extraction accuracy per field | 1.1, 5.1 | 10.1 | Accuracy table | 🟡 scoring code ready and tested on a synthetic key, waits for the answer key |
| 29 | Planted (corrupted) records caught | 1.1, 5.1 | 6.3, 6.4 | Caught / missed table | ✅ 5 of 5 caught after the column check (4 of 5 before) |
| 30 | Prompt-only baseline vs agent | 2.1 | 3.8, 4, 10.2 | Same questions, both scored | 🟡 prompt-only answer checked in code (3.8), single agent built (Part 4). Scoring waits for the key |
| 31 | Tree of Thought vs single thinking call | 4.1 | 7.2, 8.12, 10.2 | 2 to 3 conflicts compared | ✅ 3 cases compared: agree on both known cases, disagree on L04 vs L07 |
| 32 | Multi-agent vs single agent (accuracy, calls, run time) | 5.1 | 4, 6.7, 10.2 | Comparison table | 🟡 calls, tokens, time and Checker results compared. Accuracy waits for the key |
| 33 | Every model call traced (prompt, reasoning, answer, tokens, time) and cached | conventions | 0.2, 0.3, 2.2 | Trace viewer cell | ✅ `ChatGLM` + `set_llm_cache` (SQLite backend) + `TraceRecorder` callback, JSONL per run, `show_trace`. Graph nodes are named automatically once real agents use `glm` |
| 34 | Every value in the recommendation links to paper and passage | 1.1 | 8.11 | Recommendation with citations | 🟡 window cites record ids with their chunk ids and shows supporting records. Not yet shown as paper and passage text |

Count on 2026-11-07 (after Session C): 26 ✅, 5 🟡, 3 ⬜.
