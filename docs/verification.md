# Verification — integrated checkpoint 0C

Checked on 21 November 2026 in managed Linux, Python 3.12.14 and Node 24.22.3.

## Passed

- Eight foundation/setup tests: four setup checks and four original workflow checks.
- Three catalogue API tests: combined filters; idempotent bookmarks and persistence
  across app recreation; source creation, duplicate URLs and invalid input.
- Original model-double checkpoint: two fixture nodes retrieved and passed to
  the mock response synthesizer. No real retrieval-quality claim follows.
- Dependency consistency checks for both separate Python environments.
- TypeScript checking and Vite production build.
- The setup helper completed its Python and frontend installation steps in Linux.
- Built app integration: FastAPI served frontend HTML/JS/CSS, health, API docs
  and the four seeded catalogue records.
- Actual Chrome interaction: the four sources loaded, SMARD was saved, the page
  was refreshed and Saved sources still contained SMARD.
- Actual Chrome interaction: searching Bundesnetzagentur returned SMARD; choosing
  Renewables returned the Umweltbundesamt source.
- Actual Chrome interaction: the add-source dialog rejected the existing SMARD
  URL with a duplicate-source message without adding another record.
- The desktop catalogue layout was visually inspected.

## Not established

- Windows execution of the installer, catalogue or new CI configuration.
- PostgreSQL/Compose execution: Docker is not installed in this environment.
- Mobile layout and a full accessibility audit.
- Hosted CI runs, public deployment or real-model RAG.
- Real dataset ingestion, PDF citations, retrieval evaluation and MCP client calls.

The browser demo uses its own local SQLite database. That database is excluded
from the package and Git. A fresh installation starts with four unsaved sources.

## Dependency observations

The pinned FastAPI/Starlette TestClient emits an httpx deprecation warning.
The assertions passed. npm reports its inherited proxy setting and an esbuild
install-script warning; installation and the actual frontend build passed.

## History and authorship

The original Git bundle's main and setup/project-foundation histories were
restored. Integration work is on feature/fullstack-integration.
Original checkpoint.py, workflow.py, fixtures and upstream notices are preserved.
Learner exercises have not been completed by the integration.

GitHub repository creation and remote publication are tracked separately from
local code and test results.
