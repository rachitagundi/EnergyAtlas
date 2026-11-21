# Verification — full stack checkpoint 0B

Checked on 16 November 2026 in managed Linux with Python 3.12.14 and Node 24.22.1.
This record distinguishes automated/server checks from browser interaction.

## Passed

- Three backend behavioural tests:
  - combined metadata search, topic and saved-state filtering, including a literal
    percent search rather than accidentally matching every record;
  - repeated explicit bookmark state and persistence across app recreation;
  - source creation, duplicate URL rejection, malformed URL/blank-field/invalid
    topic rejection, strict boolean validation and missing-source errors.
- Python dependency consistency check (pip check).
- TypeScript type checking and Vite production build.
- Built app integration check: FastAPI served the built HTML, JS and CSS assets,
  API documentation, health endpoint and four seeded database-backed sources.
- Combined development runner: API health and Vite-proxied source API returned
  successfully when both processes ran in the same execution session.

## Not established

- Browser click-through and visual QA: the first preview could not reach its API;
  a subsequent browser action was denied by preview access policy. No workaround
  was attempted. The server integration checks above are not a substitute for
  checking visual layout, mobile sizing, focus behaviour or React interactions.
- PostgreSQL/Compose route: Docker is not available in this environment.
- Windows execution: PowerShell instructions are supplied, not claimed as tested.
- GitHub CI: a workflow is included, but has not run on GitHub.
- RAG model quality, PDF ingestion, citations, MCP and public deployment.

## Dependency note

The tested FastAPI/Starlette combination emits a deprecation warning about its
httpx-based TestClient. All assertions passed. The Python constraint file records
the exact resolved versions so this known state is reproducible.

## Learner verification

Run the manual flow in START_HERE_WINDOWS.md and send the output or any error.
In particular, confirm that saving survives a browser refresh, topic/search
filters work together, duplicate additions show a useful message, and a stopped
API produces an error state. Then write the request/data-flow explanation before
adding another feature.
