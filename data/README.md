# data/

Everything here is generated locally and not committed, with one exception:

- `llm_cache.sqlite` (committed): every model answer the notebook received, keyed by its prompt. With it the notebook
  and the app replay all model calls without a model endpoint. It holds prompts and answers only, no endpoint address
  or key.

The rest is re-created by running the notebook: the open-access papers (downloaded from Europe PMC on first use), the
vector database, the evidence and checkpoint databases, the traces and the extraction CSV files.
