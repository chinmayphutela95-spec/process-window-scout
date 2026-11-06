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

## Model-choice log
| Date | Role | Candidates | Result | Choice |
|---|---|---|---|---|
| 2026-10-09 | (plan) Extractor / Analyst | Qwen3-8B Q4 | not yet tested | first candidate |
| 2026-10-09 | (plan) Checker | different family ~4B (e.g. Gemma) vs Qwen3-8B self-check; Prof's AdditiveLLM2-OA | not yet tested | pending |
| 2026-10-09 | (plan) Embeddings | Qwen3-Embedding-0.6B, bge-m3 | not yet tested | pending |
| 2026-10-23 | Embeddings | Qwen3-Embedding-0.6B (local GPU, about 1.2 GB fp16) vs all-MiniLM-L6-v2 (course lab) | chosen before testing: no 256-token limit, runs locally; recall@5 comparison planned | Qwen3-Embedding-0.6B |
| 2026-10-22 | All agent roles (Extractor, Checker, Analyst) | GLM-5.2 hosted vs local Qwen3-8B Q4 | GLM-5.2 reachable, key valid, thinking on/off both work | GLM-5.2, thinking on; replaces the local plan above |

Original constraint (local plan, now superseded for the LLM): 8 GB VRAM → ~4-bit quantised models ≤ ~8B;
usable context about 8k to 16k tokens. Still relevant if embeddings run locally.
