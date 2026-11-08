"""Smoke test of the Streamlit app (app/streamlit_app.py) with Streamlit's AppTest. About a minute, most of it loading
the agents from the notebook, so it is a script and not a notebook cell. Run it from the repository folder:

    ../.venv/Scripts/python tests/test_app.py

1. The app loads and shows the request box, the Run button and whether it is online or replaying.
2. The Part 11 request is asked back for the grade. After "316L" the run reaches the approval pause, or, when an answer
   is neither cached nor reachable, stops with the plain "needs the model endpoint" message.
3. A replayed run reaches approval, and Approve resumes the graph with Command(resume): the decision is in the SQLite
   checkpoint and the power limit in the memory store. While the cache lacks the Tree of Thought answers of the clarity
   gate round, this part puts a stand-in Analyst into the session (the real one would need the endpoint). Everything
   else is the real graph, replayed from the cache.
Everything the test writes (its runs, traces and the limit) is removed at the end.
"""
import builtins
import dis
import sqlite3
import sys
import time
import types
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.sqlite import SqliteStore
from streamlit.testing.v1 import AppTest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "app"))
import notebook_core  # noqa: E402
APP = REPO / "app" / "streamlit_app.py"
RUNS_DB, STORE_DB, TRACES = REPO / "data" / "app_runs.sqlite", REPO / "data" / "engineer_memory.sqlite", REPO / "data" / "traces"
MACHINE = ("limits", "200 W machine")


def check(name, condition):
    assert condition, f"FAILED: {name}"
    print(f"  ok  {name}")


def page_text(at) -> str:
    """Every text the page shows, for the 'no address on the page' check."""
    parts = []
    for kind in ("title", "subheader", "markdown", "caption", "text", "info", "success", "warning", "error"):
        parts += [str(e.value) for e in getattr(at, kind)]
        parts += [str(e.value) for e in getattr(at.sidebar, kind)]
    parts += [e.value.to_string() for e in at.dataframe]
    return "\n".join(parts)


class StandInAnalyst:
    """Test only: answers every conflict with 'no supported explanation', without a model call."""

    def __init__(self):
        self.calls, self.trees = [], {}

    def invoke(self, key, conflict=None, records=(), **_):
        self.calls.append(key)
        return {"explanation": "stand-in Analyst of the app test", "favoured": "-", "tier": "-", "band": "Unresolved"}


def notebook_code(nb) -> list:
    """The code objects of every function and class method the core cells defined."""
    codes = []
    for obj in vars(nb).values():
        if isinstance(obj, types.FunctionType) and obj.__code__.co_filename.startswith("<notebook"):
            codes.append(obj.__code__)
        elif isinstance(obj, type) and obj.__module__ == "process_window_scout":
            codes += [f.__code__ for f in vars(obj).values() if isinstance(f, types.FunctionType)]
    return codes


def globals_read(code) -> set[str]:
    """Global names a code object reads, including its inner functions, lambdas and comprehensions."""
    names = {i.argval for i in dis.get_instructions(code) if i.opname == "LOAD_GLOBAL"}
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            names |= globals_read(const)
    return names


def memory_items(conn) -> list:
    return [(i.namespace, i.key, i.value) for i in SqliteStore(conn).search(MACHINE)]


def read_memory() -> list:
    """The engineer's limits for the 200 W machine, read with a connection that is closed again at once."""
    if not STORE_DB.exists():
        return []
    conn = sqlite3.connect(STORE_DB, isolation_level=None, check_same_thread=False)
    try:
        return memory_items(conn)
    finally:
        conn.close()


