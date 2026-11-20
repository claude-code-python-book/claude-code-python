# Chapter 16 sample: salesreport

- `salesreport/` is the sample project (a Git repository). Start with its README.
- `demos/` holds the small scripts behind the chapter's outputs:
  `traps.py` (silent pandas mistakes), `chained.py` (chained assignment in
  pandas 3), `draft_clean.py` (a typical first draft), `speed.py` and
  `memory.py` (timings and memory), and `nb/notebooks/explore-before.ipynb`
  (the first-look notebook from Section 2). `run_cells.py` runs a notebook's
  code cells top to bottom when Jupyter isn't available:
  `python demos/run_cells.py demos/nb/notebooks/explore-before.ipynb`.

Run the demos from this folder with the project's dependencies installed,
for example `cd salesreport && uv sync && cd .. && salesreport/.venv/bin/python demos/traps.py`.
