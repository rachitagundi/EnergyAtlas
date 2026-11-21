# Understand one complete request

The project now has one integrated source tree. Start with the catalogue, then
study the separate mock RAG exercise. Neither requires a paid model.

## First session: save a source

1. Click the bookmark next to SMARD.
2. React calls 'bookmark' in frontend/src/App.tsx.
3. 'saveSource' in frontend/src/api.ts sends a PATCH request with {"saved": true}.
4. The route in backend/app/main.py validates the JSON and opens a database session.
5. SQLAlchemy updates the record and commits it.
6. React reloads the list and counts. A refresh loads the saved state from SQLite.

React state is the current screen's data. Database state persists beyond that
screen. An API request is the message between the browser and backend.
An explicit saved=true request is idempotent: repeating it keeps the source saved.

## Read in this order

| File | Question |
| --- | --- |
| frontend/src/App.tsx | Which click starts the request, and how are errors shown? |
| frontend/src/api.ts | Which URL, method and JSON does the browser send? |
| backend/app/schemas.py | Which input values are accepted? |
| backend/app/main.py | How does the route update the record? |
| backend/app/db.py | Which fields are persisted? |
| backend/tests/test_api.py | How do we check persistence and duplicate requests? |

## Your explanation

Write fullstack_learning_notes.md in your own words:
- What changes in React, and what changes in SQLite?
- What happens if the API is stopped?
- Why does sending saved=true twice not remove the bookmark?
- What does a successful test prove, and what does it leave unchecked?

Do not complete the independent source-type-filter or top_k exercises by asking
the assistant to write the answers. Bring your prediction and diff for review.
The current source-type filter exercise is described in START_HERE_WINDOWS.md.

## Where LlamaIndex is used

The running catalogue does not call LlamaIndex. The original checkpoint.py and
workflow.py exercise document loading, indexing, retrieval and response synthesis
with mock embeddings and a mock LLM, in the separate .venv-rag environment.

A chunk is a smaller piece of document text. An embedding is a numerical
representation used to compare text. A retriever finds candidate passages.
The language model writes a response using supplied context.

The current mock embeddings are identical, and the mock LLM echoes its prompt.
They test pipeline wiring, not search quality or supported answers.

Later, a Python report service will use LlamaIndex with real models. FastAPI and
MCP will call shared search/statistics functions. Exact numerical results will
come from validated SQL queries, with units, reporting period and provenance.

## Resources, in order

1. FastAPI First Steps: https://fastapi.tiangolo.com/tutorial/first-steps/
2. React Quick Start: https://react.dev/learn
3. LlamaIndex RAG introduction: https://developers.llamaindex.ai/python/framework/understanding/rag/
4. Official video series: https://developers.llamaindex.ai/python/framework/getting_started/discover_llamaindex/

Read the concepts first. Model choices, downloads and provider installation
commands need a separate hardware, licence and budget decision.
