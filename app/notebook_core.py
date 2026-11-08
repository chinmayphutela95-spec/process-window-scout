"""Load the agents from the notebook, so the app holds no project logic of its own.

The notebook tags every cell that only defines things (tools, retrieval, Reader, Checker, clarity gate, Tree of Thought,
graph builder, guardrails) with the cell tag "core". This module runs exactly those cells, in notebook order, in one
fresh namespace. Demos and model calls live in the untagged cells and never run here.
"""
import contextlib
import io
import os
import time
from pathlib import Path
from types import SimpleNamespace

import nbformat
import streamlit as st

REPO = Path(__file__).resolve().parent.parent
NOTEBOOK = REPO / "notebooks" / "process_window_scout.ipynb"
TAG = "core"


def core_cells(path: Path = NOTEBOOK) -> list[tuple[int, str]]:
    """(cell number, code) of every cell tagged "core", in notebook order."""
    nb = nbformat.read(path, as_version=4)
    cells = [(n, c.source) for n, c in enumerate(nb.cells)
             if c.cell_type == "code" and TAG in c.metadata.get("tags", [])]
    for n, src in cells:     # plain Python only: a magic (%pip, %%writefile) belongs in an untagged cell
        assert not any(line.lstrip().startswith(("%", "!")) for line in src.splitlines()), f"cell {n} has a magic"
    return cells


@st.cache_resource(show_spinner="Loading the agents from the notebook (about 30 s, once per app start)")
def load_notebook(path: Path = NOTEBOOK) -> SimpleNamespace:
    """Run the core cells once. Returns their names as attributes (nb.build_scout_graph, nb.SHORT, ...).
    st.cache_resource keeps the result for every later rerun and browser tab, so the embedding model, the paper
    library and the cache are loaded once per app start. What the cells print is kept in nb.startup_log."""
    os.chdir(REPO)                                 # the notebook finds the repository from the working folder
    os.environ.setdefault("MPLBACKEND", "Agg")     # matplotlib without a window: the app never draws with it
    namespace = {"__name__": "process_window_scout"}
    log, t0 = io.StringIO(), time.time()
    with contextlib.redirect_stdout(log):
        for n, src in core_cells(path):
            exec(compile(src, f"<notebook cell {n}>", "exec"), namespace)
    namespace["startup_log"] = log.getvalue()
    namespace["startup_seconds"] = round(time.time() - t0, 1)
    return SimpleNamespace(**namespace)
