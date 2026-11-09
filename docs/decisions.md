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
- **2026-10-23** · Retrieval design for Checkpoint 3.1: retrieval is required even though GLM-5.2 has a
  very long context, because the context is re-sent at every agent step (cost and latency), facts in the
  middle of long contexts get missed, and the source check needs exact paper and page citations. Three
  levels: OpenAlex finds papers; semantic search over page-tagged chunks finds passages; SQL queries the
  extracted numbers. Chunks of about 250 words with 50 words overlap, tables kept whole; ChromaDB with an
  alloy metadata filter; top 5 with at most 2 chunks per paper and MMR (lambda about 0.7). · Lab 3.1's
  MiniLM truncates at 256 tokens and would cut parameter tables; the alloy filter addresses the main
  failure mode (a 304L or wrong-layer passage outranking the right 316L table).
- **2026-10-24** · Paper source switched from OpenAlex + PDF to **Europe PMC full-text XML**. · Publishers
  blocked 23 of 25 automated PDF downloads (HTTP 403); Europe PMC serves open-access full text through an
  official API with tables intact. Citations are section or table instead of page.
- **2026-10-24** · Library v1: 5 CC BY 316L papers with a parameter table plus one deliberate 25CrMo4
  distractor; alloy label from the title first, then mention counts (a 25CrMo4 paper mentioned 316L).
  Without the alloy filter the distractor's table ranked 7th for the 316L question; with it, never.
- **2026-10-24** · search_passages draws 60 candidates (not 20). · For the demo question 19 of the 20
  nearest chunks came from one paper, so the per-paper cap ran out of options. Also observed: a 316L DED
  table from a review paper is retrieved for an LPBF question, so a process label is needed next.
- **2026-10-24** · Demo question names the layer thickness (30 µm), and a deterministic `stated_conditions()`
  lookup adds, for each source paper, the sentences that state layer thickness, hatch spacing or spot size
  with a number (Methods first, sentences citing other work skipped). · Power and speed are meaningless
  without layer thickness; papers state it in Methods while results sit in tables, and semantic search
  (even restricted to chunks containing "layer thickness") kept returning the table without its condition.
  With the lookup the grounded answer reports layer thickness and hatch for every result and notes that
  90 vs 120 µm hatch makes two 30 µm results not directly comparable.
- **2026-10-26** · Model name set in the code (`GLM-5.2` default), server address and key stay in `.env`;
  `.env.example` added for anyone running the notebook. · Course guidance: graders should run the same model;
  the private endpoint details must never be committed.
- **2026-10-26** · Prefer established frameworks and libraries over hand-written code from here on
  (LangGraph for the agent loop and multi-agent flow, LangChain tool wrappers, ChromaDB, fastmcp), keeping
  each concept visible and explained in the notebook. · Less custom code to debug and maintain, closer to
  how agents are built in practice, and recommended by the course for multi-agent work.
- **2026-10-26** · MMR kept at lambda 0.7. · Test on 8 questions (no LLM): compared with plain ranking
  (lambda 1.0) under the same 2-per-paper cap, the 5 selected passages changed in 8 of 8 questions and drew
  on a different number of papers in 3 of 8 (demo question: 3 papers became 4). The cap alone does not
  explain the diversity.
- **2026-10-30** · Evidence quality becomes the centre of the next milestone (M4) and Checkpoint 4.1. ·
  All three graders (1.1, 2.1, 3.1) asked the same thing: how conflicting findings are resolved, how source
  reliability is judged, and whether extracted conditions are checked automatically. Planned design:
  - **Automated extraction checks (code, before any judgement):** (1) the value must appear verbatim in its
    cited passage (source check); (2) internal consistency: when a paper reports energy density, recompute
    P / (v h t) from its stated conditions and compare (Table 2 of the nozzle study: 140 / (100 x 0.12 x 0.03)
    = 389 J/mm3, as printed); (3) required conditions present: alloy, process (PBF-LB, not DED), layer
    thickness, hatch spacing, power, speed; missing ones are flagged, never guessed.
  - **Source reliability per record:** primary data from the study's own experiments ranks above values a
    paper quotes from other work or a review table; density method and number of samples reported; same
    process and alloy as the request; passes the consistency check.
  - **Conflict resolution:** compare only comparable records (same layer thickness and hatch band); if
    comparable records still disagree, a Tree of Thought step proposes explanations (powder, density method,
    machine and spot size, scan strategy, unit or reporting error), retrieves evidence for each, scores them
    with the explicit rubric (model judges each criterion, code sums the points), and reports the result with
    a confidence level. Both values stay visible to the engineer; nothing is silently dropped.
- **2026-11-06** · How the ToT thresholds and evidence types decide the outcome (answer to the 4.1 feedback).
  The search stops early only when an explanation is clearly ahead; otherwise it runs to depth 2 and the
  final scores fall into one of three bands:
  - **Resolved** (high confidence): best score >= 6 and lead >= 2 over the next.
  - **Competing** (medium): best score >= 3 but below 6, or the lead is under 2. The report shows every
    explanation within 2 points of the best, side by side, with the check that would separate them.
  - **Unresolved** (low): best score < 3. Both original values are shown with no explanation preferred.
  Points say whether the evidence supports an explanation; **evidence tiers** say how much to trust it:
  A = direct experimental observation reported in the study itself (measured porosity type, micrographs,
  stated method); B = deterministic code checks on the reported numbers; C = consensus of comparable studies;
  D = physics estimate (weak, withheld outside its valid range). An explanation can only be Resolved if it has
  at least one tier A or B item; physics-only support caps it at low. When two explanations score within
  2 points, the one with the higher best tier leads, but the other stays visible as the runner-up with the
  discriminating check (for example cross-section images for keyhole pores versus a CT or Archimedes density
  comparison). Nothing within the margin is dropped. · Grader asked how the thresholds interact and how
  experimental evidence is weighed against a physics estimate without losing a valid alternative.
- **2026-11-06** · Multi-agent architecture (Checkpoint 5.1): **three LLM agents plus a Coordinator written in
  code**, all in one LangGraph state graph. Reader (one per paper, parallel via `Send`, max 3 at a time),
  Checker (code checks first, then judges primary vs quoted data; sees record and passage, never the Reader's
  reasoning), Analyst (ToT generator and critic, only on conflicts flagged by code, max 3 per run).
  Coordinator = rule-based supervisor: request completeness, search plan, routing, limits; no model call.
  Communication only through the shared evidence table in graph state (records list with an `operator.add`
  reducer for the parallel Readers; each agent writes only its own fields; edges pass IDs and flags, not
  text). Protocols by stakes: one-way Coordinator to Reader, two-way Checker and Reader (structured reason,
  one retry, then "not verified", never silently accepted), brainstorming only inside the Analyst. Approval
  via `interrupt()` with a SQLite checkpointer; set `recursion_limit` and `max_concurrency` in the run config.
  Dropped roles: Planner, Searcher, Physics agent, Writer (fail the module's split rule: different tools or
  knowledge, parallel, independent check). LangGraph over CrewAI: routing depends on structured check
  results and needs explicit loops with hard limits; CrewAI's hierarchical manager lets an LLM choose the
  order. Same model (GLM-5.2) for all agents accepted for factual work; independence comes from code checks.
  Evaluate: multi-agent vs single agent on the same papers (accuracy per field, planted errors caught, calls,
  run time). · Module 5 lecture deck p. 12 rule, Lab 5.1 guidance (minimal set, cap loops, benchmark).

