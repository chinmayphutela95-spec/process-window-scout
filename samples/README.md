# Sample outputs

Real outputs of the final run, so the system can be reviewed without running anything. The notebook
(`notebooks/process_window_scout.ipynb`) is also committed with all its outputs.

## `graph_run_records.csv`

Every record the multi-agent graph extracted from the 23 papers (208 records). One row per sample and density value:
the settings (power, speed, hatch, layer, spot), the density and how it was measured, the sample's condition, where it
was found (`source`, `chunk_ids`, `value_as_printed`) and what the code Checker decided (`status`, `reason`).

| Status | Records | Meaning |
|---|---|---|
| verified | 165 | passed every code check, may set a window |
| incomplete | 28 | a setting the window needs is missing (for example no hatch spacing in the paper) |
| quoted | 6 | the value comes from another paper the authors cite, not their own experiment |
| unclear, not used | 3 | set aside by the clarity gate (approximate or untraceable density) |
| not plain 316L | 2 | a modified alloy (for example 316L with TiC) |
| not verified | 2 | still failed a check after one retry with the reason |
| other process | 1 | not laser powder bed fusion |
| no density | 1 | no density value for the sample |

## `trace_part11_demo.jsonl`

The trace of the end-to-end demo of notebook Part 11 (60 model calls: 42 Reader, 17 Analyst, 1 Writer). One JSON line
per call with the agent, the model, whether the answer was replayed from the cache, the time, the input, output and
reasoning tokens, the prompt, the model's reasoning, its answer and any tool calls.
