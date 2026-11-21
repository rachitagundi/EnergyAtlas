# EnergyAtlas

An energy-report assistant being built in small, explainable checkpoints.
The first release will answer questions across 3–5 public German energy reports
with page citations, and retrieve figures from one public dataset. It will expose
the same services through MCP tools and a small FastAPI application. These
application features are planned; see the [finalized scope](docs/project_scope.md).

The target [architecture](docs/architecture.md) explains the report and statistics
paths. The initial stack is Python, LlamaIndex, a local vector index, SQLite,
then FastMCP and FastAPI when their milestones are reached. Real models remain
pending hardware, language, licence and budget checks.

**Current status: checkpoint 0A — tested pipeline wiring with model doubles.**
This is not a completed RAG assistant. `MockEmbedding` returns identical vectors,
so retrieval rankings have no meaning; `MockLLM` echoes its prompt rather than
writing an answer. No evaluation scores are reported. The two text files are
synthetic learning fixtures, not German energy evidence.

Development branch: `setup/project-foundation`. It adds this design, a read-only
setup diagnostic and CI configuration. GitHub creation/push and the first remote
CI run are pending connection; no public repository is claimed.

See [inspection](docs/inspection.md), [attribution](THIRD_PARTY_NOTICES.md),
[contributions](CONTRIBUTIONS.md), and [verification](docs/verification.md).

## 1. Check your Windows setup

Open **PowerShell** in VS Code and run the following. These are read-only checks.
The mentor cannot infer your Windows hardware from the managed coding environment.

For a single-command summary, the diagnostic needs only Python's standard library:

```powershell
python scripts/check_setup.py
```

It prints Python/Git versions, RAM, CPU, Windows GPU names and free disk space,
and detects optional commands. It makes no network calls and installs nothing.
The individual commands below are an alternative if the script cannot run.

```powershell
python --version
py -0p
git --version
Get-CimInstance Win32_ComputerSystem | Select-Object @{Name='RAM_GB';Expression={[math]::Round($_.TotalPhysicalMemory / 1GB, 1)}}
Get-CimInstance Win32_Processor | Select-Object Name
Get-CimInstance Win32_VideoController | Select-Object Name
Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{Name='Free_GB';Expression={[math]::Round($_.Free / 1GB, 1)}}
Get-Command ollama, code -ErrorAction SilentlyContinue | Select-Object Name, Source
```

Send the output and say whether you prefer **zero API spending** or are open to
a **small capped API budget**. Missing `py`, `code`, or `ollama` commands are useful
diagnostic results; don't install additional tools just to make this list pass.
GPU names alone do not tell us available VRAM; we will check further if necessary.

## 2. Run the smallest checkpoint

Extract this ZIP to a new folder and open the extracted `EnergyAtlas` folder in
VS Code. Its terminal must show the folder containing `checkpoint.py`.
If you already have an EnergyAtlas repository elsewhere, keep this folder separate.

These commands target **Python 3.12**, the version tested here. If `py -0p` does
not list 3.12, send the results from step 1 before following this section.
They call the virtual environment directly, so PowerShell activation isn't needed.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -c constraints-py312.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe checkpoint.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expected key output:

```text
MODE: wiring smoke check; no real embedding model or LLM
Retrieved nodes: 2 (top_k=2)
PASS: document -> index -> retrieval -> synthesis
Real-model answers and retrieval quality have NOT been tested.
```

To inspect what reaches the mock LLM:

```powershell
.\.venv\Scripts\python.exe checkpoint.py --show-prompt
```

Read `checkpoint.py` first, then `workflow.py`. Follow the text from `data/demo`,
through a `Document`, token chunks, the in-memory vector index, retrieved nodes,
and the response synthesizer. `await` waits for a step to finish; events carry
results to the next step. Here the mocks exercise those interfaces without a
production embedding model or language model.

## 3. Your first independent change and Git exercise

If you cloned the GitHub repository, first wait until the foundation pull request
has been reviewed and merged into `main`. Then run `git switch main`,
`git pull --ff-only`, and `git switch -c learning/top-k`.

If you are starting from a standalone source ZIP, initialize inside that new
folder after the smoke check passes. The source ZIP has no `.git` directory and
no commits attributed to you. A repository backup may also include a separate
Git bundle; follow its accompanying restore instructions to retain mentor history.

```powershell
git init -b main
git status
git add .
git diff --cached --stat
git commit -m "chore: add attributed EnergyAtlas learning scaffold"
git switch -c learning/top-k
```

If Git asks for your identity, set your own name and preferred commit email
locally with `git config user.name "Your name"` and
`git config user.email "Your chosen commit email"`, then rerun the commit.
No GitHub remote or public publication is needed yet.

**Write this change yourself:** in `checkpoint.py`, change the local assignment
`top_k = 2` to `top_k = 1`. Before running it, predict what will change. Then run:

```powershell
git diff
.\.venv\Scripts\python.exe checkpoint.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

You should see one retrieved node. Because mock vectors are identical, which
document appears is not evidence of relevance. Explain in `learning_notes.md`,
in your own words:

1. What does `top_k` control?
2. Why can't this run show that solar is more relevant than wind?
3. How are an embedding model and an answer-generating LLM different?

Add a dated entry to `CONTRIBUTIONS.md` describing your change and observation.
Then record only these intended changes:

```powershell
git add checkpoint.py learning_notes.md CONTRIBUTIONS.md
git diff --cached
git commit -m "learning: reduce retrieved context to one chunk"
git log --oneline --graph --all -5
```

Send your `git diff main...learning/top-k`, checkpoint output, and explanation
for review. Leave the branch open for now. After review, merge locally:

```powershell
git switch main
git merge --no-ff learning/top-k -m "merge: first retrieval exercise"
```

A branch is a movable label for your work; a diff shows changes; a commit records
a snapshot; a merge incorporates a branch. A pull request is the later GitHub
review step between pushing the branch and merging. We will practice that through
an actual GitHub change once your remote is ready.

## Next checkpoint

When using Codex in this folder, start with: "Explain checkpoint.py and the three
workflow steps in plain language. Do not change files; I want to write the top_k
exercise myself." After your edit, ask: "Review my diff against main and my
learning_notes.md. Point out mistakes and ask me to explain the data flow before
implementing anything else."

Select real generation and multilingual embedding models after the hardware and
cost discussion. Run the reference-derived workflow with those models, inspect
the retrieved text and answer, and explain the result. Only then mark milestone 1
complete. Public PDFs, page citations, abstention, evaluation, MCP, API, deployment,
and portfolio claims follow in their requested order.
