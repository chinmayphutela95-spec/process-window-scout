# Capability ledger

Every capability promised in the course checkpoints, where it lives in the notebook, and the evidence that
shows it works. The final report and video should point to the "Evidence" column. Status: ✅ built and tested
on real data, 🟡 built but only on made-up data or partly, ⬜ not built yet.

Last updated 2026-11-07.

## Library and retrieval

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 1 | Find open-access PBF-LB papers automatically (OpenAlex, Europe PMC full text) | 1.1, 3.1 | 3a | Paper table with licences | ✅ 5 x 316L + 1 distractor. 1.1 said 15 to 20 papers, scope guard says 5 to 10 |
| 2 | Parse full text including tables | 3.1 | 3a | Parsed table next to the original | ✅ |
| 3 | Alloy label + metadata filter (similarity trap) | 3.1 | 3a.6 | Distractor ranks 7th without the filter | ✅ |
| 4 | Chunking (250 words, 50 overlap, tables whole) | 3.1 | 3a.3 | Chunk counts | ✅ |
| 5 | Chunking experiment (chunk size, tables whole vs split) | new | | Retrieval recall@5 against the answer key | ⬜ needs answer key |
| 6 | Qwen3 embeddings, ChromaDB, MMR, max 2 per paper | 3.1 | 3a.4, 3a.5 | MMR changed 8 of 8 result lists | ✅ |
| 7 | Stated-conditions lookup (layer thickness) | 3.1 | 3a.7 | Conditions printed per paper | ✅ |
| 8 | With vs without retrieval, invented citations caught | 2.1, 3.1 | 3a.8 | Two answers side by side; citation check | 🟡 citation check was done by hand, make it a code cell |

## Tools

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 9 | `convert_units`, `energy_density`, `melt_pool_band` | 2.1 | 1 | 26 checks, depth band plot | ✅ |
| 10 | `consensus_lookup` (records at similar settings) | 2.1 | | Query result for a test record | ⬜ |
| 11 | Source check (value verbatim in its passage) | 2.1, 5.1 | 5.4 | Pass and fail cases | 🟡 made-up passages only |
| 12 | Tools served over MCP (fastmcp), each agent only its own | 2.x, 5.1 diagram | | Agent calling a tool through the MCP server | ⬜ |

## Agents and coordination

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 13 | Reader: structured extraction with citation, reasoning printed | 1.1, 5.1 | | Records for the real papers with passage IDs | ⬜ needs VPN |
| 14 | Checker: energy density recomputed vs reported | 4.1, decisions 10-30 | | 389 J/mm³ case passes, corrupted record fails | ⬜ |
| 15 | Checker: required conditions present, primary vs quoted, same process | decisions 10-30 | | Pass/fail table per record | ⬜ |
| 16 | One retry with the reason, then "not verified" | 5.1 | 5.4, 5.7 | Run log | 🟡 made-up data |
| 17 | Comparability rule and conflict flag | 2.1, 4.1 | 5.5 | Flagged pairs | 🟡 rule (energy density within 10 %) needs Chinmay's decision |
| 18 | Outlier only if consensus AND the whole physics band disagree | 1.1, 2.1 | | Outlier table with both signals | ⬜ |
| 19 | Analyst: Tree of Thought (generator, critic, rubric, beam 2, depth 2, evidence-gated) | 4.1 | 5.5 stub | Tree printout for the 97.76 % vs 99.97 % case | ⬜ needs VPN |
| 20 | Outcome bands and evidence tiers | decisions 11-06 | | Resolved / Competing / Unresolved per conflict | ⬜ |
| 21 | Coordinator in code, parallel Readers, conditional Analyst, limits | 5.1 | 5.6 to 5.10 | Graph drawing, run log, timeline | ✅ wiring (made-up data) |

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
| 27 | Hand-checked answer key | 1.1 | | CSV, checked by Chinmay | ⬜ Chinmay, offline |
| 28 | Extraction accuracy per field | 1.1, 5.1 | | Accuracy table | ⬜ needs 13 + 27 |
| 29 | Planted (corrupted) records caught | 1.1, 5.1 | | Caught / missed table | ⬜ |
| 30 | Prompt-only baseline vs agent | 2.1 | 3a.8 partly | Same questions, both scored | 🟡 |
| 31 | Tree of Thought vs single thinking call | 4.1 | | 2 to 3 conflicts compared | ⬜ |
| 32 | Multi-agent vs single agent (accuracy, calls, run time) | 5.1 | | Comparison table | ⬜ |
| 33 | Every model call traced (prompt, reasoning, answer, tokens, time) and cached | conventions | 2 (`ask_llm`) | Trace viewer cell | 🟡 per-run trace for the graph still to do |
| 34 | Every value in the recommendation links to paper and passage | 1.1 | | Recommendation with citations | ⬜ |

Count on 2026-11-07: 9 ✅ (two of them wiring only), 6 🟡, 19 ⬜.
