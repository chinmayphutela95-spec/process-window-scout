"""Process Window Scout in the browser: the graph of Part 11 behind a small page.

Start it from the repository folder (see Part 12 of the notebook):
    ../.venv/Scripts/python -m streamlit run app/streamlit_app.py

All project logic comes from the notebook's "core" cells (notebook_core.py). This file only asks, shows and resumes.
Streamlit reruns this whole script after every click. What must survive a rerun lives in st.session_state (this
browser tab) or in the SQLite checkpointer (every run, also after a restart of the app).
"""
import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
from notebook_core import load_notebook  # noqa: E402

st.set_page_config(page_title="Process Window Scout", layout="wide")
nb = load_notebook()

RUNS_DB = nb.DATA / "app_runs.sqlite"     # the app's own checkpointer file: the notebook empties its demo files on every run
EXAMPLE = "Stainless steel on a 200 W machine, 30 µm layers, relative density above 99.5 %"   # the request of Part 11
TIERS = "A: a sentence from the papers, found word for word. B: a code check. D: only the melt-pool band. -: nothing."
nb.TRACER.print_chars = 90                # one short line per model call in the terminal, the full reasoning is on the page

s = st.session_state
s.setdefault("thread", None)              # the run this tab shows (a thread id of the checkpointer)
s.setdefault("step", 0)                   # how often this tab advanced the run (names the trace files)
s.setdefault("analyst", None)             # the Tree of Thought Analyst of this run, it keeps the trees for the page
s.setdefault("error", None)               # why the last step stopped, if it did
s.setdefault("memory_before", None)       # the memory store before my decision, to show what was written


# ---------- the graph: the notebook's builder with a SQLite checkpointer and the engineer's memory store ----------

def config() -> dict:
    return nb.run_config(s.thread, recursion_limit=40)      # same limit as the Part 11 demo


@contextmanager
def scout_graph():
    """The Part 11 graph (clarification, memory, one wider search), opened for one click and closed again,
    so no SQLite file stays locked while the notebook runs."""
    runs = nb.open_sqlite(RUNS_DB)
    memory_file = nb.open_sqlite(nb.STORE_DB, isolation_level=None)
    store = nb.SqliteStore(memory_file)
    store.setup()
    s.analyst = s.analyst or nb.ToTAnalyst()
    try:
        yield nb.build_scout_graph(nb.GLMReader(), s.analyst, nb.REAL_LIBRARY, checkpointer=nb.SqliteSaver(runs),
                                   judge=nb.check_record_full, guardrails=True, store=store, widen=True), store
    finally:
        runs.close()
        memory_file.close()


def advance(inputs) -> None:
    """Run the graph from where it stands until it pauses for me or ends, one line per node as it arrives."""
    s.step, s.error = s.step + 1, None
    nb.TRACER.start(f"{s.thread}-{s.step}")
    with st.status("The agents are working ...", expanded=True) as box, scout_graph() as (graph, _):
        try:
            for update in graph.stream(inputs, config(), stream_mode="updates"):
                for node, change in update.items():
                    entries = (change or {}).get("log", []) if node != "__interrupt__" else []
                    if node == "checker" and entries:
                        verdicts = [e["msg"].split(":")[0] for e in entries]
                        box.write(f"**checker** {len(entries)} records: "
                                  + ", ".join(f"{v} {verdicts.count(v)}" for v in sorted(set(verdicts))))
                    for e in entries if node != "checker" else []:
                        box.write(f"**{node}** {nb.SHORT.get(e['subject'], e['subject'])} {e['msg'][:200]}")
        except nb.ModelUnavailable:
            s.error = ("This step needs the model endpoint: an answer it needs is not in the cache and the endpoint is not "
                       "reachable. With the endpoint back, restart the app, open this run under Saved runs and press Try again.")
        except Exception as e:                                  # anything else: a short message without the address
            s.error = f"The run stopped: {nb.redact(f'{type(e).__name__}: {e}')[:300]}"
        finally:
            nb.TRACER.stop()
    st.rerun()                                                  # draw the page again from the saved state


def saved_state():
    """The run as the checkpointer saved it, the question it waits on (or None) and the memory for its machine."""
    with scout_graph() as (graph, store):
        snap = graph.get_state(config())
        machine = (snap.values.get("request") or {}).get("machine") or "any"
        memory = {k: v for item in store.search(("limits", machine)) for k, v in item.value.items()}
    waiting = next((i.value for t in snap.tasks for i in t.interrupts), None)
    return snap, waiting, machine, memory


