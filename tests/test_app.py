"""Smoke test of the Streamlit app (app/streamlit_app.py) with Streamlit's AppTest. About a minute, most of it loading
the agents from the notebook, so it is a script and not a notebook cell. Run it from the repository folder:

    ../.venv/Scripts/python tests/test_app.py

1. The app loads and shows the request box, the Run button and whether it is online or replaying.
2. The Part 11 request is asked back for the grade. After "316L" the run reaches the approval pause, or, when an answer
   is neither cached nor reachable, stops with the plain "needs the model endpoint" message. The short answer of 9.5
   comes before the window tables, every number in it is in those tables, the conflicts or the request line, and the
   evidence table, the set-aside papers and the conflicts sit in collapsed sections. Every window has its evidence line,
   and a thin-evidence flag is named in the approval question and in the answer.
3. A replayed run reaches approval, and Approve resumes the graph with Command(resume): the decision is in the SQLite
   checkpoint and the power limit in the memory store. If an answer the Analyst needs is missing offline, this part puts
   a stand-in Analyst into the session (the real one would need the endpoint). Everything else is the real graph,
   replayed from the cache.
4. My own request of 9 November at a layer the library does not have (60 µm): the machine question asks for power and
   spot, the page shows my limits and the default target, says there is no window at 60 µm, shows the orientation windows
   per neighbouring layer and method with the method-spread pairs, the answer says they are not a recommendation, and
   Reject resumes the graph.
Everything the test writes (its runs, traces and the limit) is removed at the end.
"""
import builtins
import dis
import re
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
MY_REQUEST = "What is the appropriate laser power and speed combinations that I should try if I want to print SS316L with 60 um layers?"
MY_MACHINE = "My machine's power limit is 500W and it can do between 60-100 um spot size"


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


def page_parts(at):
    """Every element of the main page in page order, with the label of the collapsed section it sits in (or None)."""
    def walk(node, label):
        for child in getattr(node, "children", {}).values():
            yield child, label
            yield from walk(child, child.label if type(child).__name__ == "Expander" else label)
    return list(walk(at.main, None))


def answer_on_page(at):
    """The answer text, its position and the numbers in it that the window tables, the conflicts and the request line
    do not show. The approval part (section 4) and the reasoning (section 5) do not count as a source."""
    parts = page_parts(at)
    kinds = [type(e).__name__ for e, _ in parts]
    start = next(i for i, (e, _) in enumerate(parts) if kinds[i] == "Markdown" and e.value == "**Answer**")
    text, shown = parts[start + 1][0].value, []
    for i, (e, label) in enumerate(parts):
        if kinds[i] == "Subheader" and e.value[:2] in ("4.", "5."):
            break
        if i != start + 1 and (label is None or label.startswith("Conflicts")):
            shown.append(e.value.to_string() if kinds[i] == "Dataframe" else str(getattr(e, "value", "")))
    first_table = next(i for i, k in enumerate(kinds) if k == "Dataframe")
    return text, start < first_table, sorted(nb_numbers(text) - nb_numbers(chr(10).join(shown)))


