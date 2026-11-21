# Start EnergyAtlas on Windows

Use the integrated checkpoint 0C package. Keep old project folders separate.

## 1. Open the correct folder

Extract the ZIP, then open its EnergyAtlas folder in VS Code. You should see:
backend, frontend, scripts, package.json, README.md and this guide.

In PowerShell, run:

```powershell
Get-Location
python --version
node --version
npm.cmd --version
python scripts/check_setup.py
```

The tested target is Python 3.12 and Node 24. No py launcher is required.
The diagnostic should report project.fullstack.complete as true.

## 2. Install once

```powershell
python scripts/setup_local.py
```

The script finds the project from its own location, creates .venv-fullstack,
installs backend requirements with constraints, and installs frontend dependencies.
No models, AI accounts, paid APIs or Docker are required.

## 3. Start both servers

From the folder containing package.json:

```powershell
npm.cmd run dev
```

Open http://127.0.0.1:5173 . Keep the terminal running.
API docs: http://127.0.0.1:8010/api/docs .
Health: http://127.0.0.1:8010/api/health .
Expected health: {"status":"ok","checkpoint":"0C"}.

## 4. Verify one complete request

Save SMARD, open Saved sources, refresh and confirm it remains saved.
Search for Bundesnetzagentur. Clear search and filter Renewables.
Add a test URL; adding it twice should show a duplicate-source message.

Follow docs/LEARN.md to understand the request. Write your own explanation before
starting another feature.

## Common errors

| Error | What to check |
| --- | --- |
| py is not recognised | Use the python commands above; the launcher is optional |
| Cannot find package.json | Get-Location must show the integrated EnergyAtlas root |
| Missing constraints or package-lock | Re-extract the complete integrated package into a new folder |
| npm.ps1 cannot run | Use npm.cmd; no execution-policy change is needed |
| API unavailable | Keep the terminal running and read the Python startup error |
| Address already in use | Stop the previous EnergyAtlas run with Ctrl+C before starting this one |

## Check the code

```powershell
$env:PYTHONPATH = "backend"
.\.venv-fullstack\Scripts\python.exe -m pytest backend\tests -v
Remove-Item Env:PYTHONPATH
npm.cmd --prefix frontend run build
```

Python checks and builds were run in managed Linux. Windows verification remains
separate; paste the actual command/error output when troubleshooting.

## Next independent change

After explaining the bookmark flow, add a source-type filter (Data portal /
Overview / Statistics). Predict the behaviour, implement the API parameter and
React dropdown, and add a test combining source type with topic. Use a separate
learning branch. This feature has not been written for you.

The older top_k exercise is retained separately and is also still your work.

## PostgreSQL later

Dockerfile and compose.yaml are included, but Docker execution is not verified.
Once Docker Desktop is available, stop the local API before using:

```powershell
docker compose up --build
```

The Compose app is intended to use PostgreSQL and serve the built frontend at
http://127.0.0.1:8010 . Its credentials are local development examples.
