# Chapter 8 — Writing Python Code with Claude Code: A Refactoring Tutorial

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`invoicer`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-layout.txt`](snippets/01-layout.txt) | Layout | tree | 2. Setting the Stage: Project Layout and First Run |
| [`02-terminal.sh`](snippets/02-terminal.sh) | Terminal | bash | 2. Setting the Stage: Project Layout and First Run |
| [`03-prompt.txt`](snippets/03-prompt.txt) | Prompt | prompt | 2. Setting the Stage: Project Layout and First Run |
| [`04-prompt.txt`](snippets/04-prompt.txt) | Prompt | prompt | 3. Writing New Python Code: A First Prompt That Works |
| [`05-listing-8-1-src-invoicer-csv-rows-py-first-version.py`](snippets/05-listing-8-1-src-invoicer-csv-rows-py-first-version.py) | Listing 8-1: src/invoicer/csv_rows.py (first version) | python | 3. Writing New Python Code: A First Prompt That Works |
| [`06-terminal.sh`](snippets/06-terminal.sh) | Terminal | bash | 3. Writing New Python Code: A First Prompt That Works |
| [`07-output.txt`](snippets/07-output.txt) | Output | text | 3. Writing New Python Code: A First Prompt That Works |
| [`08-prompt.txt`](snippets/08-prompt.txt) | Prompt | prompt | 5. Iterating Without Starting Over |
| [`09-output.txt`](snippets/09-output.txt) | Output | text | 5. Iterating Without Starting Over |
| [`10-listing-8-2-the-first-lines-of-run-billing-in-src-invoice.py`](snippets/10-listing-8-2-the-first-lines-of-run-billing-in-src-invoice.py) | Listing 8-2: The first lines of run_billing in src/invoicer/billing_run.py (legacy) | python | 6. Refactoring Where Claude Code Pays Off |
| [`11-prompt.txt`](snippets/11-prompt.txt) | Prompt | prompt | 6. Refactoring Where Claude Code Pays Off |
| [`12-listing-8-3-tests-test-billing-characterization-py.py`](snippets/12-listing-8-3-tests-test-billing-characterization-py.py) | Listing 8-3: tests/test_billing_characterization.py | python | 6. Refactoring Where Claude Code Pays Off |
| [`13-prompt.txt`](snippets/13-prompt.txt) | Prompt | prompt | 6. Refactoring Where Claude Code Pays Off |
| [`14-listing-8-4-the-orchestration-in-src-invoicer-billing-run.py`](snippets/14-listing-8-4-the-orchestration-in-src-invoicer-billing-run.py) | Listing 8-4: The orchestration in src/invoicer/billing_run.py after Refactor 1 | python | 6. Refactoring Where Claude Code Pays Off |
| [`15-prompt.txt`](snippets/15-prompt.txt) | Prompt | prompt | 6. Refactoring Where Claude Code Pays Off |
| [`16-listing-8-5-the-validation-model-in-src-invoicer-billing.py`](snippets/16-listing-8-5-the-validation-model-in-src-invoicer-billing.py) | Listing 8-5: The validation model in src/invoicer/billing_models.py | python | 6. Refactoring Where Claude Code Pays Off |
| [`17-output.txt`](snippets/17-output.txt) | Output | text | 6. Refactoring Where Claude Code Pays Off |
| [`18-output.txt`](snippets/18-output.txt) | Output | text | 6. Refactoring Where Claude Code Pays Off |
| [`19-prompt.txt`](snippets/19-prompt.txt) | Prompt | prompt | 6. Refactoring Where Claude Code Pays Off |
| [`20-output.txt`](snippets/20-output.txt) | Output | text | 6. Refactoring Where Claude Code Pays Off |
| [`21-code.py`](snippets/21-code.py) | Code | python | 6. Refactoring Where Claude Code Pays Off |
| [`22-prompt.txt`](snippets/22-prompt.txt) | Prompt | prompt | 6. Refactoring Where Claude Code Pays Off |
| [`23-output.txt`](snippets/23-output.txt) | Output | text | 6. Refactoring Where Claude Code Pays Off |
| [`24-prompt.txt`](snippets/24-prompt.txt) | Prompt | prompt | 6. Refactoring Where Claude Code Pays Off |
| [`25-terminal.sh`](snippets/25-terminal.sh) | Terminal | bash | 6. Refactoring Where Claude Code Pays Off |
| [`26-output.txt`](snippets/26-output.txt) | Output | text | 6. Refactoring Where Claude Code Pays Off |
| [`27-listing-8-7-src-invoicer-billing-run-py-after-the-rename.py`](snippets/27-listing-8-7-src-invoicer-billing-run-py-after-the-rename.py) | Listing 8-7: src/invoicer/billing_run.py after the rename | python | 6. Refactoring Where Claude Code Pays Off |
| [`28-prompt.txt`](snippets/28-prompt.txt) | Prompt | prompt | 7. Pythonic Idioms Claude Should Follow (Comprehensions, Context Managers, pathlib) |
| [`29-output.txt`](snippets/29-output.txt) | Output | text | 7. Pythonic Idioms Claude Should Follow (Comprehensions, Context Managers, pathlib) |
| [`30-output.txt`](snippets/30-output.txt) | Output | text | 7. Pythonic Idioms Claude Should Follow (Comprehensions, Context Managers, pathlib) |
| [`31-terminal.sh`](snippets/31-terminal.sh) | Terminal | bash | 9. Running and Verifying: Closing the Loop |
| [`32-output.txt`](snippets/32-output.txt) | Output | text | 9. Running and Verifying: Closing the Loop |
| [`33-prompt.txt`](snippets/33-prompt.txt) | Prompt | prompt | 10. A Realistic End-to-End Example |
| [`34-output.txt`](snippets/34-output.txt) | Output | text | 10. A Realistic End-to-End Example |
| [`35-listing-8-8-src-invoicer-cli-py.py`](snippets/35-listing-8-8-src-invoicer-cli-py.py) | Listing 8-8: src/invoicer/cli.py | python | 10. A Realistic End-to-End Example |
| [`36-terminal.sh`](snippets/36-terminal.sh) | Terminal | bash | 10. A Realistic End-to-End Example |
| [`37-output.txt`](snippets/37-output.txt) | Output | text | 10. A Realistic End-to-End Example |
