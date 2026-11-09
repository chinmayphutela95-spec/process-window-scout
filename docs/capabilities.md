# Capability ledger

Every capability promised in the course checkpoints, where it lives in the notebook, and the evidence that
shows it works. The final report and video should point to the "Evidence" column. Status: ✅ built and tested
on real data, 🟡 built but only on made-up data or partly, ⬜ not built yet.

Last updated 2026-11-09. Notebook column uses the Parts of `docs/notebook-outline.md` (0 to 12).

## Library and retrieval

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 1 | Find open-access PBF-LB papers automatically (OpenAlex, Europe PMC full text) | 1.1, 3.1 | 3.2, 3.9, 3.12 | Paper table with licences | ✅ v1: 5 x 316L + 1 distractor (3.1). Frozen library v2 (11-07): 10 x 316L (20 to 50 µm, 1 review) + 1 distractor, all CC BY. Extension (11-07, 3.12): 6 more CC BY 316L papers at 30 µm (E01 to E06), own collection, for window, conflicts and consensus only, never scored |
| 2 | Parse full text including tables | 3.1 | 3.1, 3.11 | Parsed table next to the original | ✅ tables also rendered to HTML with merged cells for the answer-key sheets |
| 3 | Alloy label + metadata filter (similarity trap) | 3.1 | 3.6 | Distractor ranks 7th without the filter | ✅ |
| 4 | Chunking (250 words, 50 overlap, tables whole) | 3.1 | 3.3 | Chunk counts | ✅ |
| 5 | Chunking experiment (chunk size, tables whole vs split) | new | 10.6 | Retrieval recall@5 against the answer key | ✅ recall@5 on the checked key (85 values): v1 windows 0.68 tables whole, 0.74 split, v2 splitter 0.72 either way. Differences of a few values, so tables stay whole |
| 6 | Qwen3 embeddings, ChromaDB, MMR, max 2 per paper | 3.1 | 3.4, 3.5, 3.10 | MMR changed 8 of 8 result lists | ✅ v1 hand-written. v2 with LangChain `Chroma` + MMR retriever + alloy filter, cap applied after MMR |
| 7 | Stated-conditions lookup (layer thickness) | 3.1 | 3.7, 3.9 | Conditions printed per paper | ✅ works on both libraries |
| 8 | With vs without retrieval, invented citations caught | 2.1, 3.1 | 3.8 | Two answers side by side; citation check | ✅ invented citations checked in code: none of the 4 studies exists in Crossref as written, every grounded citation points to a real passage |

