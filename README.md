# Process Window Scout (AM-PWS)

An autonomous research agent that recommends **process windows for metal 3D printing (PBF-LB)** from the
open-access literature, and tells you which published results to trust.

Given a request such as *"316L stainless steel, 200 W machine, 30 µm layers, target density above 99.5%"*,
the agent:

1. finds and reads relevant open-access papers (OpenAlex API);
2. extracts laser power, scan speed, hatch spacing, layer thickness and density, each with its citation;
3. checks every result for plausibility using three signals:
   - **source check**: is the value really in the cited passage?
   - **consensus**: what do other papers report at similar settings?
   - **physics band**: an analytical melt-pool model run across a range of laser absorptivities
     (weak evidence, never ground truth);
4. flags a result as an outlier only when consensus *and* the whole physics band disagree, explores
   likely explanations, and recommends a process window for the engineer to approve.

Capstone project for the Carnegie Mellon University School of Computer Science Executive Education
course on agentic AI systems (2026). Project type: Research Assistant.

## Status
In development: Part 1 (deterministic tools) of the project notebook is built and tested. See [`docs/decisions.md`](docs/decisions.md) for design decisions and the
model-choice log, and [`checkpoints/`](checkpoints/) for each course checkpoint.

| Checkpoint | Topic | Status |
|---|---|---|
| 1.1 | Scoping and initial agent design | Submitted |
| 2.1 | Agent design refinement | Submitted |
| 3.1 | RAG and retrieval design | Planned |
| 4.1 | Tree of Thought integration | Planned |
| 5.1 | Multi-agent architecture | Planned |
| 6.1 | Safety guardrails and human intervention | Planned |
| 7.1 | Final report and presentation | Planned |

## Repository layout
```
notebooks/     process_window_scout.ipynb: the whole agent, built and tested Part by Part
docs/          architecture, decisions, model-choice log
checkpoints/   course checkpoint write-ups and diagrams
data/          downloaded papers and generated databases (not committed)
```

## Design principles
- **Open-weight model** (GLM-5.2) served through an OpenAI-compatible endpoint, with thinking mode on and the
  model's reasoning shown at every step. Endpoint settings come from `.env` and are never committed.
- **The LLM never does arithmetic.** All numbers come from cited papers or deterministic Python tools.
- **Public data only:** open-access papers with reuse-permitting licenses.
- **Human in the loop:** no recommendation is final until the user approves it.

## Setup
*(to be completed as the code is built)*
```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
```