- **2026-11-06** · Coordination skeleton built (notebook Part 5, stub agents, tested offline). Choices made while
  building: the evidence table uses an **upsert reducer** `merge_records` (same record id updates, new id appends)
  instead of `operator.add`, so the Checker's verdict and a Reader's retry update one record rather than
  duplicating it; `operator.add` stays for the trace log. **Field ownership is enforced in code** (`write()` refuses
  fields an agent does not own; a Reader may only set status "extracted"). Conflict rule in code: verified records at
  the requested layer thickness whose energy densities are within 10 % but densities differ by more than 1
  percentage point (first values, to be tuned on real records). Window = span of verified records reaching the
  target, ids as citations. Agents' models are arguments of `build_scout_graph`, so M2b/M4 plug in GLM-5.2 without
  rewiring; offline tests use a `ScriptedModel` with fixed answers per (paper, attempt). In-memory checkpointer
  for now; SQLite later for pauses across restarts. `recursion_limit` 25 and `max_concurrency` 3 in every run
  config. · Module 5 squad lab patterns (reducer, Send, ScriptedModel, interrupt), Checkpoint 5.1 design.

- **2026-11-07** · GLM-5.2 through LangChain: `ChatGLM`, a subclass of `ChatOpenAI` with three overrides (notebook 2.2).
  · Spike with real calls (notebook 2.4). `ChatOpenAI` drops vLLM's `reasoning` field on purpose (its documentation
  says fields outside OpenAI's API are not kept), so the reasoning text was lost while the token count survived. The
  subclass copies it to `additional_kwargs["reasoning_content"]` (LangChain's key for DeepSeek and Ollama reasoning),
  times each call, raises `ModelUnavailable` at once when offline, and builds the cache key from the model name and
  settings. Structured output works with thinking on in all three methods (two made-up passages, every number
  correct). Chosen: `json_schema` for the Reader and the Analyst (the server enforces the schema and the model still
  reasons in full, 4 to 6 s and about 1,000 output tokens per extraction). Fallback: `function_calling` (2 s, 300
  tokens, but only 60 to 70 words of reasoning). `json_mode` is not used (the schema has to be pasted into the prompt,
  and one call took 10 s and 2,362 tokens). `bind_tools` and `create_agent` give clean tool calls and keep the
  reasoning at every step. The quotes the model returns are not verbatim (3 of 12 abridged with "..." or stitched from
  two sentences), so the Reader will cite a passage ID and code will check every number against that passage.
- **2026-11-07** · One cache and one trace for every model call, both standard LangChain hooks: `set_llm_cache` with my
  own SQLite backend on the `BaseCache` interface (`data/llm_cache.sqlite`), and a `TraceRecorder` callback handler that
  writes one JSON line per call to `data/traces/<run>.jsonl` (agent or node, prompt, reasoning, answer or tool calls,
  tokens, seconds of the real call, cached or not), with a `show_trace` viewer (notebook 2.3). · The ready-made
  `SQLiteCache` lives in `langchain-community`, which is being retired and warns about it. Three problems found and
  fixed while building: (1) LangChain's default key contains the server address, (2) LangChain sets `total_cost` to 0
  on a replayed answer, which changed the next step's key, so a tool loop missed the cache on its first replay (the key
  now uses only each message's type, text and tool calls, tested end to end: fresh two-step agent run, then an offline
  replay hit both steps), (3) opening the SQLite file anew for every call failed about 1 write in 15 on this laptop
  ("attempt to write a readonly database"), while one connection kept open never failed in 600 writes. Restart & Run
  All now replays every model answer without the endpoint (30 to 40 s).
- **2026-11-07** · Frozen library v2 (notebook 3a.9 and 3a.10): 10 x 316L plus the 25CrMo4 distractor, all CC BY, in the
  ChromaDB collection `papers_v2`, built with LangChain components (`RecursiveCharacterTextSplitter` counting words,
  250 and 50 overlap, `langchain_chroma.Chroma`, MMR retriever with the alloy filter, the 2-per-paper cap applied after
  MMR). Part 3a keeps `papers_v1` and `selection.json` unchanged, and the submitted 3.1 run is replayed from its trace
  with a check that today's retrieval returns the same passages and conditions. · Chosen for variety in the
  evaluation: layers of 20, 30, 40 and 50 µm (one paper also 70), Archimedes and image analysis on the same samples,
  pycnometry with as-built and HIP results, a review with quoted tables, a scan speed reported in m/s, and a paper with
  no measured density. Two exceptions to the "density in a table" rule are kept on purpose and documented:
  PMC12387571 (density only in text and figures, the 99.97 % side of the 4.1 test case) and PMC13073740 (simulation
  paper with quoted parameters and no density, so the right answer is "not reported"). The new `density_tables` test
  ignores energy, power and dislocation density and the alloy's own density in kg/m³, which the old
  `has_parameter_table` counted. `QwenEmbeddings` wraps the already loaded Qwen3 model in LangChain's `Embeddings`
  interface, because `HuggingFaceEmbeddings` would load a second 1.2 GB copy onto the 8 GB GPU.
- **2026-11-07** · The answer key is filled in by hand, independently of the agent (notebook 3a.11). Review sheets: one
  self-contained HTML file in `data/answer_key/` (tables rendered from the XML with merged cells, conditions and
  density-method sentences, Methods text). Empty template `eval/answer_key.csv` with fixed columns, instructions in
  `eval/README.md`. · Extraction accuracy only means something against a key the agent never touched.

- **2026-11-07** · Reader (notebook Part 3b, outline Part 5): GLM-5.2 with `json_schema` structured output into a
  Pydantic `Record` that holds every number **as printed with its unit**, `quantity` (relative density, porosity or
  none), the paper's sample label and the chunk ids it read from. Code converts units with Part 1's `convert_units` and
  turns porosity into density (the model never does arithmetic). The prompt (`ChatPromptTemplate`) carries the grounding
  rules, the density definition (measured relative density of parts, method, as-built or HIP) and source precedence
  (tables and text over abstract, measured over nominal, quoted marked, a printed mean over its replicates). The Reader
  reads a paper in **reading units, one per density table**, with the paper's parameter tables, stated conditions and 4
  best passages as context (budget 30,000 characters). · One call per whole paper timed out twice on L08 (about 80
  records, and the reasoning listed every record before the answer). Per table, all 24 calls parsed: median 12.5 s,
  103,084 output tokens (49 % reasoning) for 190 records. The traps behaved: L01 no density, L02 m/s converted, L04
  read from the text, L08 as-built and HIP, L10 tiny porosities copied as printed, L05 review quoted. Its typical mistake:
  values printed in µm tagged as mm (32 records), caught by the Checker and corrected on the retry.
