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

## Model-choice log
| Date | Role | Candidates | Result | Choice |
|---|---|---|---|---|
| 2026-10-09 | (plan) Extractor / Analyst | Qwen3-8B Q4 | not yet tested | first candidate |
| 2026-10-09 | (plan) Checker | different family ~4B (e.g. Gemma) vs Qwen3-8B self-check; Prof's AdditiveLLM2-OA | not yet tested | pending |
| 2026-10-09 | (plan) Embeddings | Qwen3-Embedding-0.6B, bge-m3 | not yet tested | pending |
| 2026-10-23 | Embeddings | Qwen3-Embedding-0.6B (local GPU, about 1.2 GB fp16) vs all-MiniLM-L6-v2 (course lab) | chosen before testing: no 256-token limit, runs locally; recall@5 comparison planned | Qwen3-Embedding-0.6B |
| 2026-10-22 | All agent roles (Extractor, Checker, Analyst) | GLM-5.2 hosted vs local Qwen3-8B Q4 | GLM-5.2 reachable, key valid, thinking on/off both work | GLM-5.2, thinking on; replaces the local plan above |
| 2026-11-07 | LangChain wrapper and structured output for all LLM roles (Reader, Analyst, ReAct baseline) | `ChatOpenAI` as is, `ChatGLM` subclass, raw `openai` client. Structured output: `json_schema`, `function_calling`, `json_mode` | `ChatOpenAI` loses the reasoning text. With `ChatGLM` all three methods correct on 2 test passages: json_schema 4 to 6 s, about 1,000 tokens, full reasoning. function_calling 2 s, 300 tokens, little reasoning. json_mode 3 to 10 s, needs the schema in the prompt. `bind_tools` and `create_agent` correct, 1 to 2 s per tool step | `ChatGLM` + `json_schema` (fallback `function_calling`) |

Original constraint (local plan, now superseded for the LLM): 8 GB VRAM → ~4-bit quantised models ≤ ~8B;
usable context about 8k to 16k tokens. Still relevant if embeddings run locally.