memory_at_start = read_memory()
threads = []
t0 = time.time()
try:
    print("1. The app loads")
    at = AppTest.from_file(str(APP), default_timeout=900)
    at.run()
    check("the app loads without an error", not at.exception)
    check("it shows the Part 11 request and a Run button",
          at.text_area(key="request").value.startswith("Stainless steel") and at.button(key="run").label == "Run")
    mode = " ".join(e.value for e in list(at.sidebar.success) + list(at.sidebar.info))
    check("it says whether it is online or replaying from the cache", "Online" in mode or "Replay" in mode)
    print(f"     loaded in {time.time() - t0:.0f} s, mode: {mode.split(':')[0]}")
    t1 = time.time()
    nb = notebook_core.load_notebook()                       # the app's cached copy (st.cache_resource), not a second load
    check("the test shares the app's loaded agents (one load per process)", time.time() - t1 < 2)
    missing = {g for code in notebook_code(nb) for g in globals_read(code) if not hasattr(nb, g) and not hasattr(builtins, g)}
    check("every global name the notebook's functions and classes read is defined by a core cell", not missing)

    print("2. The Part 11 request")
    at.button(key="run").click().run()
    threads.append(at.session_state["thread"])
    check("the vague request is asked back for the grade before any paper is read",
          [t.key for t in at.text_input] == ["ask_alloy"] and not at.dataframe)
    at.text_input(key="ask_alloy").input("316L")
    at.button(key="continue").click().run()
    check("no error after the answer", not at.exception)
    reached = any(b.key == "approve" for b in at.button)
    stopped = any("needs the model endpoint" in w.value for w in at.warning)
    check("the run reached the approval pause, or said plainly that it needs the endpoint", reached or stopped)
    print(f"     {'reached the approval pause' if reached else 'stopped at the Analyst: an answer is not in the cache'}")
    check("the clarity gate set L04 and E04 aside, shown on the page",
          {"L04", "E04"} <= {e.label.split()[0] for e in at.expander if "density not clearly reported" in e.label})
    check("the page shows neither the endpoint address nor the key", nb.redact(page_text(at)) == page_text(at))

    print("3. Approve and resume")
    if not reached:
        at.session_state["analyst"] = StandInAnalyst()       # test only: the real Tree of Thought needs the endpoint offline
        at.button(key="retry").click().run()                 # carries on from the last saved step (the Analyst)
        check("Try again resumed from the saved step and reached the approval pause", any(b.key == "approve" for b in at.button))
    check("the window table lists Archimedes first", at.dataframe[0].value.iloc[0]["density method"] == "Archimedes")
    at.button(key="reject").click().run()
    check("Reject without a comment is refused and the run keeps waiting",
          any("say why" in w.value for w in at.warning) and any(b.key == "approve" for b in at.button))
    at.text_input(key="note").input("test of the app: start in the middle of the window")
    at.number_input(key="limit").set_value(190)
    at.button(key="approve").click().run()
    check("no error after approving", not at.exception)
    check("the page shows the saved decision", any(e.value.startswith("Approved: test of the app") for e in at.success))
    check("and what was written to the memory store", any("Written by this decision" in m.value and "190" in m.value for m in at.markdown))
    runs = sqlite3.connect(RUNS_DB, check_same_thread=False)
    saved = SqliteSaver(runs).get_tuple({"configurable": {"thread_id": threads[0]}}).checkpoint["channel_values"]
    runs.close()
    check("the decision is in the run's last SQLite checkpoint (read with a new connection)",
          saved["approval"] == {"approved": True, "note": "test of the app: start in the middle of the window",
                                "limits": {"max_power_W": 190}})
    check("the limit is in the memory store under the machine's name", read_memory() == [(MACHINE, "engineer", {"max_power_W": 190})])
    print(f"All app tests passed in {time.time() - t0:.0f} s.")
finally:                                                     # leave the files as they were
    if threads and RUNS_DB.exists():
        runs = sqlite3.connect(RUNS_DB, check_same_thread=False)
        for t in threads:
            SqliteSaver(runs).delete_thread(t)
        runs.close()
    for t in threads:
        for f in TRACES.glob(f"{t}-*.jsonl"):
            f.unlink()
    if STORE_DB.exists():
        conn = sqlite3.connect(STORE_DB, isolation_level=None, check_same_thread=False)
        store = SqliteStore(conn)
        store.setup()
        for ns, key, _ in memory_items(conn):
            store.delete(ns, key)
        for ns, key, value in memory_at_start:
            store.put(ns, key, value)
        conn.close()
