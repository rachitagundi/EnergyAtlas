# Inspection — 16 November 2026

The current workspace was empty. No files from another conversation were assumed.
This managed Linux environment has Python 3.12.14 and Git 2.52.0. These are not
measurements of the learner's Windows machine.

## Reference architecture

| Stage | Upstream implementation | Purpose |
| --- | --- | --- |
| Load | `SimpleDirectoryReader` | Convert files into documents |
| Index | `VectorStoreIndex.from_documents` | Split documents and embed chunks into an in-memory vector index |
| Retrieve | `as_retriever(similarity_top_k=2)` | Embed the question and select two nearby chunks |
| Generate | `CompactAndRefine` with Ollama | Put retrieved text into prompts and synthesize a streamed response |
| Orchestrate | LlamaIndex `Workflow`, events and context | Route ingestion separately from retrieval and synthesis |

Embeddings are numeric representations used to search. The LLM writes an answer
from the retrieved context. They are separate components. A vector index is not
a trained language model, and RAG does not retrain the LLM.

## Findings

- No `requirements.txt`, `pyproject.toml`, or dependency lockfile exists in the
  reference subdirectory at the inspected commit; none appears in the repository
  root listing either. Imports are not an installable dependency manifest.
- Core imports: LlamaIndex core/workflows; separate Ollama and Hugging Face
  integrations; `nest_asyncio`. The evaluation notebook also uses Opik and pandas.
- README says Python 3.10+, but the inspected current core release 0.14.26 requires
  Python >=3.11,<4.0. We test Python 3.12 here.
- Core 0.14.26 and its resolved workflows package 2.26.1 expose `ctx.store.set/get`.
  Direct `Context.set`/`Context.get`, used upstream, are absent. This was checked
  in the installed environment.
- README says 'Llama 2' while its command/script use `llama3.2`. Its installation
  shell commands are for Linux/macOS, not Windows.
- `BAAI/bge-small-en-v1.5` is an English-labelled embedding model. We will select
  a multilingual alternative before ingesting German reports, after hardware
  inspection; do not present this English baseline as German-validated.
- The script uses process-global Settings, an in-memory index, and a relative
  `data` path. The adaptation injects models and resolves demo data from its file.
- No source-aware citation policy, insufficient-evidence policy, retrieval
  benchmark, MCP tool server/client verification, API, or deployment is implemented
  by this checkpoint. Returning top-k chunks does not establish sufficient evidence.
- In the evaluation notebook, a synchronous task returns an async application's
  coroutine without awaiting it. It also assumes prior notebook state. We are
  not reusing its evaluation results or presenting them as EnergyAtlas scores.

## Dependency decision

Install only `llama-index-core==0.14.26` for checkpoint 0A, constrained to the
resolved versions in `constraints-py312.txt`. Model test doubles come with core.
This avoids installing Torch, downloading weights, or selecting a paid API.
The first installation still downloads Python packages; runtime uses local fixtures.

Inspected optional integration releases: `llama-index-llms-ollama==0.12.0`
requires core >=0.14.5,<0.15; `llama-index-embeddings-huggingface==0.9.0`
requires core >=0.13.0,<0.15. These ranges overlap core 0.14.26. This is a metadata
compatibility check, not a completed installation or real-model runtime check.
Model/provider dependencies must be resolved and locked once selected.

FastMCP's inspected current root requires Python >=3.11 and declares Apache-2.0.
It now delegates dependencies to its slim package; that manifest was inspected too.
We defer installing it until the MCP milestone and recheck its then-current version.
LLM Zoomcamp is a learning companion, not an additional orchestration stack.
There is no current reason to introduce PydanticAI.

## Next acceptance gates

0A: install, run this smoke check, understand the data flow, and complete one Git
exercise. This checks wiring, not RAG quality.

1B: measure Windows RAM/CPU/GPU/free disk, choose local or hosted generation and
multilingual embeddings with the learner, verify licences and current costs,
run the same workflow with real models, and inspect retrieved chunks plus answer.
Milestone 1 is complete only after that real-model run and the learner's explanation.

Later: public-report provenance and PDF pages; citations/abstention and a labelled
retrieval benchmark; MCP discovery/calls through an actual client; interface/tests/
deployment; architecture/demo/accurate portfolio descriptions. GIS stays optional.
