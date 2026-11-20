# Capstone Checkpoint 6.1: Safety Guardrails, Evaluation and Human Intervention

*Text of the version submitted on 2026-11-16, copied from the submitted Word file.*

**Project:** Process Window Scout (AM-PWS), a research agent for selecting PBF-LB process parameters
**Project type:** Research Assistant

## 1. Purpose and threat model

Process Window Scout reads open-access 316L papers, extracts laser settings and densities with their source passages, checks them, explains conflicts and proposes a process window for my approval. Its worst failure is a wrong number that looks right and sends me to the machine with settings that give porous parts.

| Risk | Seen in my runs |
|---|---|
| Misread values | 32 unit slips, parameters taken from the wrong table |
| Incomparable evidence | one sample 18 points apart by two density methods, heat-treated samples labelled as-built |
| Overconfident output | a summary claimed a 6.08 point gap when the largest was 6.78 |
| Out-of-scope request | no paper in the library reports 60 µm layers |
| Runtime failure | the model endpoint dropped during a retry |
| Untrusted input | hidden instructions in a paper (not seen yet) |

## 2. Guardrails

The prompt asks, but code enforces. My guardrails are planned to sit at the four gates of the agent loop.

| Gate | Guardrail |
|---|---|
| G1 Input | If the request lacks the alloy grade, layer or machine power, the agent asks before searching. Only CC BY papers, filtered by alloy. Planned: a scan of paper chunks for instruction-like text. |
| G2 Plan | Numeric limits: target density, the lower of the machine's and my remembered power limit, one retry per record, three conflicts per run. |
| G3 Tools | Each agent gets only its own MCP tools. None writes or acts on a machine, and arithmetic stays in code. |
| G4 Output | 17 code checks per record (value in its cited passage, right row and column, condition matches label). A failed record gets one retry, then stays "not verified". Only verified as-built records set a window, one per density method. Code checks every number in the written summary. |

Every model call would be logged with its reasoning, tokens and time, and the state would ideally be saved after each step. Following the checkpoint 5's feedback, I will try to add a comparability status (COMPARABLE, CONDITION_DIFFERENCE or INSUFFICIENT_INFORMATION) from machine, laser and scan strategy, so setup differences are not reported as contradictions.

## 3. Evaluation

Code checks run on every case. My hand-checked answer key is rerun after every change, and each new failure becomes a test.

| Metric | Result so far |
|---|---|
| Recall and precision against my answer key (93 values) | 0.87 and 0.98 |
| Planted errors caught, correct records falsely flagged | 5 of 5, 0 of 134 |
| Window and summary numbers traced to a verified passage | all |
| Agreement with an independent reference on 7 new papers | density 56 of 56 |
| Against a single agent at 30 µm | 32 of 36 densities right against 17 |
| Escalation and approval rates | planned |

## 4. Human routing

Reading and checking run inside written limits but every window needs my approval and the agent never touches the machine. A record passes and would be logged, blocked, or would be held for me. Beyond the final approval, the agent would stop or flag a case for me when:

- the request is ambiguous, before any search,
- no verified record at my layer reaches the target ("for orientation only, not a recommendation"),
- a window rests on fewer than three records or one paper (planned),
- the best explanation of a conflict leads by under two points or rests on physics alone,
- two density methods disagree on one sample by more than one point,
- the endpoint is down, so only checked answers are replayed.

The approval screen is planned to be a short decision card: answer of the model after thinking, windows, then flags. A rejection needs a reason, and a limit I set is remembered for that machine.

## 5. Trade-offs

A missed error would mean a failed build, so I would end up accepting more false alarms. A synchronous approval would stall a high-volume agent, but hope is that one request would mean one build. Code checks beat a model judge on cost and repeatability and cannot be talked round, but they only catch what I anticipated.

In the end the project is more or less limited to the type of literature I decide to chunk, hopefully in future can extend it to more physics informed models which would work in tandem with this approach to give a realistic windows with low cost, low complexity (and likely low hallucination) and extensive guarrailing would make more sense.
