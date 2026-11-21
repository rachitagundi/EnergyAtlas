# EnergyAtlas version 1

## Purpose

Help a researcher or analyst answer questions from a small, curated collection
of public German energy reports and retrieve exact statistics from one public
dataset. Make the supporting evidence inspectable.

This is a Python software and data project with an applied AI component. Energy
is the demonstration domain. The learner should be able to explain ingestion,
retrieval, citations, SQL, API design, tests and evaluation in an interview.

## Fixed first-release scope

- Germany; a curated collection of 3–5 public, text-based energy PDFs in German
  and/or English. Select actual documents only after checking access and reuse terms.
- Report search and short answers with publisher, title, source URL, document date
  when known, and the physical PDF page number for each supporting passage.
- An explicit insufficient-evidence outcome when the indexed material cannot
  support a response. Retrieved content is evidence to inspect, not proof of truth.
- One small public structured dataset loaded into SQLite. Return supported
  region/year/metric combinations with values, units, definitions and provenance.
  National coverage is enough initially; include federal states only if the
  chosen source actually provides them. Do not invent regional disaggregation.
- A labelled set of 12 initial questions: 9 answerable questions with expected
  supporting passages and 3 questions the corpus does not answer. Report measured
  retrieval Recall@3 and reciprocal rank on the answerable subset. Inspect citation
  support and insufficient-evidence behavior separately, stating sample size.
- Two read-only MCP tools: `search_reports` and `get_region_statistics`.
  Verify actual tool discovery and successful calls using a real MCP client.
- A small FastAPI application with report-Q&A and statistics endpoints and the
  same shared services used by MCP. Include an example request/response and a demo.
- Automated checks, a repeatable environment, deployment instructions, architecture,
  attribution and an honest contribution log.

## Examples of intended behavior

Report question: "What barriers to solar expansion do these reports identify?"
Return only supported points, with the relevant source pages. This is a proposed
demo question, not a statement about documents already in the corpus.

Data question: "Return the available value for this region, year and metric."
Read the numeric value and unit from the validated table. If that combination is
absent, return an explicit unavailable result, not a language-model estimate.

## Deferred

GIS/maps, forecasting, model training/fine-tuning, automatic web crawling,
scanned-PDF OCR, unrestricted database access, multi-agent systems, additional
orchestration frameworks and multiple user accounts are outside version 1.

## Current implementation

The inherited checkpoint loads two synthetic text fixtures, builds an in-memory
index and exercises a LlamaIndex workflow with model doubles. It does not perform
meaningful semantic ranking or generate real answers. The current development
branch adds the project plan, architecture, setup diagnostics and CI configuration.

Real models, public PDFs, provenance-aware citations, the dataset/database,
evaluation, MCP tools, API and deployment are still planned. Milestone 1 remains
open until the real-model run and the learner's change and explanation are reviewed.

## Delivery order and completion evidence

| Milestone | Work | Completion evidence |
| --- | --- | --- |
| 1 | Real-model minimal RAG, explanation and learner Git exercise | Hardware/model decision recorded; retrieved text and real answer inspected; learner branch reviewed |
| 2 | Public reports and metadata | 3–5 sources recorded with access/reuse terms, dates, hashes and preserved PDF page references |
| 3 | Citations, insufficient evidence and evaluation | Labels committed; reproducible measured retrieval results and documented answer/citation review |
| 4 | Structured dataset and MCP tools | Validated table with provenance; actual MCP client lists and calls both tools |
| 5 | API, tests and deployment | API examples pass; clean environment starts; deployed smoke check and limitations recorded |
| 6 | Portfolio presentation | Architecture, reproducible demo, README and contribution-supported CV bullets |

## Repository policy

Start in a private GitHub repository named `EnergyAtlas` under the user's verified
account when GitHub is connected. Record the scaffold as AI-assisted. Keep the
learner exercise separate from mentor-written changes. Use a development branch
and a draft pull request for review; make the portfolio public after the source
and contribution review. No paid services or model downloads are enabled by this
repository setup.