def saved_threads() -> list[str]:
    if not RUNS_DB.exists():
        return []
    runs = nb.open_sqlite(RUNS_DB)
    try:
        return sorted({c.config["configurable"]["thread_id"] for c in nb.SqliteSaver(runs).list(None)}, reverse=True)
    finally:
        runs.close()


# ---------- sidebar: mode, saved runs ----------

st.sidebar.title("Process Window Scout")
if nb.LLM_OK:
    st.sidebar.success("Online: new questions go to the model, known ones come from the cache.")
else:
    st.sidebar.info("Replay: the model endpoint is not reachable, so every answer comes from the cache.")
st.sidebar.caption(f"{nb.LLM_CACHE.size()} model answers in the cache. Agents loaded from "
                   f"{len(nb.REAL_LIBRARY)} papers in {nb.startup_seconds:.0f} s.")
threads = saved_threads()
if threads:
    pick = st.sidebar.selectbox("Saved runs (SQLite checkpointer)", threads, index=None, placeholder="open a saved run")
    if pick and st.sidebar.button("Open"):
        s.thread, s.analyst, s.error, s.memory_before = pick, None, None, None
        s.step = len(list(nb.TRACES.glob(f"{pick}-*.jsonl")))     # new trace files continue the numbering
        st.rerun()
if s.thread and st.sidebar.button("New request"):
    s.thread, s.analyst, s.error, s.memory_before = None, None, None, None
    st.rerun()

# ---------- 1. the request ----------

st.title("Process Window Scout")
st.caption("From one request to an approved, cited process window. The model reads, code checks, I decide.")
st.subheader("1. Request")
request_text = st.text_area("What do you want to print?", EXAMPLE, height=70, key="request")
if st.button("Run", type="primary", key="run"):
    s.thread, s.step, s.analyst, s.memory_before = f"app-{datetime.now():%Y%m%d-%H%M%S}", 0, None, None
    advance({"request": nb.parse_request(request_text)})

if not s.thread:
    st.stop()                                                   # nothing else to show before the first run

snap, waiting, machine, memory = saved_state()
values = snap.values
remembered = ((values.get("recommendation") or {}).get("limit_sources") or {}).get("remembered")
st.caption(f"Run `{s.thread}`" + (f", read from the request: {nb.describe_request(values['request'], remembered)}"
                                  if values.get("request") else ""))
stalled = bool(snap.next) and waiting is None                 # stopped between two steps, not paused for me
if s.error or stalled:
    st.warning(s.error or "This run stopped before it finished, for example without the model endpoint.")
if stalled and st.button("Try again", key="retry"):
    advance(None)                                               # None = carry on from the last saved step

# ---------- 2. clarification ----------

if waiting and "ask" in waiting:
    st.subheader("2. The agent asks first")
    st.write(waiting["question"])
    answers = {f: st.text_input(q, key=f"ask_{f}") for f, q in waiting["ask"].items()}
    if st.button("Continue", type="primary", key="continue"):
        layer = answers.get("layer_um", "30").replace("µm", "").replace("um", "").strip()
        if not all(answers.values()):
            st.warning("Please answer every question.")
        elif not layer.replace(".", "", 1).isdigit():
            st.warning("The layer thickness must be a number in µm.")
        else:
            if "layer_um" in answers:
                answers["layer_um"] = float(layer)
            advance(nb.Command(resume=answers))

# ---------- 3. results: shown as far as the run got ----------