- **2026-11-07** · Checker (Part 3b, outline Part 6), code only: (11) every printed number in the cited chunks, and in a
  row-per-sample table the density in that sample's own row. (14) P/(v·h·t) against a printed energy density (2 %),
  plus Part 1's typical ranges. (15) power, speed, hatch and layer present, primary or quoted, PBF-LB. Failures of 11 and
  14 go back to the Reader once with the reason, then "not verified". Incomplete, quoted, no density and other process
  are final statuses (re-reading would not change them), and only verified records feed conflicts and the window. ·
  The range check was added because P/(v·h·t) cannot see a speed and hatch swap (v·h is symmetric) and needs a printed
  energy density to see a unit slip. Origin and process are judged on the chunk that holds the density itself, after a
  parameter table that cites a dataset made L04's own measurements look quoted. Planted errors: 4 of 5 caught. Missed: a
  speed and hatch swap with both values in range (L02, 200 mm/s and 70 µm). Next: a column-position check.
- **2026-11-07** · Real Reader and Checker in the LangGraph graph (5.11) without rewiring: `reader_node` takes several
  records per paper, `route_after_check` sends a paper's rejected records back together (one call per paper), the
  Checker node takes `judge=check_record`, and a `PendingAnalyst` stands in without any model call. · Real run to the
  approval pause: 190 records, 33 sent back from 4 papers, 31 verified on the retry, 2 quoted literature rows "not
  verified", 4 fresh calls of 7 to 27 s. The provisional conflict rule flags 70 pairs among 39 verified 30 µm records:
  22 inside one paper (9 are one sample measured by Archimedes and by image analysis) and many pairing very different
  P, v and h that only share an energy density. L04 vs L07 is not flagged (10.5 % apart in energy density). The rule
  needs Chinmay's decision (same density method, closeness in P, v and h, not only E_v).
- **2026-11-07** · Engineering lessons. The trace file is also kept open for a run (appending by reopening failed now
  and then, the same Windows lock problem as the cache). The endpoint stays slow after a client gives up: two abandoned
  48,000-token requests left the next calls running at about 10 tokens per second for 20 minutes. So the Reader uses
  smaller units and a generous timeout (1,200 s) instead of retrying long calls.

- **2026-11-07** · Notebook renumbered to `docs/notebook-outline.md` (Parts 0 to 11). Each Part opens with its question,
  course concept, framework feature and evidence. Cache and trace moved to Part 0, the record schema to Part 4 (shared
  by the baseline and the Reader), the Reader is Part 5, the Checker Part 6, the Tree of Thought Part 7, the graph with
  the T1 to T5 wiring tests Part 8, guardrails Part 9, evaluation Part 10. · Agreed with Chinmay so every course concept
  has one visible place. No prompt or schema changed, so all cached answers still replay.
- **2026-11-07** · Single-agent baseline (Part 4): `create_agent` with `@tool` versions of `search_library`,
  `stated_conditions`, `energy_density` and `convert_units`, a `ToolStrategy` final answer (the records of 4.1 plus a
  window), 32,000 tokens, 1,200 s timeout, no retries, `recursion_limit` 60. · First half of capabilities 30 and 32.
  Result: 15 model calls, 355 s of model time, 434k input and 87k output tokens (the prompt grows with every tool
  result), 24 records at 30 µm from 5 papers, its own window 190 to 220 W, 700 to 800 mm/s, 90 to 120 µm. It skipped
  L06's image-analysis values and named density methods the Reader left blank. Accuracy follows with the answer key.