## Tools

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 9 | `convert_units`, `energy_density`, `melt_pool_band` | 2.1 | 1 | 26 checks, depth band plot | ✅ |
| 10 | `consensus_lookup` (records at similar settings) | 2.1 | 6.6 | Query result for a test record | ✅ `consensus_lookup` as a LangChain tool on `comparable()` |
| 11 | Source check (value verbatim in its passage) | 2.1, 5.1 | 6.1 to 6.3, 8.4 | Pass and fail cases | ✅ verbatim, same-row and column checks. Headers read by word or by symbol and unit ("P (W)"), unit alone as fallback. 0 false alarms on 134 v2 records |
| 12 | Tools served over MCP (fastmcp), each agent only its own | 2.x, 5.1 diagram | 8.15 | Agent calling a tool through the MCP server | ✅ fastmcp server written with `%%writefile`, own process over HTTP, 4 tools, per-agent tool lists (`AGENT_TOOLS`), parity test against Part 1, Analyst agent called `energy_density` and `melt_pool_band` through the server (call log with the server's process id). `langchain-mcp-adapters` replaced by a 15-line bridge (needs mcp below 2.0) |

## Agents and coordination

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 13 | Reader: structured extraction with citation, reasoning printed | 1.1, 5.1 | 4.1, 5.1 to 5.4 | Records for the real papers with passage IDs | ✅ after the Reader fixes: 134 records from v2 + 14 from the extension, µm slips 32 to 1, L02 means, method per value, parameter tables named by symbol and unit (E04, E05 now complete). Before/after in 8.13. The Reader is not deterministic: L04's speed range became one incomplete record in Session E |
| 14 | Checker: energy density recomputed vs reported | 4.1, decisions 10-30 | 6.1, 6.2 | 389 J/mm³ case passes, corrupted record fails | ✅ energy density recomputed vs printed (2 %), range check: 32 unit slips caught in the first run, 1 after the Reader fixes |
| 15 | Checker: required conditions present, primary vs quoted, same process | decisions 10-30 | 6.1, 6.2 | Pass/fail table per record | ✅ 14 incomplete, 21 quoted, 1 DED row on real records |
| 16 | One retry with the reason, then "not verified" | 5.1 | 8.4, 8.7, 8.11 | Run log | ✅ first run: 33 records sent back, 31 fixed, 2 not verified. After the fixes: 6 sent back (4 became quoted, 2 not verified). A Reader timeout costs one unit, not the run |
| 37 | Check 16: one sample keeps one parameter set across the paper's tables | decision 11-09 (from the evaluation) | 6.4, 8.11, 10.5 | Flag list in 6.4, retries in 8.11, before and after in 10.5 | ✅ a record must match its sample's row in the paper's parameter table. On the Reader's first attempt it flags exactly the three L08 sample 13 rows of Table 5 (200 W against Table 1's 350 W), all real errors, and the retry corrects them. Label reuse and ambiguous labels are not judged (made-up tests in 6.4) |
| 17 | Comparability rule and conflict flag | 2.1, 4.1 | 6.5, 8.12 | Flagged pairs | ✅ active rule (Chinmay, 11-07 evening): methods may differ (tagged), every layer, at most 3 to the Analyst. 30 µm: old rule 84 pairs, strict 2, active 4. All layers: 12 conflicts, 3 across papers, 30 method-spread pairs. Tolerance sensitivity table (9 settings) |
| 18 | Outlier only if consensus AND the whole physics band disagree | 1.1, 2.1 | 6.6 | Outlier table with both signals | ✅ consensus AND the whole melt-pool band, shown on 36 real records (0 outliers with the strict rule), synthetic test |
| 19 | Analyst: Tree of Thought (generator, critic, rubric, beam 2, depth 2, evidence-gated) | 4.1 | 7, 8.11, 8.12 | Tree printout for the 97.76 % vs 99.97 % case | ✅ generator, critic, rubric, beam 2, depth 2, evidence gate and support gate (Session E), both papers' method and condition sentences for every branch. L08 sample 4 method Resolved +8, L06 S1 method Competing +5, L04 vs L07 (Session D record) method Resolved +8. After the clarity gate (online rerun 11-09): E06 vs L06 S9 by Archimedes against image analysis method Competing +5, E06 vs L06 S9 both by Archimedes regime Competing +5. Both causes physically sensible, the regime one only weakly (decisions.md, 2026-11-09) |
| 20 | Outcome bands and evidence tiers | decisions 11-06 | 7.1, 8.12 | Resolved / Competing / Unresolved per conflict | ✅ bands and tiers. Rubric: quote per side (+3 each) with the critic's supporting words checked by code, code facts only when they test the cause. Three-rubric table in 8.12 |
| 21 | Coordinator in code, parallel Readers, conditional Analyst, limits | 5.1 | 8.6 to 8.15 | Graph drawing, run log, timeline | ✅ real Reader, Checker and Tree of Thought Analyst in the graph on 16 papers, conflicts at every layer, windows per method, widening, MCP tools |

## Memory and guardrails

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 22 | Clarification step (grade, machine, layer thickness) | 2.1 | 9.2 | "Stainless steel" request asks back | ✅ "stainless steel" request pauses and asks for grade, machine and layer thickness |
| 23 | Human approval interrupt, resume, reject | 5.1 | 8.8, 8.9 | Paused state, approve and reject runs | ✅ wiring |
| 24 | Persistent state (SQLite checkpointer), evidence store across runs | 2.1, 5.1 | 9.1 | Resume after kernel restart | ✅ SQLite checkpointer: paused run resumed by a fresh graph on a fresh connection. Evidence table in SQLite with SQL queries |
| 25 | Engineer-feedback memory changes a later run | 2.1 | 9.3 | Constraint (e.g. 400 W limit) filters run 2 | ✅ a 200 W limit from run 1 (LangGraph `SqliteStore`) filters run 2. A 400 W limit would change nothing |
| 26 | Widen to neighbouring layer thickness, mark "adjacent" | 2.1 | 8.14 | Sparse request widened | ✅ `widen_node`: fewer than 10 verified records meeting the request, one search at the nearest thinner and thicker layer (within 50 %), marked adjacent, never bounds. With the extension 10 records meet 30 µm (no widening). On v2 alone 7 do, and it widens to 20 and 40 µm |
| 35 | Clarity gate: exact number, tied to its sample, plain 316L (input-quality guardrail) | decision 11-08 | 6.8, 8.11 | Records left out with reasons, set-aside list at the approval pause | ✅ on the graph run (online 11-09), with check() cells after 8.11: L04 and E04 set aside (approximate values, or tied only through an energy density), E06 2 and 4 wt% TiC not plain 316L. E03, E05 and every table value pass. The set-aside list reaches the approval pause |

## Evaluation and traceability

| # | Capability | Promised in | Notebook | Evidence to show | Status |
|---|---|---|---|---|---|
| 27 | Hand-checked answer key | 1.1 | 3.11, `eval/` | CSV, checked by Chinmay | ✅ 93 checked rows (84 pre-filled by another model from the papers only, 9 typed by Chinmay), 1 pre-filled row fixed. No blind sample. Committed byte for byte (2026-11-08) |
| 28 | Extraction accuracy per field | 1.1, 5.1 | 10.1 | Accuracy table | ✅ graph, v2, L08 from Table 5: recall 0.87, precision 0.98, density 74 of 91 right, power 72 of 88, speed 74 of 86. Weakest: L08 cross-table lookups, which led to check 16 (37). After it (11-09): power 75 of 88, L08 power 9 of 18, all else unchanged. That gain is not blind, Part 10 shows before and after |
| 29 | Planted (corrupted) records caught | 1.1, 5.1 | 6.3, 6.4, 10.3 | Caught / missed table | ✅ 5 of 5 caught after the column check (4 of 5 before) |
| 30 | Prompt-only baseline vs agent | 2.1 | 3.8, 4, 10.1 | Same questions, both scored | ✅ prompt-only answer checked in code (3.8). Single agent at 30 µm: recall 0.65, 17 of 36 densities right, against the graph's 0.92 and 32 of 36. The single agent uses the older um label |
| 31 | Tree of Thought vs single thinking call | 4.1 | 7.2, 8.12, 10.2 | 2 to 3 conflicts compared | ✅ 5 cases: tree and single call agree on the cause in all five, also after the clarity gate (rerun 11-09). Three-rubric comparison in 8.12 |
| 32 | Multi-agent vs single agent (accuracy, calls, run time) | 5.1 | 4, 10.1, 10.4 | Comparison table | ✅ calls, tokens, time, Checker results and accuracy compared (10.1, 10.5). The graph: a third of the input tokens, about twice the output tokens, 32 of 36 densities at 30 µm against 17 |
| 33 | Every model call traced (prompt, reasoning, answer, tokens, time) and cached | conventions | 0.2, 0.3, 2.2 | Trace viewer cell | ✅ `ChatGLM` + `set_llm_cache` (SQLite backend) + `TraceRecorder` callback, JSONL per run, `show_trace`. Graph nodes are named automatically once real agents use `glm` |
| 34 | Every value in the recommendation links to paper and passage | 1.1 | 8.11, 11 | Recommendation with citations | ✅ Part 11 demo (online 11-09, replays offline): one request from clarification to cited windows per method within the remembered 200 W limit, conflicts explained, approval and resume, trace summary. Windows cite record ids with their chunk ids |
| 36 | Browser front end: request, question back, windows, evidence with citations, set-aside papers, conflicts with their tree outcome, reasoning per call, approve or reject that resumes the graph | decision 11-08 | 12, `app/` | The app, `tests/test_app.py` | ✅ Streamlit 1.67 over the Part 11 graph with an SQLite checkpointer (`data/app_runs.sqlite`) and the memory store of 9.3. No logic in the app: it runs the 40 notebook cells tagged `core`. App test (AppTest, offline, about 30 s): loads, asks back for the grade, shows L04 and E04 set aside, stops with the plain endpoint message at the Analyst, resumes with Try again, Archimedes window first, Reject without a comment refused, Approve resumes, decision in the SQLite checkpoint, limit in the memory store. Offline the approval part uses a stand-in Analyst until the online rerun caches the new tree answers |

Count on 2026-11-09 (after check 16 and the online rerun): 37 ✅, 0 🟡, 0 ⬜.
