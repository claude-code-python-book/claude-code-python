# Chapter 9 — pytest and Test Coverage: Generate Tests and Fill the Gaps

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`README.md`, `examples`, `hand_mutants.py`, `invoicer`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-code.py`](snippets/01-code.py) | Code | python | 1. What Makes a Good Unit Test in Python |
| [`02-listing-9-1-late-fee-in-src-invoicer-billing-py.py`](snippets/02-listing-9-1-late-fee-in-src-invoicer-billing-py.py) | Listing 9-1: late_fee in src/invoicer/billing.py | python | 2. Generating Your First pytest Test |
| [`03-prompt.txt`](snippets/03-prompt.txt) | Prompt | prompt | 2. Generating Your First pytest Test |
| [`04-listing-9-2-tests-test-late-fee-py-first-version.py`](snippets/04-listing-9-2-tests-test-late-fee-py-first-version.py) | Listing 9-2: tests/test_late_fee.py (first version) | python | 2. Generating Your First pytest Test |
| [`05-terminal.sh`](snippets/05-terminal.sh) | Terminal | bash | 2. Generating Your First pytest Test |
| [`06-output.txt`](snippets/06-output.txt) | Output | text | 2. Generating Your First pytest Test |
| [`07-prompt.txt`](snippets/07-prompt.txt) | Prompt | prompt | 2. Generating Your First pytest Test |
| [`08-output.txt`](snippets/08-output.txt) | Output | text | 2. Generating Your First pytest Test |
| [`09-listing-9-3-tests-conftest-py-the-row-factory.py`](snippets/09-listing-9-3-tests-conftest-py-the-row-factory.py) | Listing 9-3: tests/conftest.py (the row factory) | python | 3. Fixtures, conftest.py, and Fixture Scope |
| [`10-listing-9-4-a-test-in-tests-test-billing-py-that-uses-the.py`](snippets/10-listing-9-4-a-test-in-tests-test-billing-py-that-uses-the.py) | Listing 9-4: A test in tests/test_billing.py that uses the factory | python | 3. Fixtures, conftest.py, and Fixture Scope |
| [`11-listing-9-5-tests-conftest-py-a-local-rates-service.py`](snippets/11-listing-9-5-tests-conftest-py-a-local-rates-service.py) | Listing 9-5: tests/conftest.py (a local rates service) | python | 3. Fixtures, conftest.py, and Fixture Scope |
| [`12-terminal.sh`](snippets/12-terminal.sh) | Terminal | bash | 3. Fixtures, conftest.py, and Fixture Scope |
| [`13-output.txt`](snippets/13-output.txt) | Output | text | 3. Fixtures, conftest.py, and Fixture Scope |
| [`14-listing-9-6-src-invoicer-fx-py.py`](snippets/14-listing-9-6-src-invoicer-fx-py.py) | Listing 9-6: src/invoicer/fx.py | python | 4. Mocking the Right Way: unittest.mock, pytest-mock, monkeypatch |
| [`15-listing-9-7-a-stub-in-tests-test-fx-py.py`](snippets/15-listing-9-7-a-stub-in-tests-test-fx-py.py) | Listing 9-7: A stub in tests/test_fx.py | python | 4. Mocking the Right Way: unittest.mock, pytest-mock, monkeypatch |
| [`16-listing-9-8-a-mock-that-checks-the-call-in-tests-test-fx.py`](snippets/16-listing-9-8-a-mock-that-checks-the-call-in-tests-test-fx.py) | Listing 9-8: A mock that checks the call, in tests/test_fx.py | python | 4. Mocking the Right Way: unittest.mock, pytest-mock, monkeypatch |
| [`17-listing-9-9-tests-for-convert-in-tests-test-fx-py.py`](snippets/17-listing-9-9-tests-for-convert-in-tests-test-fx-py.py) | Listing 9-9: Tests for convert in tests/test_fx.py | python | 4. Mocking the Right Way: unittest.mock, pytest-mock, monkeypatch |
| [`18-code.py`](snippets/18-code.py) | Code | python | 4. Mocking the Right Way: unittest.mock, pytest-mock, monkeypatch |
| [`19-output.txt`](snippets/19-output.txt) | Output | text | 4. Mocking the Right Way: unittest.mock, pytest-mock, monkeypatch |
| [`20-code.py`](snippets/20-code.py) | Code | python | 4. Mocking the Right Way: unittest.mock, pytest-mock, monkeypatch |
| [`21-listing-9-10-a-test-that-patches-the-wrong-name.py`](snippets/21-listing-9-10-a-test-that-patches-the-wrong-name.py) | Listing 9-10: A test that patches the wrong name | python | 4. Mocking the Right Way: unittest.mock, pytest-mock, monkeypatch |
| [`22-output.txt`](snippets/22-output.txt) | Output | text | 4. Mocking the Right Way: unittest.mock, pytest-mock, monkeypatch |
| [`23-prompt.txt`](snippets/23-prompt.txt) | Prompt | prompt | 5. Parametrized Tests: Coverage Without Repetition |
| [`24-listing-9-11-tests-test-late-fee-py-parametrized.py`](snippets/24-listing-9-11-tests-test-late-fee-py-parametrized.py) | Listing 9-11: tests/test_late_fee.py (parametrized) | python | 5. Parametrized Tests: Coverage Without Repetition |
| [`25-terminal.sh`](snippets/25-terminal.sh) | Terminal | bash | 5. Parametrized Tests: Coverage Without Repetition |
| [`26-output.txt`](snippets/26-output.txt) | Output | text | 5. Parametrized Tests: Coverage Without Repetition |
| [`27-listing-9-12-examples-billing-api-billing-api-app-py.py`](snippets/27-listing-9-12-examples-billing-api-billing-api-app-py.py) | Listing 9-12: examples/billing_api/billing_api/app.py | python | 6. Testing FastAPI with TestClient and httpx.AsyncClient |
| [`28-listing-9-13-examples-billing-api-tests-test-app-py.py`](snippets/28-listing-9-13-examples-billing-api-tests-test-app-py.py) | Listing 9-13: examples/billing_api/tests/test_app.py | python | 6. Testing FastAPI with TestClient and httpx.AsyncClient |
| [`29-listing-9-14-examples-billing-portal-portal-models-py.py`](snippets/29-listing-9-14-examples-billing-portal-portal-models-py.py) | Listing 9-14: examples/billing_portal/portal/models.py | python | 7. Testing Django Views and Models with pytest-django |
| [`30-listing-9-15-the-pytest-settings-in-examples-billing-porta.toml`](snippets/30-listing-9-15-the-pytest-settings-in-examples-billing-porta.toml) | Listing 9-15: The pytest settings in examples/billing_portal/pyproject.toml | toml | 7. Testing Django Views and Models with pytest-django |
| [`31-listing-9-16-examples-billing-portal-tests-test-invoices-p.py`](snippets/31-listing-9-16-examples-billing-portal-tests-test-invoices-p.py) | Listing 9-16: examples/billing_portal/tests/test_invoices.py | python | 7. Testing Django Views and Models with pytest-django |
| [`32-listing-9-17-fetch-many-in-src-invoicer-fx-py.py`](snippets/32-listing-9-17-fetch-many-in-src-invoicer-fx-py.py) | Listing 9-17: fetch_many in src/invoicer/fx.py | python | 8. Async Tests with pytest-asyncio |
| [`33-listing-9-18-tests-test-fx-async-py.py`](snippets/33-listing-9-18-tests-test-fx-async-py.py) | Listing 9-18: tests/test_fx_async.py | python | 8. Async Tests with pytest-asyncio |
| [`34-code.py`](snippets/34-code.py) | Code | python | 8. Async Tests with pytest-asyncio |
| [`35-listing-9-19-tests-test-properties-py.py`](snippets/35-listing-9-19-tests-test-properties-py.py) | Listing 9-19: tests/test_properties.py | python | 9. Property-Based Testing with Hypothesis |
| [`36-prompt.txt`](snippets/36-prompt.txt) | Prompt | prompt | 10. Edge Cases, Negative Tests, and Boundaries |
| [`37-listing-9-20-the-boundary-cases-added-to-tests-test-late-f.py`](snippets/37-listing-9-20-the-boundary-cases-added-to-tests-test-late-f.py) | Listing 9-20: The boundary cases added to tests/test_late_fee.py | python | 10. Edge Cases, Negative Tests, and Boundaries |
| [`38-listing-9-21-the-overdue-boundary-in-tests-test-billing-py.py`](snippets/38-listing-9-21-the-overdue-boundary-in-tests-test-billing-py.py) | Listing 9-21: The overdue boundary in tests/test_billing.py | python | 10. Edge Cases, Negative Tests, and Boundaries |
| [`39-listing-9-22-invalid-and-boundary-input-in-tests-test-bill.py`](snippets/39-listing-9-22-invalid-and-boundary-input-in-tests-test-bill.py) | Listing 9-22: Invalid and boundary input in tests/test_billing_models.py | python | 10. Edge Cases, Negative Tests, and Boundaries |
| [`40-terminal.sh`](snippets/40-terminal.sh) | Terminal | bash | 10. Edge Cases, Negative Tests, and Boundaries |
| [`41-output.txt`](snippets/41-output.txt) | Output | text | 10. Edge Cases, Negative Tests, and Boundaries |
| [`42-terminal.sh`](snippets/42-terminal.sh) | Terminal | bash | 11. Measuring Coverage with coverage.py and pytest-cov |
| [`43-listing-9-23-coverage-settings-in-pyproject-toml.toml`](snippets/43-listing-9-23-coverage-settings-in-pyproject-toml.toml) | Listing 9-23: Coverage settings in pyproject.toml | toml | 11. Measuring Coverage with coverage.py and pytest-cov |
| [`44-code.py`](snippets/44-code.py) | Code | python | 11. Measuring Coverage with coverage.py and pytest-cov |
| [`45-prompt.txt`](snippets/45-prompt.txt) | Prompt | prompt | 12. Prompting Claude Code for Real Gap Analysis: A Worked Example |
| [`46-listing-9-24-tests-test-legacy-export-py.py`](snippets/46-listing-9-24-tests-test-legacy-export-py.py) | Listing 9-24: tests/test_legacy_export.py | python | 12. Prompting Claude Code for Real Gap Analysis: A Worked Example |
| [`47-listing-9-25-the-region-gap-in-tests-test-billing-py.py`](snippets/47-listing-9-25-the-region-gap-in-tests-test-billing-py.py) | Listing 9-25: The region gap, in tests/test_billing.py | python | 12. Prompting Claude Code for Real Gap Analysis: A Worked Example |
| [`48-listing-9-26-the-same-day-payment-in-tests-test-billing-mo.py`](snippets/48-listing-9-26-the-same-day-payment-in-tests-test-billing-mo.py) | Listing 9-26: The same-day payment, in tests/test_billing_models.py | python | 12. Prompting Claude Code for Real Gap Analysis: A Worked Example |
| [`49-terminal.sh`](snippets/49-terminal.sh) | Terminal | bash | 12. Prompting Claude Code for Real Gap Analysis: A Worked Example |
| [`50-output.txt`](snippets/50-output.txt) | Output | text | 12. Prompting Claude Code for Real Gap Analysis: A Worked Example |
| [`51-code.toml`](snippets/51-code.toml) | Code | toml | 13. Mutation Testing with mutmut: Do the Tests Really Assert? |
| [`52-listing-9-27-github-workflows-tests-yml.yml`](snippets/52-listing-9-27-github-workflows-tests-yml.yml) | Listing 9-27: .github/workflows/tests.yml | yaml | 14. Enforcing Coverage in CI and Keeping the Suite Healthy |
| [`53-listing-9-28-the-dev-group-and-pytest-settings-in-pyprojec.toml`](snippets/53-listing-9-28-the-dev-group-and-pytest-settings-in-pyprojec.toml) | Listing 9-28: The dev group and pytest settings in pyproject.toml | toml | 14. Enforcing Coverage in CI and Keeping the Suite Healthy |
| [`54-terminal.sh`](snippets/54-terminal.sh) | Terminal | bash | 14. Enforcing Coverage in CI and Keeping the Suite Healthy |
| [`55-output.txt`](snippets/55-output.txt) | Output | text | 14. Enforcing Coverage in CI and Keeping the Suite Healthy |
| [`56-listing-9-29-claude-skills-test-gaps-skill-md.md`](snippets/56-listing-9-29-claude-skills-test-gaps-skill-md.md) | Listing 9-29: .claude/skills/test-gaps/SKILL.md | markdown | 14. Enforcing Coverage in CI and Keeping the Suite Healthy |