- **2026-11-07** · Comparability rule (Chinmay's decision): the strict rule is active. Same layer thickness, same
  condition (as-built or HIP, unknown allowed but marked), power and speed each within 10 %, hatch within 15 %, the same
  density method when both are known (unknown allowed but marked). One sample measured by two methods is a "method
  spread", not a conflict. Only pairs across papers go to the Analyst. The energy-density rule is kept only for the
  "before" count. · On the final records the old rule flagged 70 pairs (22 inside one paper), many pairing settings that
  only share an energy density. The strict rule flags 1 conflict across papers (L04 vs L07 at 190 W, 800 mm/s) and lists
  9 method-spread pairs (all L06, Archimedes against image analysis, gaps of 1.5 to 6.8 points).
- **2026-11-07** · Process window from one density method (Chinmay's decision): the bounds come from verified records
  measured by Archimedes where available (otherwise the most common known method). Records that reach the target by
  another or an unknown method are shown next to the window as supporting evidence and do not set its bounds. · Image
  analysis of a section reads denser than Archimedes on the same sample (L06: up to 6.8 points), so mixing methods
  widens the window with optimistic values. Recomputed 30 µm window: bounds from a single Archimedes record (L07 high-VED: 220 W, 725 mm/s, 120 µm hatch), with 6 records that reach 99.5 % by image analysis (L06 S6 to S9) or by an unstated method (L04 at 190 W, 700 and 800 mm/s) shown as support.
- **2026-11-07** · Answer-key scope (Chinmay's decision): L01 to L10 in full except L08, which is keyed only from Table
  5 (`eval/README.md`). The scoring code scores L08 only on records taken from Table 5. · Table 5 is the smallest L08
  table (18 rows, against 32 in Table 2 and 64 in Table 4) that still has what L08 is in the library for: as-built and
  HIP results of the same samples. Its HIP rows carry only the condition as a label, a realistic layout trap.
- **2026-11-07** · Main Tree of Thought test case: L04 vs L07 at 190 W and 800 mm/s (hatch 90 vs 100 µm, 99.96 % vs
  94.6 %). It replaces 97.76 % vs 99.97 % from Checkpoint 4.1, which are at 140 W, 100 mm/s and 190 W, 800 mm/s and are
  not comparable under the strict rule. Two method-spread pairs whose cause the papers state (L06 S1, L08 sample 4) serve
  as known-answer controls. · Under the strict rule L04 vs L07 is the only cross-paper conflict at 30 µm.
- **2026-11-07** · Column-position check added to check 11 (a number must sit under a header, or carry a unit, of its
  own field) and used by the graph's Checker (`check_record_full`). · It catches the speed and hatch swap that 6.3
  missed (planted errors 5 of 5 now). Two refinements removed its false alarms on the 190 real records (from 20 to 0):
  a table only counts for a field if it has a column for that field, and a number that is also in a cited table is
  judged there rather than in running text.
- **2026-11-07** · Tree of Thought built as in Checkpoint 4.1 (Part 7): generator, critic per branch with the rubric
  (the model judges, code sums), evidence gate (quotes must be found word for word), beam 2, depth 2, at most 9 calls,
  bands Resolved / Competing / Unresolved with evidence tiers. Results: both known cases pick "method" with the paper's
  own explanation quoted (Competing, +5, lead 3), and the single call agrees. L04 vs L07: the tree says "regime"
  (Resolved, +7, the hatch 90 vs 100 µm changes the energy density by 11 %), the single call says "method" (low
  confidence, no verified quote). L04's Methods state its porosity came from image analysis and its relative density
  from Archimedes, so the two values were probably measured differently. The tree's method branch never retrieved that
  sentence. · Lessons: per-branch retrieval is the weak point (the 4.1 risk "weak evaluation prunes the best branch"),
  and a method explanation can reach only +5 (text +3, check +2, since consensus and physics say nothing about methods),
  so it can never be Resolved with the 6-point threshold. Both need Chinmay's view before tuning. Once the Reader
  records L04's method, L04 vs L07 is no longer comparable (different known methods) and no cross-paper conflict is left.
- **2026-11-07** · Engineering lessons. A LangGraph graph invoked directly inside another graph's node waited forever (it
  inherits the outer run's context): the Analyst now runs the tree in a worker thread, which starts with a fresh
  context. `SqliteStore` needs an autocommit connection (`isolation_level=None`). Every SQLite file is opened with a test
  write and retried (the Windows read-only lesson of 0.3).

- **2026-11-07** · Reader fixes, made together in one rerun (5.1): the schema labels lengths `µm` instead of `um`, tables
  whose header prints a mean or average come with the focus table (L02's Table 5) and rule 5 says the mean may sit in
  another table, and the paper's own sentences on how it measured density come with every call (headed `method`) with a
  rule asking for the method of each value. · The first run tagged 32 µm values as mm (all caught by the range check),
  gave L02 27 replicate records because its means were in a table the Reader never saw, and left L04's methods blank.
  Result (v2 papers, strict rule, 8.13): records 190 to 135 (L02 27 to 9 with the printed means, L08 101 to 64), unit slips at the first attempt 32 to 1 (a quoted literature row of L09), records sent back 33 to 6, L04's three porosities now "image analysis". Under the strict rule L04 vs L07 is no longer a conflict (1 to 0). L08 Table 4 (16 samples x 4 values) is left out: every call on it ran past the 20-minute timeout (twice whole, once per half), and a unit that never answers cannot be replayed offline. Its as-built values are also in Table 2 and its HIP values for six samples in Table 5, the answer-key table.
- **2026-11-07** · The single agent (Part 4) keeps the record schema it was run with (label `um`), defined as a copy in
  4.2. · Rerun with the new label, its eleventh call ran past the 20-minute timeout in one runaway answer. It is a fixed
  comparison point, so I kept it as run. A call that times out now stops the agent, not the notebook.
- **2026-11-07** · Comparability, active rule (Chinmay's decision, evening): methods may differ inside a conflict pair, the
  difference is tagged as a candidate cause, conflicts are searched at every layer thickness, at most 3 pairs across
  papers go to the Analyst (requested layer first, then the largest gap), same-sample pairs stay method spread. The
  morning's strict rule is kept as `STRICT_RULE` for counting. · After the Reader fixes the strict rule dropped L04 vs
  L07 (image analysis against Archimedes), so the agent would never have explained the largest disagreement in the
  library. A method difference is a cause to explain, not a reason to look away. Tolerances (10 % power and speed, 15 %
  hatch) stay a judgement, with a sensitivity table in 8.12: 58 comparable pairs, 12 conflicts, 3 across papers at 10 / 15 %. At 5 % no pair across papers remains, at 20 / 25 % there are 28, so the choice matters and is shown as judgement.
- **2026-11-07** · Tree of Thought scoring (Chinmay's decision, evening): a verified quote counts per side of the pair (+3
  from each paper), a code fact earns points only if it tests the explanation (B3 methods for "method", B5 the lower
  record's own paper data and D3 the melt-pool band for "regime", B4 for "reporting"), and consensus and energy density
  are context only. Both papers' method and condition sentences are given to every branch and to the single call.
  Thresholds unchanged. · Session C showed that a method explanation could never reach Resolved (+5 at most) and that the
  method branch missed L04's method sentence because it depended on its own searches. Results: both known controls now reach "method", Resolved +8 (Competing +5 before). E06 vs L06 S9 (Archimedes 96.3 % against image analysis 99.53 %): method, Resolved +8. E06 vs L06 S9 Archimedes: regime +5, Competing. L04 vs L07: Competing, reporting +6 against method +5 (one sentence of L04 says it also used Archimedes, which cuts against "method"), single call: method (high). The first run of the new rubric exposed two gate bugs, fixed the same evening: quotes with an appended chunk id or a curly apostrophe were rejected, and a row of table numbers was accepted as a quote. The gate now accepts sentences only and ignores typography and appended ids.
- **2026-11-07** · One window per density method (Chinmay's decision, evening), side by side with record and paper counts,
  Archimedes first. The first window with a known method gives the headline bounds, the others are listed next to it.
  · Showing the windows side by side makes the method effect visible instead of hiding it in "supporting" records.
  30 µm, 99.5 %: Archimedes 165 to 220 W, 725 to 800 mm/s, 70 to 120 µm from 2 records (E03, L07), image analysis 150 to 250 W, 700 to 1100 mm/s from 8 records in 3 papers.
- **2026-11-07** · Library extension (Chinmay's decision, evening): six more CC BY 316L PBF-LB papers at 30 µm (E01 to E06,
  3.12), chosen the same way as v2 (Europe PMC full text, solid parts, density with parameters in a table or text;
  lattices, foams and a mislabelled superalloy paper left out). They feed only the window, the conflicts and the
  consensus, have their own Chroma collection (`papers_ext`) and short names, and are never scored. v2, its collection,
  the review sheets and the answer key are unchanged. · A window from one or two records is not a recommendation.
  E01 PMC9317792, E02 PMC8779437, E03 PMC10934583, E04 PMC9573657, E05 PMC12387858, E06 PMC10935024: 14 records, 7 verified (E02, E04 and E05 are incomplete: the Reader gave their densities but left power, speed and hatch empty. E05's parameter table heads its columns "P (W)" without the word power, so `parameter_tables` missed it and it never reached the context, an open fix). Verified records meeting the 30 µm request: 7 on v2, 10 with the extension.
- **2026-11-07** · Widening (capability 26, 8.14): when fewer than 10 verified records meet the request (requested layer and
  at least the target density), the Coordinator searches once at the nearest thinner and thicker layer thickness among
  the verified records (each at most 50 % away) and marks those records `scope = "adjacent"`. They are shown with the
  windows and never bound them. · Checkpoint 2.1 promised it, 5.1 limits it to one extra search round (the graph has no
  edge back into `widen`). I count records that meet the request rather than all records at the thickness (2.1's
  wording), because only those can support a window. With the extension exactly 10 records meet 316L, 30 µm, 99.5 %, so the graph does not widen. On v2 alone 7 do, and the wider search adds 20 µm (L10) and 40 µm (L09), both shown in 8.14.
- **2026-11-07** · MCP (capability 12, 8.15): one fastmcp server file written by the notebook (`%%writefile`), run as its
  own process over HTTP on 127.0.0.1, serving `search_passages`, `stated_conditions`, `energy_density` and
  `melt_pool_band`. Each agent gets only its own tools (`AGENT_TOOLS`), `consensus_lookup` stays a local tool because it
  reads the evidence table in the notebook's process. · `langchain-mcp-adapters` 0.3.2 needs mcp below 2.0 while fastmcp
  4.1 needs mcp 2.x (pip dry run), so a 15-line bridge does what its `load_mcp_tools` does (fastmcp `Client` plus
  `StructuredTool` with the server's schema). HTTP instead of stdio so the server and its embedding model start once.
  The calculation formulas now exist twice (Part 1 and the server), so a parity test checks they agree. The Analyst agent (`create_agent`, its three tools) called `energy_density` twice and `melt_pool_band` once through the server, and the server's call log shows them under its own process id. Server start about 8 s, first search loads the embedding model in about 17 s.
- **2026-11-07** · Documentation standard (Chinmay's request): every rule and threshold is stated with its value, reason,
  evidence and limitations where it is used. Part 0 has a "how the pieces fit" narrative and a rules and thresholds
  table, and each Part ends with "what this step showed". Added to `docs/notebook-outline.md`.

- **2026-11-07** · Public-repo cleanup (Session E): outputs print paths relative to the project root, the notebook
  progress-bar warning and the pip version notice (both printed the local install path) are suppressed, and examples
  use "a 200 W machine" instead of a machine brand (a request may name a machine by its power, `GENERIC_MACHINE`). A
  scan of every committed file found no local path, e-mail address or employer name in the current tree. The submitted
  checkpoint documents carry my name as author, which is intended. Older commits still contain the local path in three
  notebook outputs: the history needs a squash or filter before the repository goes public.
- **2026-11-07** · Symbol-plus-unit headers (Session E): a parameter table is one with a power column named by the word or
  by "P (W)" / "LP [W]" and a speed column, and the column check reads "P (W)", "v (mm/s)", "h (µm)", "t (µm)",
  "VED (J/mm³)" by symbol and unit, with the unit alone as a fallback only where it is unambiguous ("(µm)" names nothing).
  · E04's and E05's parameter tables were missed because their columns are named only by symbol, so the Reader never
  saw them. After: E04 and E05 records verified (4 of 4, were incomplete), E02 still incomplete: the Reader writes "core 200 W, 800 mm/s" into its notes but leaves the fields
  empty, and the paper's parameter sentence gives no hatch, so the record would stay incomplete anyway, column check on v2 still 0 false alarms (133 pass, 1 n/a). Side effect: L04's tensile-specimen
  table is now in L04's context, and the Reader merged "190 W, 700 to 800 mm/s" into one record without a speed.
- **2026-11-07** · Support gate for the critic (Session E): a verified quote is not support by itself. The critic copies the
  few words of its quote that show the cause, code checks they are in the quote and contain a real word, and a caption or
  a row of numbers never counts. The same gates apply to the single call. Chunk ids written before or after a quote are
  ignored. · In Session D a table caption earned +3 for "reporting" in L04 vs L07. Results (Session D, now): L06 S1
  method Resolved +8, Competing +5 (the critic found a supporting sentence for the Archimedes side only). L08 sample 4 method Resolved +8, unchanged.
  E06 vs L06 S9 image analysis method Resolved +8, Competing +3. E06 vs L06 S9 Archimedes regime Competing +5, unchanged.
  L04 vs L07 on L04's Session D record reporting Competing +6, method Resolved +8, as the single call. Tree and single
  call agree on all five cases.
- **2026-11-07** · Robustness (Session E): Reader calls stop after 10 minutes and are retried once (a runaway answer ends on
  another try, as L04 did), a unit that fails or is missing from the cache offline costs that unit only, and a tree call
  that fails (an answer cut at the token limit) counts as no answer for that branch. · The first Session E run lost L04 to
  a 20-minute runaway and a tree call hit the 16,000-token limit with a degenerate answer.
- **2026-11-07** · Single agent stays on the Session C schema (Session E, item 4): tried once more with the `µm` label and the
  same 20-minute timeout. Calls 1 to 10 replayed, call 11 answered in 46 s, call 12 ran past the timeout. Part 4 and Part
  10.1 state that the baseline uses the older label and why.
- **2026-11-07** · Part 10 as one section per question (Session E): multi-agent vs single agent, tree vs single call, planted
  errors, Checker results, accuracy per (paper, field) on v2 only, the chunking experiment and fine-tuning. Chunking
  experiment (capability 5): recall@5 of the chunks holding the true density value, one search per value inside its
  paper, plain similarity (no MMR) so only the chunking differs. On the provisional key (96 Checker-verified v2 values):
  v1 windows tables whole 0.75, v1 tables split 0.77, v2 splitter tables whole 0.76, v2 tables split 0.71. The cell
  switches to `eval/answer_key.csv` when it has rows. · The differences are small, so the Checkpoint 3.1 choice (tables
  whole) stands until the real key says otherwise.
- **2026-11-07** · Part 11 end-to-end demo (Session E): "Stainless steel on a 200 W machine, 30 µm layers, relative density
  above 99.5 %" through the full graph with clarification, memory and widening: it asks for the grade, applies the 200 W
  limit remembered in 9.3 (52 records above it left out), explains two conflicts and pauses for approval, then resumes.
  48 model calls (all replayed), one line of reasoning per call so it fits on screen, trace summary at the end.

- **2026-11-08** · Notebook text shortened (Session F, markdown only): about 18,500 words to about 7,000. Each Part opens
  with one sentence linking it to the previous Part and four one-line bullets, each subsection says what it does, why
  and what to look at, and each Part ends with two lines of "what this showed". Part 0 gained a glossary of agent words
  and a 15-minute reading guide, and the rules table keeps a short reason per rule. · Chinmay ran the notebook in VS
  Code and found it hard to follow. Details that left the notebook and were not recorded here before:
  `ChatGLM` sets `disable_streaming=True` so every call takes the same path through its overrides, and LangChain's
  `content_blocks` view does not show GLM's reasoning, so `reasoning_of` is the one place it is read. The cache keeps
  one SQLite connection because reopening the file failed about one time in fifteen (most likely the virus scanner
  holding it). The 2-per-paper cap is applied after LangChain's MMR retriever, which has no per-paper limit (it returns
  15, the cap keeps the first 5 that respect it). Energy density is coarse (Bertoli et al., 2017). The old check
  `has_parameter_table` also accepted energy-density tables, so the frozen library uses `density_tables`. A new
  `thread_id` means a fresh evidence table, reusing one continues the old run. LangGraph's default `recursion_limit` in
  this version is above 10,000, so `run_config` always sets one. The LangGraph vocabulary table of Part 8 became the
  glossary in Part 0.

- **2026-11-08** · Answer key pre-filled by a different model, then checked row by row by me (my proposal, agreed
  2026-11-08). Claude (Opus 5.5) read only the papers' XML, the review sheets and `eval/README.md`, never the agent's
  outputs, and wrote `eval/prefill/answer_key_prefill.csv` (93 rows, 32 marked "check") with the exact location and the
  printed string of every value. That file stays frozen, so the difference to the final key measures the pre-fill's
  errors. I check every row against the paper (`checked` = ok or fixed) and add notes where needed. Only checked rows
  are scored. A blind sample was planned, but I used the pre-fill as a starting point for L07 and L03 as well, so the
  pre-fill's quality is reported as the share of rows I had to fix. · Typing about 90 rows by hand would take hours I do not
  have. A pre-fill by GLM-5.2 would share the Reader's blind spots and flatter its score, so the pre-fill comes from a
  different model family, and the rows I fix give a number for how far it can be trusted.

- **2026-11-08** · Clarity gate (Chinmay's decision): a step right after the Checker, a named graph node (`clarity`) before
  the wider search, the conflict search and the windows. Pure code, no model call, run on every value: (1) exact number,
  none of approximately, approx., about, around, nearly, roughly, up to, below, above, less than, more than, over,
  under, higher than, greater than, lower than, at least, at most, ~, ≈, <, >, ≤, ≥ among the few words before the
  printed value, in text and in table cells. (2) A value from running text sits in a sentence that names the sample,
  its power or its speed as printed. A link only through an energy density does not count. Table values pass rule 2,
  because check 11 already proves the row. (3) Plain 316L: no nonzero additive in the sample label (2 wt% TiC). A
  failing record stays visible as "unclear, not used" or "not plain 316L" with its reason and is never used for bounds,
  conflicts or consensus. A paper with no usable record left is listed as "set aside: density not clearly reported",
  in the run report and in the interrupt payload at the approval pause. · Per value and not per paper, because a
  paper rule ("no density table, skip") would also drop E03 to E06, which print exact values in their text and carry
  most of the 30 µm Archimedes evidence (E03 I-67° 99.86 %, E05 S1 99.68 % and S2 99.99 %). On the current records
  the gate leaves out exactly the expected six: L04 0.04 % ("approximately") and 2 % ("about"), so L04 is set aside,
  E04 samples 1 and 8 (tied only through 155 and 79 J/mm³), so E04 is set aside too (it has no other record), and
  E06's 2 and 4 wt% TiC rows. The 30 µm Archimedes window does not change (165 to 225 W, 600 to 800 mm/s, 4 records),
  the "not stated" window from E04 disappears, and the conflict search still finds the two E06 against L06 S9 pairs. Their
  trees change, because E06's own-paper regime check no longer compares plain 316L with its TiC composites. E03, E05 and the E06
  plain 316L row pass, and no table value changes. I added five bound phrases to the agreed list (higher than, greater
  than, lower than, at least, at most), for the same reason as "above" and "below".
- **2026-11-08** · Plain-316L filter (Chinmay's decision), part of the clarity gate: a sample with a nonzero additive is
  not plain 316L evidence. "316L (0 wt% TiC)" is the plain control and stays. · E06 says so itself (3.12), but its 2 and
  4 wt% TiC rows were verified and used in the consensus and in E06's own-paper regime check.
- **2026-11-08** · Streamlit UI: go (Chinmay's decision), built after the clarity gate and the scoring, as a small app over
  the existing graph: request form, run or replay from the cache, windows per method, evidence with citations and
  status including the set-aside list, conflicts with their verdicts, approve or reject (which resumes the graph). The
  notebook stays the single source of the logic.
- **2026-11-08** · Streamlit UI built (Part 12, `app/`). How the app gets the code: every notebook cell that only defines
  things carries the cell tag `core` (40 cells). `app/notebook_core.py` reads the notebook with nbformat and runs exactly
  those cells once, in notebook order, in one namespace, inside `st.cache_resource` (about 25 s, once per app start).
  The app (`app/streamlit_app.py`) calls the same `parse_request`, `build_scout_graph` (clarification, memory, wider
  search, as in Part 11), `Command(resume=...)` and `redact` as the notebook. To make this possible, 14 cells that ended in
  a demo were split in two (definitions tagged, demo untagged). The code text only moved, with two exceptions:
  `STATUS_ORDER` moved up three lines in 6.7, and in 9.2 `STORE_DB = fresh_file(...)` became the path plus a separate
  `fresh_file(STORE_DB)` in the demo half. A check in 12.1 keeps core cells free of magics, model calls, graph runs and
  traces, and checks that every name the app takes from the notebook is defined in a core cell. The app test checks that
  every global the core functions read is defined. · Alternatives: (a) run the whole notebook at app start: about
  100 s, and it repeats every demo and replays every model call. (b) Move the code into a package: two copies of the
  truth, or a notebook that only imports, which hides the code the course wants to see. (c) `%%writefile` the logic
  into a module, as for the MCP server: the server needs its own process, the app does not, and a second copy of the
  agents would drift. The app file holds only page code, so it is a normal committed file, not written from the
  notebook. · Same graph and memory as Part 11, but checkpoints go to `data/app_runs.sqlite` (SQLite, so a paused run
  can be opened again after a restart, as in 9.1). The notebook empties its own demo files on every run, so the app
  keeps its own. The memory store is the engineer's file of 9.3 (`data/engineer_memory.sqlite`), and the app opens both
  files for one click and closes them again, so it never locks them while the notebook runs. Replay mode is the
  notebook's offline mode: every answer from the LLM cache, and a missing one stops the step with "this step needs the
  model endpoint" (Try again resumes from the saved step). Errors are shown through `redact()`, never with the address.
  · Testing: `tests/test_app.py` with Streamlit's AppTest, a script and not a notebook cell, because loading the agents
  takes about 25 s and a notebook cell would load a second embedding model next to the kernel's. Until the online rerun
  caches the Tree of Thought answers of the clarity gate round, the real Analyst cannot finish offline, so the test's
  approval part puts a stand-in Analyst into the session (test only, the app has no hook for it). Installed with the
  venv's pip: streamlit 1.67.0 (it brought pandas 3.1.1, pyarrow 26.0.1, altair 6.3.0, pydeck 0.9.3, watchdog 7.1.0).
- **2026-11-09** · Check 16, one sample, one parameter set (Chinmay's decision, code in 6.4, part of `check_record_full`).
  If the paper has a parameter table (a table whose header names power and speed) with a row for the record's sample,
  the record's power, speed, hatch and layer must equal that row, as printed or after a factor of 1000. A failure goes
  the normal way: one retry to the Reader with the reason (both values and both tables), then "not verified". Guards
  against false alarms: if the record's own table prints its parameters, that row decides and no other table is
  asked, because a paper may reuse a label for another study. A label found in two parameter tables, or in none, is not
  judged. A trailing HIP, HT, annealed or stress relieved is dropped from the label ("13 HIP_1" is sample 13), because a
  post-treatment does not change how the part was built. "This work sample 13 SLM" (L08 Table 8) and "Sample 5, ROI R1"
  (Table 6) are not matched to Table 1: their values are right, and a looser match would invite false alarms. · Found by
  the evaluation (10.5): for L08 sample 13 the Reader took 200 W from another row of Table 1, where sample 13 has 350 W.
  The number was in the cited passage and in the power column, so checks 11 and the column check passed. On the
  Reader's first attempt (148 records) check 16 judges 89 records and flags exactly three, all L08 sample 13 from Table 5
  (as-built, HIP_1, HIP_2), each 200 W against Table 1's 350 W. All three are real errors: my checked key gives sample
  13 350 W in each row. In the graph the three went back to the Reader once with the reason, and the retry corrected
  all three to 350 W, so they ended verified. Because the check came from the evaluation, the scores after it are no
  longer a blind measure. Part 10 shows both. Before (run of
  7 November, scored 8 November): recall 0.87, precision 0.98, power 72 of 88, L08 power 6 of 18. After (run of
  9 November): recall 0.87, precision 0.98, power 75 of 88, L08 power 9 of 18, every other field unchanged.

- **2026-11-09** · Online rerun after the clarity gate and check 16: Restart & Run All online twice, then fully offline.
  Tree results on the two conflicts the gate changed. E06's own-paper regime check no longer has the TiC rows, so the
  E06 side gets no regime fact. (1) E06 316L 96.3 % by Archimedes against L06 S9 99.53 % by image analysis (both 180 W,
  30 µm, 100 against 90.9 J/mm³): method, Competing, +5 (a method sentence from each paper +6, the code check that the
  methods differ +2, a contradicting quote -3), lead 4. The single call also says method. Physically sensible: L06
  measured the same S9 part at 94.6 % by Archimedes, so with matched methods the gap reverses, and one polished section
  misses pores outside its plane. The -3 is a weak spot: the critic took L06's sentence that it used Archimedes as a
  contradiction, though the 99.53 % is L06's image-analysis value. So method is understated and Competing is cautious.
  (2) E06 96.3 % against L06 S9 94.6 %, both by Archimedes: regime, Competing, +5 (L06's sentence that an energy density
  above 90 J/mm³ is recommended +3, the code check that S9 sits on its paper's lack-of-fusion side +2), lead 5. The
  single call also says regime. Plausible in direction, since S9 sits right at its own paper's threshold and E06 is 10 %
  higher, but weak: the gap is 1.7 points, close to the scatter of Archimedes on porous parts, both parts are below
  97 %, and E06 at 100 J/mm³ is porous too, which an energy density alone does not explain. Competing is the right band.
  Machine and powder found no sentence in either paper and scored -2. I did not tune anything. · Why two online runs: in
  the first, the method critic of pair 1 stopped at the token limit, so that branch had no answer and pair 1 came out
  Unresolved (reporting +1). Part 9 ran the same tree again, the call succeeded and was cached. A failed call is never
  cached, so a rerun can change a tree. The second online run replayed every call (0 new, 0 errors), and 8.11, Part 9
  and Part 11 now show the same trees. Run times: first online 317 s (8.11 graph run 143 s, 10 new model calls: the L08
  retry, 8 tree calls and one single-call comparison), second online 138 s, offline 149 s with 0 skipped cells (350
  checks offline, 352 online, the two extra are the live call of Part 2). · Windows at 30 µm and 99.5 %: Archimedes 165
  to 225 W, 600 to 800 mm/s, h 70 to 120 µm (4 records, 3 papers), unchanged. With my stored 200 W limit (9.3, Part 11):
  Archimedes 165 to 175 W, 600 to 800 mm/s, h 70 to 120 µm (E03 I-67° and E05 S1), image analysis 150 to 180 W (4
  records, L06 only). The limit leaves out 54 verified records, among them E05 S2 (225 W) and L07 high-VED (220 W).
  The app (Part 12) now reaches approval with the real Analyst, online and offline, so its test no longer needs the
  stand-in. A browser run of the Part 11 request showed the same capped window and both trees with their points.

- **2026-11-09** · One retry for a cut-off Tree of Thought call (Chinmay's decision, `invoke_or_none` in 7.1). A generator,
  critic, follow-up or single call whose answer stops at the token limit (LengthFinishReasonError) or cannot be read (a
  JSON or schema error) is sent once more, as the same call. A second failure, or any other error, still counts as no
  answer for that branch. The trace names the second call "(retried after token limit)", and the tree log and the
  Analyst's run-log line say so too. · Why: in the first online run of 9 November the method critic of pair 1 stopped at
  the 16,000-token limit, and pair 1 fell from Competing to Unresolved in 8.11. A tree result hung on one failed call.
  · Why the same call, and not more tokens or a "keep it brief" note: the client fails before anything is cached, so the
  second try really goes to the model, and its answer is cached under the call's own key. Every later replay, online or
  offline, then gets that answer without a retry, so reruns stay stable. More tokens or a changed prompt would give the
  retry another cache key, so each online rerun would send the failing call again and could change the tree, and a
  changed prompt would also ask the critic a slightly different question. The 9 November cut-off was a one-off: the same
  call, sent again in Part 9, finished in 16 s. Timeouts are not retried, because one tree call may run 20 minutes.
  · Cut-off calls so far: the cache holds 110 tree calls (70 critic, 17 single call, 12 generator, 11 follow-up), all
  complete, the longest 11,503 of 16,000 output tokens. A cut-off is never cached, so the count comes from the runs: 2 in
  all online runs on record, one in the first Session E run (7 November, see above) and the method critic of pair 1 in
  the first run of 9 November.

- **2026-11-09** · Chinmay's own app test (run `app-20261109-112948`): "What is the appropriate laser power and speed
  combinations that I should try if I want to print SS316L with 60 um layers?", machine answer "My machine's power limit
  is 500W and it can do between 60-100 um spot size", rejected with "I asked for 60 um layers, all the results are shown
  for 30 um". The library has no 60 µm records (its layers are 20, 30, 40, 50 and 70 µm), and nothing was invented, but
  the app failed him four ways. Four fixes (Chinmay's decisions), plus one of mine:
  (1) Orientation windows. Adjacent records still never set the recommended window. But when the requested layer has
  none, `recommend_node` gives one window per neighbouring layer and density method from the adjacent records that
  reach the target, labelled "measured at 50 µm, not at your 60 µm, for orientation only, not a recommendation", next to
  the same-sample pairs at those layers whose two methods differ by more than 1 point. The status is "orientation only"
  and the approval question asks whether to accept them as a starting point for trials, not as a recommendation.
  (2) The Analyst gets only pairs at the requested layer and at the neighbouring layers the wider search used. This
  reverses part of the 11-07 rule "conflicts are searched at every layer": the search still covers every layer for the
  log and the method spread, but trees about 30 µm pairs did not help a 60 µm request. With no pair there, the log says
  "no conflicts among the evidence for this request" and the Analyst is skipped. The 30 µm demo keeps both of its
  conflicts, because they are at 30 µm (check in 9.4).
  (3) Machine facts in code: a power limit ("power limit is 500W", "500 W limit", "max 400 W", "up to 370 W") and a spot
  range ("60-100 um spot", "spot size of 70 to 90 µm") from the request or the machine answer. In the request a power
  counts only next to such a word, because "a 200 W machine" names the machine (so 9.3 still needs my stored limit). In
  the machine answer every power is the maximum, because the question now asks "Which machine, and its maximum laser
  power in W (spot size if you know it)?". The power limit works like a stored one (the lower wins), the spot range is
  shown, and a record whose stated spot is outside it is tagged, never left out, because most papers do not report the
  spot. The memory key is short ("500 W machine"), not the sentence.
  (4) A default target says so: "at least 99.5 % (default, you did not give one)".
  (5) Mine: HIP and heat-treated records never enter a window or an orientation window, though they stay in the evidence
  table. A furnace closes pores the print left, so such a density says nothing about the print settings. Without this,
  12 of the 28 records at 50 µm that reach 99.5 % were HIP rows of L08. At 30 µm there is no HIP record, so nothing
  else changes. · What his request shows now (offline replay with a scripted Analyst, 9.4): 500 W machine, max 500 W, spot
  60 to 100 µm, 60 µm, at least 99.5 % (default). No window at 60 µm. Orientation at 50 µm, L08 only, h 110 µm:
  pycnometry 8 records, 200 to 350 W, 650 to 1200 mm/s, image analysis 8 records, 200 to 350 W, 400 to 800 mm/s. Next
  to them the four L08 samples at 1200 mm/s whose methods disagree: 99.69 against 81.3 %, 99.48 against 84.69 %, 99.35
  against 91.22 %, 98.55 against 94.88 % (pycnometry against image analysis). So the pycnometry window's upper speed is
  exactly where image analysis sees lack-of-fusion pores that pycnometry misses, which L08 itself says. No conflicts
  among the evidence for this request. No record above 500 W. 22 verified records state a spot outside 60 to 100 µm,
  none of them in the orientation windows (L08: 70 µm).

## Model-choice log
| Date | Role | Candidates | Result | Choice |
|---|---|---|---|---|
| 2026-10-09 | (plan) Extractor / Analyst | Qwen3-8B Q4 | not yet tested | first candidate |
| 2026-10-09 | (plan) Checker | different family ~4B (e.g. Gemma) vs Qwen3-8B self-check; Prof's AdditiveLLM2-OA | not yet tested | pending |
| 2026-10-09 | (plan) Embeddings | Qwen3-Embedding-0.6B, bge-m3 | not yet tested | pending |
| 2026-10-23 | Embeddings | Qwen3-Embedding-0.6B (local GPU, about 1.2 GB fp16) vs all-MiniLM-L6-v2 (course lab) | chosen before testing: no 256-token limit, runs locally; recall@5 comparison planned | Qwen3-Embedding-0.6B |
| 2026-10-22 | All agent roles (Extractor, Checker, Analyst) | GLM-5.2 hosted vs local Qwen3-8B Q4 | GLM-5.2 reachable, key valid, thinking on/off both work | GLM-5.2, thinking on; replaces the local plan above |
| 2026-11-07 | LangChain wrapper and structured output for all LLM roles (Reader, Analyst, ReAct baseline) | `ChatOpenAI` as is, `ChatGLM` subclass, raw `openai` client. Structured output: `json_schema`, `function_calling`, `json_mode` | `ChatOpenAI` loses the reasoning text. With `ChatGLM` all three methods correct on 2 test passages: json_schema 4 to 6 s, about 1,000 tokens, full reasoning. function_calling 2 s, 300 tokens, little reasoning. json_mode 3 to 10 s, needs the schema in the prompt. `bind_tools` and `create_agent` correct, 1 to 2 s per tool step | `ChatGLM` + `json_schema` (fallback `function_calling`) |
| 2026-11-07 | Reader (structured extraction) | one call per paper vs one call per density table (reading units), both GLM-5.2 json_schema with thinking on | per paper: L08 timed out twice (600 s). Per table: 24 of 24 calls parsed, median 12.5 s, 190 records, 32 unit tags wrong (µm as mm), fixed on the retry | reading units, json_schema |
| 2026-11-07 | Single-agent baseline (Part 4) | `create_agent` + 4 tools + `ToolStrategy` | 15 calls, 355 s, 434k in / 87k out tokens, 24 records at 30 µm | kept as the baseline for capabilities 30 and 32 |
| 2026-11-07 | Analyst (Part 7) | Tree of Thought (generator + critic, GLM-5.2 json_schema, 16,000 tokens) vs one thinking call | known cases: both pick the right cause. L04 vs L07: tree regime (Resolved), single call method (low) | tree kept, retrieval per branch and thresholds to tune |
| 2026-11-07 | Reader with the three fixes (µm label, mean tables, method sentences) | same GLM-5.2 json_schema Reader, one call per density table | 23 of 24 units answered in 7 to 82 s, L08 Table 4 ran past 20 minutes three times (left out) | kept, L08 Table 4 open |
| 2026-11-07 | MCP client for LangChain | `langchain-mcp-adapters` 0.3.2 vs own bridge (fastmcp `Client` + `StructuredTool`) | adapter needs mcp below 2.0, fastmcp 4.1 needs mcp 2.x | own 15-line bridge |
| 2026-11-08 | Answer-key pre-fill (evaluation, not the agent) | typing by hand vs GLM-5.2 vs Claude Opus 5.5 | GLM would share the Reader's errors, hand typing too slow | Claude Opus 5.5, every row checked by me, quality = share of rows fixed |

Original constraint (local plan, now superseded for the LLM): 8 GB VRAM → ~4-bit quantised models ≤ ~8B;
usable context about 8k to 16k tokens. Still relevant if embeddings run locally.
