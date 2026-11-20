# Chapter 16 — Data Work: pandas, Polars, and Jupyter Notebooks

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`ch16-data-work-sample`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-listing-16-1-notebooks-explore-before-ipynb-code-cells.py`](snippets/01-listing-16-1-notebooks-explore-before-ipynb-code-cells.py) | Listing 16-1: notebooks/explore-before.ipynb (code cells) | python | 2. Claude Code and Jupyter: Reading and Editing Notebooks |
| [`02-output.txt`](snippets/02-output.txt) | Output | text | 2. Claude Code and Jupyter: Reading and Editing Notebooks |
| [`03-output.txt`](snippets/03-output.txt) | Output | text | 2. Claude Code and Jupyter: Reading and Editing Notebooks |
| [`04-prompt.txt`](snippets/04-prompt.txt) | Prompt | prompt | 2. Claude Code and Jupyter: Reading and Editing Notebooks |
| [`05-listing-16-2-the-data-rules-in-claude-md.md`](snippets/05-listing-16-2-the-data-rules-in-claude-md.md) | Listing 16-2: The data rules in CLAUDE.md | markdown | 3. Exploring a Dataset Safely (Sample First, Never Overwrite Raw Data) |
| [`06-listing-16-3-claude-settings-json.json`](snippets/06-listing-16-3-claude-settings-json.json) | Listing 16-3: .claude/settings.json | json | 3. Exploring a Dataset Safely (Sample First, Never Overwrite Raw Data) |
| [`07-listing-16-4-tests-test-raw-data-py.py`](snippets/07-listing-16-4-tests-test-raw-data-py.py) | Listing 16-4: tests/test_raw_data.py | python | 3. Exploring a Dataset Safely (Sample First, Never Overwrite Raw Data) |
| [`08-output.txt`](snippets/08-output.txt) | Output | text | 3. Exploring a Dataset Safely (Sample First, Never Overwrite Raw Data) |
| [`09-output.txt`](snippets/09-output.txt) | Output | text | 3. Exploring a Dataset Safely (Sample First, Never Overwrite Raw Data) |
| [`10-output.txt`](snippets/10-output.txt) | Output | text | 4. Cleaning and Transforming with pandas |
| [`11-listing-16-5-src-salesreport-load-py.py`](snippets/11-listing-16-5-src-salesreport-load-py.py) | Listing 16-5: src/salesreport/load.py | python | 4. Cleaning and Transforming with pandas |
| [`12-listing-16-6-src-salesreport-clean-py.py`](snippets/12-listing-16-6-src-salesreport-clean-py.py) | Listing 16-6: src/salesreport/clean.py | python | 4. Cleaning and Transforming with pandas |
| [`13-code.py`](snippets/13-code.py) | Code | python | 4. Cleaning and Transforming with pandas |
| [`14-output.txt`](snippets/14-output.txt) | Output | text | 4. Cleaning and Transforming with pandas |
| [`15-output.txt`](snippets/15-output.txt) | Output | text | 4. Cleaning and Transforming with pandas |
| [`16-output.txt`](snippets/16-output.txt) | Output | text | 4. Cleaning and Transforming with pandas |
| [`17-output.txt`](snippets/17-output.txt) | Output | text | 4. Cleaning and Transforming with pandas |
| [`18-listing-16-7-the-pandas-and-notebook-rules-in-claude-md.md`](snippets/18-listing-16-7-the-pandas-and-notebook-rules-in-claude-md.md) | Listing 16-7: The pandas and notebook rules in CLAUDE.md | markdown | 4. Cleaning and Transforming with pandas |
| [`19-output.txt`](snippets/19-output.txt) | Output | text | 5. When to Move to Polars |
| [`20-listing-16-8-extras-report-polars-py-not-run.py`](snippets/20-listing-16-8-extras-report-polars-py-not-run.py) | Listing 16-8: extras/report_polars.py (not run) | python | 5. When to Move to Polars |
| [`21-prompt.txt`](snippets/21-prompt.txt) | Prompt | prompt | 6. Turning a Notebook into a Tested Python Module |
| [`22-listing-16-9-the-test-rows-in-tests-conftest-py.py`](snippets/22-listing-16-9-the-test-rows-in-tests-conftest-py.py) | Listing 16-9: The test rows in tests/conftest.py | python | 6. Turning a Notebook into a Tested Python Module |
| [`23-listing-16-10-summarize-in-src-salesreport-report-py.py`](snippets/23-listing-16-10-summarize-in-src-salesreport-report-py.py) | Listing 16-10: summarize() in src/salesreport/report.py | python | 6. Turning a Notebook into a Tested Python Module |
| [`24-listing-16-11-notebooks-01-explore-orders-ipynb-code-cells.py`](snippets/24-listing-16-11-notebooks-01-explore-orders-ipynb-code-cells.py) | Listing 16-11: notebooks/01-explore-orders.ipynb (code cells) | python | 6. Turning a Notebook into a Tested Python Module |
| [`25-listing-16-12-src-salesreport-charts-py.py`](snippets/25-listing-16-12-src-salesreport-charts-py.py) | Listing 16-12: src/salesreport/charts.py | python | 7. Charts with matplotlib and Plotly |
| [`26-listing-16-13-extras-chart-plotly-py-not-run.py`](snippets/26-listing-16-13-extras-chart-plotly-py-not-run.py) | Listing 16-13: extras/chart_plotly.py (not run) | python | 7. Charts with matplotlib and Plotly |
| [`27-listing-16-14-the-order-model-in-src-salesreport-validate-p.py`](snippets/27-listing-16-14-the-order-model-in-src-salesreport-validate-p.py) | Listing 16-14: The Order model in src/salesreport/validate.py | python | 8. Data Validation with Pandera or Pydantic |
| [`28-listing-16-15-split-valid-in-src-salesreport-validate-py.py`](snippets/28-listing-16-15-split-valid-in-src-salesreport-validate-py.py) | Listing 16-15: split_valid() in src/salesreport/validate.py | python | 8. Data Validation with Pandera or Pydantic |
| [`29-output.txt`](snippets/29-output.txt) | Output | text | 8. Data Validation with Pandera or Pydantic |
| [`30-listing-16-16-extras-schema-pandera-py-not-run.py`](snippets/30-listing-16-16-extras-schema-pandera-py-not-run.py) | Listing 16-16: extras/schema_pandera.py (not run) | python | 8. Data Validation with Pandera or Pydantic |
| [`31-listing-16-17-run-in-src-salesreport-pipeline-py.py`](snippets/31-listing-16-17-run-in-src-salesreport-pipeline-py.py) | Listing 16-17: run() in src/salesreport/pipeline.py | python | 9. End-to-End Example: A Sales Report Pipeline |
| [`32-terminal.sh`](snippets/32-terminal.sh) | Terminal | bash | 9. End-to-End Example: A Sales Report Pipeline |
| [`33-code.md`](snippets/33-code.md) | Code | markdown | 9. End-to-End Example: A Sales Report Pipeline |
| [`34-output.txt`](snippets/34-output.txt) | Output | text | 9. End-to-End Example: A Sales Report Pipeline |
| [`35-listing-16-18-the-golden-file-test-in-tests-test-pipeline-p.py`](snippets/35-listing-16-18-the-golden-file-test-in-tests-test-pipeline-p.py) | Listing 16-18: The golden-file test in tests/test_pipeline.py | python | 9. End-to-End Example: A Sales Report Pipeline |
| [`36-output.txt`](snippets/36-output.txt) | Output | text | 9. End-to-End Example: A Sales Report Pipeline |