rec, records = values.get("recommendation"), values.get("records", [])
if records:
    req = values["request"]
    st.subheader(f"3. Windows at {req['layer_um']:g} µm, at least {req['target_density_pct']:g} %"
                 + (" (default)" if req.get("target_default") else ""))

    def window_table(windows):
        st.dataframe(pd.DataFrame([{"density method": w["method"], "records": w["records"], "papers": w["papers"],
                                    "P (W)": "{:g} to {:g}".format(*w["power_W"]), "v (mm/s)": "{:g} to {:g}".format(*w["speed_mm_s"]),
                                    "h (µm)": "{:g} to {:g}".format(*w["hatch_um"]), "records cited": ", ".join(w["cites"]),
                                    **({"spot outside your range": w.get("spot_outside", 0)} if rec.get("spot_range") else {})}
                                   for w in windows]), hide_index=True)

    if not rec:
        st.info("No window yet: the run has not reached the window step.")
    else:
        st.write(f"Status: **{rec['status']}**" + (f", headline bounds from **{rec['method']}** records" if rec.get("method") else "")
                 + (f". Power limit {nb.limits_text(rec['limit_sources']['machine'], rec['limit_sources']['remembered'])}, the "
                    f"lower one applies: {len(rec.get('blocked_by_limits', []))} records above {rec['limits']['max_power_W']:g} W left out"
                    if (rec.get("limits") or {}).get("max_power_W") else "") + ".")
        if rec.get("spot_range"):
            st.caption("Your spot range: {:g} to {:g} µm. ".format(*rec["spot_range"]) + f"{len(rec.get('spot_outside', []))} verified "
                       "records state a spot outside it. They are tagged in the evidence table, not left out, because most papers do "
                       "not report the spot.")
        if rec["windows"]:
            window_table(rec["windows"])
        if rec.get("orientation"):
            st.warning(f"No window at {req['layer_um']:g} µm: no verified record at this layer reaches the target. What follows was "
                       "measured at a neighbouring layer, for orientation only. It is not a recommendation.")
            for layer in sorted({w["layer_um"] for w in rec["orientation"]}):
                here = [w for w in rec["orientation"] if w["layer_um"] == layer]
                st.markdown(f"**Orientation window: {here[0]['label']}**")
                window_table(here)
        elif not rec["windows"]:
            st.warning(f"No window at {req['layer_um']:g} µm, and no neighbouring layer reaches the target either.")
        if rec.get("method_spread"):
            st.markdown("**Same sample, two density methods, more than 1 point apart.** Neither record sets a window, because I "
                        "cannot tell which density to trust.")
            st.dataframe(pd.DataFrame([{"paper": p["paper"], "sample": p["sample"], "layer (µm)": p["layer_um"],
                                        "P (W)": p["power_W"], "v (mm/s)": p["speed_mm_s"],
                                        "method A": p["method_a"], "density A (%)": p["density_a"],
                                        "method B": p["method_b"], "density B (%)": p["density_b"], "gap": p["gap"]}
                                       for p in rec["method_spread"]]), hide_index=True)
    widened = values.get("widened") or {}
    if widened.get("adjacent"):
        st.caption(f"One wider search at {', '.join(f'{t:g}' for t in widened['layers'])} µm: {len(widened['adjacent'])} records "
                   f"marked adjacent. They are shown in the table, never used as bounds.")

    role = {**{i: f"orientation ({w['layer_um']:g} µm)" for w in (rec or {}).get("orientation", []) for i in w["cites"]},
            **{i: "bounds" for i in (rec or {}).get("cites", [])}, **{i: "support" for i in (rec or {}).get("supporting", [])},
            **{i: "above machine limit" for i in (rec or {}).get("blocked_by_limits", [])}}
    outside = set((rec or {}).get("spot_outside", []))
    rows = [{"status": r["status"] + (", adjacent" if r.get("scope") == "adjacent" else ""),
             "window": ", ".join(x for x in (role.get(r["id"], ""), r.get("window_note") or "",
                                             "spot outside your range" if r["id"] in outside else "") if x),
             "paper": nb.SHORT.get(r["paper_id"], r["paper_id"]), "sample": r.get("sample_label"),
             "P (W)": r.get("power_W"), "v (mm/s)": r.get("speed_mm_s"), "h (µm)": r.get("hatch_um"), "t (µm)": r.get("layer_um"),
             "spot (µm)": r.get("spot_um"), "density (%)": r.get("density_pct"), "method": nb.method_key(r) or "not stated",
             "condition": r.get("condition"),
             "cited chunk": ", ".join(r.get("chunk_ids", [])), "source": r.get("source"), "reason": r.get("reason"),
             "record": r["id"]} for r in records]
    order = {status: n for n, status in enumerate(nb.STATUS_ORDER)}
    rows.sort(key=lambda x: (order.get(x["status"].split(",")[0], 99), x["window"] == "", x["paper"]))
    st.markdown("**Evidence table**")
    present = list(dict.fromkeys(x["status"] for x in rows))
    shown = st.multiselect("Statuses shown", present, default=present, key="statuses")
    st.dataframe(pd.DataFrame([x for x in rows if x["status"] in shown]), hide_index=True, height=320)

    if values.get("set_aside"):
        st.markdown("**Set aside: density not clearly reported**")
        for p in values["set_aside"]:
            with st.expander(f"{p['short']} {p['paper_id']}: {p['why']} ({len(p['reasons'])} records)"):
                for reason in p["reasons"]:
                    st.write(reason)

    st.markdown("**Conflicts and the Analyst's explanation (Tree of Thought)**")
    explained = {"|".join(e["ids"]): e for e in values.get("explanations", [])}
    if "conflicts" in values and not values["conflicts"]:
        st.write("No conflicts among the evidence for this request, so the Analyst was not needed.")
    for c in values.get("conflicts", []):
        e, (a, b) = explained.get("|".join(c["ids"]), {}), c["records"]
        st.write(f"{nb.SHORT[a['paper_id']]} {a.get('sample_label')} ({a['density_pct']} %, {nb.method_key(a) or 'method not stated'}) vs "
                 f"{nb.SHORT[b['paper_id']]} {b.get('sample_label')} ({b['density_pct']} %, {nb.method_key(b) or 'method not stated'}) "
                 f"at {c['layer_um']:g} µm" + (f", tagged {', '.join(c['tags'])}" if c.get("tags") else ""))
        if not e:
            st.write("Not explained yet: the run stopped before the Analyst finished.")
            continue
        cause = f"Favoured cause: **{e['favoured']}** (tier {e['tier']})." if e["favoured"] != "-" else "No cause has enough support."
        st.write(f"Outcome: **{e.get('band')}**. {cause} {e['explanation']}")
        tree = (getattr(s.analyst, "trees", None) or {}).get("|".join(e["ids"]))
        if tree:
            st.dataframe(pd.DataFrame([{"cause": x["id"], "points": x.get("score"), "tier": x.get("tier"),
                                        "in beam": bool(x.get("in_beam")), "what earned them": ", ".join(x.get("parts") or {})}
                                       for x in tree["branches"] if "score" in x]), hide_index=True)
    st.caption("Evidence tiers. " + TIERS)