def nb_numbers(text):
    return notebook_core.load_notebook().numbers_in(text)


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
    if reached:
        check("the request line shows the machine's 200 W and the remembered 190 W", "max 200 W (machine), 190 W (remembered)" in page_text(at))
    aside = [e for e, label in page_parts(at) if label and label.startswith("Set aside") and type(e).__name__ == "Markdown"]
    check("the clarity gate set L04 and E04 aside, shown on the page", {"L04", "E04"} <= {e.value.split()[0].strip("*") for e in aside})
    if reached:
        answer, first, unseen = answer_on_page(at)
        print(f"     answer: {answer}")
        check("the short answer comes before the window tables", first)
        check("every number in it is in the window tables, the conflicts or the request line", not unseen)
        check("its caption says who wrote it", any(c.value.startswith(("Written by GLM-5.2", "Written by code")) for c in at.caption))
        lines = [m.value for m in at.markdown if m.value.startswith("Evidence, ")]
        check("every window has its evidence line under its table",
              len(lines) == len(at.dataframe[0].value) and all("Edges:" in x for x in lines))
        flagged = [x for x in at.dataframe[0].value["review"] if x]
        check("a thin window is named in the approval question and in the answer",
              not flagged or ("Thin evidence, needs review" in page_text(at) and "thin evidence" in answer.lower()))
        print(f"     flagged windows: {len(flagged)}")
        check("the evidence table, the set-aside papers and the conflicts are collapsed sections with their counts",
              all(any(e.label.startswith(t) and e.label.endswith(")") and not e.proto.expanded for e in at.expander)
                  for t in ("Evidence table (", "Set aside: density not clearly reported (", "Conflicts and the Analyst's explanation (")))
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
    at.number_input(key="limit").set_value(180)
    at.button(key="approve").click().run()
    check("no error after approving", not at.exception)
    check("the page shows the saved decision", any(e.value.startswith("Approved: test of the app") for e in at.success))
    check("and what was written to the memory store", any("Written by this decision" in m.value and "180" in m.value for m in at.markdown))
    runs = sqlite3.connect(RUNS_DB, check_same_thread=False)
    saved = SqliteSaver(runs).get_tuple({"configurable": {"thread_id": threads[0]}}).checkpoint["channel_values"]
    runs.close()
    check("the decision is in the run's last SQLite checkpoint (read with a new connection)",
          saved["approval"] == {"approved": True, "note": "test of the app: start in the middle of the window",
                                "limits": {"max_power_W": 180}})
    check("the limit is in the memory store under the machine's name", read_memory() == [(MACHINE, "engineer", {"max_power_W": 180})])

    print("4. A layer the library does not have (my own request of 9 November)")
    at4 = AppTest.from_file(str(APP), default_timeout=900)
    at4.run()
    at4.text_area(key="request").input(MY_REQUEST)
    at4.button(key="run").click().run()
    threads.append(at4.session_state["thread"])
    check("it asks only for the machine, with its maximum power and spot size",
          [t.key for t in at4.text_input] == ["ask_machine"] and "maximum laser power" in at4.text_input(key="ask_machine").label)
    at4.text_input(key="ask_machine").input(MY_MACHINE)
    at4.button(key="continue").click().run()
    text = page_text(at4)
    check("no error, and the run reached the approval pause", not at4.exception and any(b.key == "approve" for b in at4.button))
    check("the request line shows 60 µm, the 500 W limit, the spot range and that the target is the default",
          all(x in text for x in ("60 µm", "max 500 W", "spot 60 to 100 µm", "(default, you did not give one)")))
    check("it says plainly that there is no window at 60 µm", any("No window at 60 µm" in w.value for w in at4.warning))
    labels = [m.value for m in at4.markdown if m.value.startswith("**Orientation window:")]
    tables = [d.value for d in at4.dataframe[:len(labels)]]           # no window at 60 µm, so the orientation tables come first
    check("every orientation table names the layer it was measured at and says it is not a recommendation",
          labels and all(re.search(r"measured at \d+ µm, not at your 60 µm, for orientation only, not a recommendation", x) for x in labels))
    check("one row per density method in each orientation table", all(t["density method"].is_unique for t in tables))
    check("every orientation window has its evidence line",
          len([m for m in at4.markdown if m.value.startswith("Evidence, ")]) == sum(len(t) for t in tables))
    check("a pycnometry row stops below 1200 mm/s, where L08's two methods disagree",
          all(float(v.split(" to ")[1]) < 1200 for t in tables for m, v in zip(t["density method"], t["v (mm/s)"]) if m == "pycnometry"))
    check("the method-spread pairs next to it show L08 sample 4 at 1200 mm/s, 99.69 against 81.3 %",
          "81.3" in at4.dataframe[len(labels)].value.to_string() and "99.69" in at4.dataframe[len(labels)].value.to_string())
    evidence = next(d.value for d in at4.dataframe if {"window", "record", "condition"} <= set(d.value.columns))
    behind = evidence[evidence["window"].str.contains("orientation")]
    check("every record behind an orientation window is verified and as printed",
          len(behind) > 0 and all(s.startswith("verified") for s in behind["status"]) and not behind["condition"].isin(nb.POST_BUILD).any())
    check("the conflicts part says the Analyst was not needed, or shows its outcome for each conflict",
          "No conflicts among the evidence for this request" in text or "Outcome:" in text)
    check("the approval question says orientation, not recommendation", "not as a recommendation" in text)
    answer4, first4, unseen4 = answer_on_page(at4)
    print(f"     answer: {answer4}")
    check("the short answer comes first, says the orientation windows are not a recommendation, and shows no number "
          "the page does not", first4 and "not a recommendation" in answer4 and not unseen4)
    at4.text_input(key="note").input("test of the app: orientation only, I will run my own trials")
    at4.button(key="reject").click().run()
    check("Reject resumes the graph and the decision is saved", any(e.value.startswith("Rejected: test of the app") for e in at4.success))
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
