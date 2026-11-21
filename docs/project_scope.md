# First-release scope

EnergyAtlas is a full stack energy-research workspace. The catalogue now provides
a complete browser/API/database flow. Report answers and structured energy
statistics remain planned.

## Current milestone: integrated checkpoint 0C

One repository combines the newer foundation with React/TypeScript, FastAPI,
SQLAlchemy/SQLite, catalogue filtering and persistent favourites. The original
mock RAG exercise and its history remain intact.

## Remaining first-release work

- Verify the application on Windows and through actual browser interaction.
- Verify PostgreSQL and schema migrations.
- Import one public dataset, retaining metric definitions, units, source, period
  and supported geography. National coverage is enough initially.
- Select 3–5 public German/English text PDFs after checking access/reuse terms.
  Retain hashes, dates when known and physical PDF page references.
- Select real embedding/generation models after hardware, licence and budget checks.
- Implement supported answers and an explicit insufficient-evidence result.
- Label 12 questions: 9 answerable with expected passages, 3 unsupported.
  Measure Recall@3 and reciprocal rank on the answerable subset; inspect answer
  and citation support and unsupported-question behaviour separately.
- Implement and verify MCP client discovery and calls for search_reports and
  get_region_statistics, reusing shared services with FastAPI.
- Add operational/deployment verification and accurate portfolio documentation.

No numerical performance or answer-quality result is claimed before measurement.
Advanced GIS, forecasting, training, automatic crawling and distributed storage
are deferred. The original scope is archived for change history.