# ---------- 4. approval ----------

if waiting and "recommendation" in waiting:
    st.subheader("4. Approve or reject")
    st.write(waiting["question"])
    note = st.text_input("Comment (needed to reject)", key="note")
    limit = st.number_input(f"Power limit of '{machine}' in W (optional, remembered for this machine)", min_value=0,
                            value=0, step=10, key="limit")
    approve, reject = st.columns(2)
    decision = None
    if approve.button("Approve", type="primary", key="approve"):
        decision = {"approved": True}
    if reject.button("Reject", key="reject"):
        if note:
            decision = {"approved": False}
        else:
            st.warning("Please say why in the comment.")
    if decision is not None:
        decision.update({"note": note} if note else {})
        decision.update({"limits": {"max_power_W": limit}} if limit else {})
        s.memory_before = memory
        advance(nb.Command(resume=decision))

if values.get("approval") and not snap.next:
    st.subheader("4. Decision saved")
    verdict = values["approval"]
    st.success(f"{'Approved' if verdict.get('approved') else 'Rejected'}"
               + (f": {verdict['note']}" if verdict.get("note") else "") + ". Saved in the run's last checkpoint.")
    st.write(f"Memory store for '{machine}': {memory or 'empty'}")
    if s.memory_before is not None:
        st.write("Written by this decision: " + (str(memory) if memory != s.memory_before else "nothing (only a power limit is remembered)"))

# ---------- 5. how the agents got there ----------

if values.get("log"):
    calls = [t for f in sorted(nb.TRACES.glob(f"{s.thread}-*.jsonl")) for t in nb.load_trace(f.stem) if "error" not in t]
    st.subheader("5. How the agents got there")
    with st.expander(f"Run log ({len(values['log'])} lines, one per node and record)"):
        st.dataframe(pd.DataFrame(values["log"]), hide_index=True)
    st.markdown(f"**Reasoning of every model call** ({len(calls)} calls, {sum(t['cached'] for t in calls)} replayed from the cache)")
    for t in calls:
        with st.expander(f"{t['agent']}: {'replayed' if t['cached'] else 'model call'}, {t.get('output_tokens')} tokens out"):
            st.text(t.get("reasoning") or "(no reasoning)")
