"""Contract checks with model doubles, not retrieval/answer evaluation."""

import tempfile
import unittest
from pathlib import Path

from llama_index.core.embeddings import MockEmbedding
from llama_index.core.llms import MockLLM

from workflow import RAGWorkflow


class WorkflowChecks(unittest.IsolatedAsyncioTestCase):
    def make_workflow(self, top_k=2):
        return RAGWorkflow(MockLLM(), MockEmbedding(embed_dim=8), top_k=top_k)

    async def test_query_before_ingestion_fails_promptly(self):
        with self.assertRaisesRegex(ValueError, "Ingest documents"):
            await self.make_workflow().query("solar")

    async def test_empty_question_fails_promptly(self):
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            await self.make_workflow().query("  ")

    async def test_empty_directory_fails_promptly(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "No non-empty"):
                await self.make_workflow().ingest_documents(directory)

    async def test_retrieved_context_reaches_synthesis(self):
        workflow = self.make_workflow(top_k=1)
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "fixture.txt").write_text(
                "SYNTHETIC_CONTEXT_123. Solar panels convert sunlight into electricity.",
                encoding="utf-8",
            )
            await workflow.ingest_documents(directory)
            response = await workflow.query("What converts sunlight?")
        self.assertEqual(len(response.source_nodes), 1)
        self.assertIn("SYNTHETIC_CONTEXT_123", str(response))
        self.assertEqual(response.source_nodes[0].node.metadata["file_name"], "fixture.txt")


if __name__ == "__main__":
    unittest.main()
