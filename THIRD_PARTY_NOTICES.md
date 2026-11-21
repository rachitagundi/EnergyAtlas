# Sources and attribution

This is an AI-assisted learning scaffold for Rachita Gundi's EnergyAtlas project.
It is not a claim that the learner has independently implemented this code.

## Primary reference: ai-engineering-hub

- Author: patchy631; copyright (c) 2024 patchy631.
- Repository: https://github.com/patchy631/ai-engineering-hub
- Inspected commit: `042aeb5067384981eeba6a07fa882f436bb1660d`.
- Reference: `simple-rag-workflow/workflow.py`, its README, and both notebooks.
- Licence: MIT. The exact upstream notice is retained in `LICENSE` and
  `third_party/ai-engineering-hub/LICENSE`.
- The original script and README are retained unchanged under `third_party/`.
  They are reference material and are not the checkpoint entry point.
- EnergyAtlas `workflow.py` adapts its event-based ingest/retrieve/synthesize
  structure. Changes include current context-store methods, explicit model
  injection, plain-text-only fixtures, validation before workflow execution,
  and non-streaming output for a smaller first checkpoint.
- No upstream report PDFs, evaluation data, or notebook output are redistributed.

## Other references, not copied or installed

- PrefectHQ/FastMCP, inspected commit
  `ffc65c7a8063bf66522fafd3d8db280d49a34e4e`:
  https://github.com/PrefectHQ/fastmcp . Apache-2.0. It is a candidate for
  milestone 4, not a dependency of this checkpoint.
- DataTalksClub/llm-zoomcamp, inspected commit
  `85c4833f649e6aae431c8e2dbdce58be0c53df2a`:
  https://github.com/DataTalksClub/llm-zoomcamp . No root LICENSE/COPYING file was
  present in the inspected root listing. Do not assume permission to relicense
  its material; use it as linked learning material. Module dependencies are
  separate; no course code is included here.

Installed packages retain their own licences. LlamaIndex core and the inspected
Ollama/Hugging Face LlamaIndex integrations declare MIT in package metadata.
Model weights have separate licences; no production model has been selected.
