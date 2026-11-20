*Text of the version submitted for Checkpoint 3.1, copied from the submitted Word file.*

# Capstone Checkpoint 3.1: Retrieval Design and Integration

**Project:** Process Window Scout (AM-PWS), a research agent for selecting PBF-LB process parameters

**Project type:** Research Assistant

## 1. Is retrieval needed?

Yes. The knowledge the agent needs lives in published papers, not in the model. For example, a model can quote typical 316L ranges, but not which study reported which density at which settings, and every value in this project must be traceable to its source. I am using locally hosted GLM-5.2, which accepts a very long context, so the papers could in principle be pasted into the prompt. I still chose retrieval: the context is re-sent at every agent step, facts in the middle of long contexts get missed, and the source check needs the exact passage behind each value.

## 2. How retrieval is integrated (still on-going)

| Level | Question it answers | Mechanism |
|---|---|---|
| Papers | Which open-access 316L studies exist? | Europe PMC search API |
| Passages | Where are the parameters and densities? | Semantic search over chunks |
| Conditions | At what layer thickness and hatch spacing? | Lookup of stated conditions in each source paper |
| Numbers | Which values match given settings? | SQL over an evidence table (next milestone) |

Each paper's full text is planned to be cached, chunked, embedded with Qwen3-Embedding-0.6B on the laptop GPU and stored in ChromaDB with its DOI, alloy and section or table. The prompt tells the model to use only the retrieved text, cite it for every number, give the layer thickness and hatch spacing behind each result, and say "not reported" otherwise.

## 3. Key design choices

- **Data source.** OpenAlex and Europe PMC
- **Chunking.** Sections are cut into 250-word windows with 50 words of overlap. Tables are never split (43 tables, one chunk each), since a parameter row means nothing without its header and units.
- **Embedding model.** Qwen3-Embedding-0.6B
- **Trial with Number of results.** Five passages, chosen by maximal marginal relevance (lambda 0.7) from 60 candidates, at most two per paper. For my test question, 19 of the 20 closest chunks came from one paper, which would otherwise look like agreement.
- **Stated conditions.** Power and speed only mean something together with layer thickness, but papers give it in the Methods text while results sit in tables. Retrieval returned the table without the sentence saying it was printed at 30 µm, so for each source paper the code must also extract the sentences that state a layer thickness or hatch spacing with a number.
## 4. How retrieval changes the output

I asked GLM-5.2: "For 316L at a layer thickness of 30 µm, which laser power and scan speed gave the highest relative density in these studies, and what density was reported?" Both answers and the model's reasoning are saved as a trace in the code files.

**Without retrieval**, it answered from memory with four "highly cited" studies, each with an exact power, speed and density at 30 µm, partly using hatch spacings it assumed. None of the four titles could be found in Crossref as written; at least one is a real paper with a reworded title. Over three runs (one without the 30 µm condition) it named three different sets of studies, and one reference appeared with two different titles and journals.

**With retrieval**, it answered with a table. The highest density is up to 99.97% in one study, with minimum porosity at 190 W and 700 to 800 mm/s, 30 µm layers and 90 µm hatch spacing; it adds that the paper does not tie the 99.97% to those exact settings. A second study, also at 30 µm but with 120 µm hatch spacing, reached 97.76% at 140 W and 100 mm/s, and the model noted that the different hatch spacings make the two not directly comparable. I checked both papers: the values, layer thicknesses and hatch spacings match.

Retrieval turned confident but unverifiable numbers into fewer, checkable ones with their process conditions. It cannot judge them, though: 97.76% at such a high energy density is a weak result for 316L, which is the job of the plausibility check in the next milestone.

## 5. Failure mode: the similarity trap

Semantic search ranks by meaning, not by alloy. I added one distractor paper on 25CrMo4 steel describing the same kind of experiment; without an alloy filter its tables entered the top ten for the 316L question, ahead of genuine 316L passages. A model would then use numbers from the wrong steel with a citation that looks valid. Still on-going but the design will have to manage this in three ways:

- the clarification step fixes the alloy and layer thickness first
- every chunk carries an alloy label, taken from the title first, and the search filters on it, so the distractor never appears
- The source check compares each passage's conditions with the request. That check is still needed, since one retrieved 316L table was about directed energy deposition, the right alloy but the wrong process.
## Appendix: retrieval trace for the 30 µm question (from the notebook)

| Rank (MMR order) | Similarity | Paper | Section or table |
|---|---|---|---|
| 1 | 0.756 | PMC12387571 (LPBF 316L for implants) | 2. Methodology |
| 2 | 0.735 | PMC13208960 (SLM Venturi nozzle) | Table 2: conditions and measured density |
| 3 | 0.701 | PMC12194911 (review, 316/316L) | 2. DED, SLM and EBM process parameters |
| 4 | 0.711 | PMC12387571 (LPBF 316L for implants) | 3. Results |
| 5 | 0.637 | PMC13073740 (melt pool model, 316L) | 4. Results |

Stated conditions added for the answer: PMC12387571, 30 µm layers, 90 µm hatch, 138 µm spot (2. Methodology); PMC13208960, 30 µm layers, 120 µm hatch (2. Experimental Setup). Without the alloy filter, two 25CrMo4 tables appear at ranks 6 and 8.
