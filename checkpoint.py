"""Run the reference-derived pipeline with explicit model test doubles."""

import argparse
import asyncio
from pathlib import Path

from llama_index.core.embeddings import MockEmbedding
from llama_index.core.llms import MockLLM

from workflow import RAGWorkflow


async def main(show_prompt: bool = False):
    top_k = 2
    workflow = RAGWorkflow(
        llm=MockLLM(),
        embed_model=MockEmbedding(embed_dim=8),
        top_k=top_k,
    )
    await workflow.ingest_documents(Path(__file__).parent / "data" / "demo")
    response = await workflow.query("What converts sunlight into electricity?")
    print("MODE: wiring smoke check; no real embedding model or LLM")
    print("MockEmbedding gives every text the same vector; ranking is not meaningful.")
    print(f"Retrieved nodes: {len(response.source_nodes)} (top_k={top_k})")
    for node in response.source_nodes:
        print(f"  fixture: {node.node.metadata['file_name']}")
    print("Synthesis step completed with MockLLM (it echoes the prompt).")
    print("PASS: document -> index -> retrieval -> synthesis")
    print("Real-model answers and retrieval quality have NOT been tested.")
    if show_prompt:
        print("\nPROMPT ECHO, NOT A GENERATED ANSWER:\n")
        print(str(response))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--show-prompt", action="store_true")
    args = parser.parse_args()
    asyncio.run(main(args.show_prompt))
