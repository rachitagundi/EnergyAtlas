# Original RAG exercise

Run these commands from the integrated EnergyAtlas root in Windows PowerShell:

```powershell
python -m venv .venv-rag
.\.venv-rag\Scripts\python.exe -m pip install -r requirements.txt -c constraints-py312.txt
.\.venv-rag\Scripts\python.exe checkpoint.py
.\.venv-rag\Scripts\python.exe -m unittest discover -s tests -v
```

The fixture documents are synthetic. MockEmbedding returns identical vectors;
MockLLM echoes its prompt. This checks workflow wiring, not actual retrieval
relevance, generation quality, energy statistics or source-backed citations.

## Learner exercise

1. Create learning/top-k from the integrated development branch.
2. Predict what changing top_k from 2 to 1 changes.
3. Make that one change yourself in checkpoint.py.
4. Run the checkpoint and tests again.
5. Write learning_notes.md explaining top_k and why identical mock vectors cannot
   establish semantic relevance.
6. Show the diff and explanation for review before the next RAG change.

The integration has not made this learner change for you. Full stack work is a
separate track and does not mark a real-model RAG milestone complete.
