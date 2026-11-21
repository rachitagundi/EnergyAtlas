The starter had a model-double checkpoint but no Git history, agreed release
scope, architecture or portable setup check. This change defines EnergyAtlas's
first release and gives the learner a read-only Python command for checking their
Windows setup before model selection.

It adds the target architecture, a gated implementation plan, an optional-command-
tolerant setup diagnostic and its contract checks. GitHub Actions is configured
to install the constrained dependencies and run the checks on Ubuntu and Windows
with Python 3.12. Actions are pinned to inspected commits. Upstream attribution
is preserved and the learner's one-line `top_k` exercise is left for them to write.

Validation on managed Linux/Python 3.12.14:

- `python -m unittest discover -s tests -v`: 7 checks passed.
- `python checkpoint.py`: model-double pipeline smoke check passed.
- `python -m pip check`: no broken requirements found.
- `python scripts/check_setup.py`: produced the expected JSON report.
- `git diff --check`: passed before commit.

Windows runtime and hosted CI results remain pending. Real models, public-report
ingestion/citations, statistics, measured evaluation, MCP tools, the API and
deployment are planned. This is an AI-assisted repository foundation; no learner
implementation or real-model quality result is claimed.
