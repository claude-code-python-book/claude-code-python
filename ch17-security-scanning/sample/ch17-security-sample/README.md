# Chapter 17 sample: bookfinder

- `bookfinder/` is the sample project (a Git repository): the fixed search
  API, its tests (including the injection payloads), CLAUDE.md, the /triage
  skill, pre-commit, Dependabot, the security workflow and a Semgrep rule.
- `demos/` holds the scripts behind the chapter's outputs. They are
  deliberately vulnerable; run them only on your own machine.
  - `vulnerable/` and `exploit.py`: the first two versions of search_books()
    and the attacks against them (`python demos/exploit.py`).
  - `patterns/`: pickle and YAML, shell=True, Jinja2 and SSRF demonstrations.
  - `legacy.py`: run it with several Python versions.
  - `pydantic_v1_style.py`: a Pydantic 1 model on Pydantic 2.
  - `lockdemo.sh`, `hashdemo.sh`: lock drift and pip hash checking (need uv).
  - `renovate.json`: the Renovate configuration from Section 9.
