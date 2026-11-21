# EnergyAtlas progress — 21 November 2026

## Completed in this checkpoint

- Restored the original main and setup/project-foundation history from the Git bundle.
- Created feature/fullstack-integration from the newer foundation.
- Integrated the catalogue frontend/backend without changing the original mock workflow.
- Retained the setup diagnostic, original contract tests, PR template and attribution.
- Added project-file completeness and Node/npm checks to the setup diagnostic.
- Added a Python setup helper that does not require the Windows py launcher.
- Updated the product README, architecture, roadmap and learning guide.

See verification.md for the actual checks and limitations.

## Immediate learner checkpoint

Run the integrated catalogue. Save SMARD, open Saved sources, refresh, and confirm
the bookmark remains. Then trace the request using LEARN.md and write your own
explanation. No model installation is needed.

## Planned after catalogue verification

1. PostgreSQL and schema migrations, checked against the same API behaviour.
2. One real, licensed public energy dataset, with supported geography, units and periods.
3. 3–5 permitted public reports with document hashes and physical PDF page references.
4. Real-model retrieval and supported answers after model/budget choice.
5. A 12-question labelled evaluation: 9 answerable and 3 unsupported questions.
   Measure Recall@3 and reciprocal rank only on the answerable subset; review
   answer/citation support and insufficient-evidence behaviour separately.
6. MCP discovery and calls for search_reports and get_region_statistics.
7. Authentication as needed for user accounts, operational checks and deployment.

## Outside the first release

Forecasting, unrestricted SQL, automatic web crawling, model training, delivery
logistics, sharding and advanced GIS. Add complexity only for a demonstrated need.
