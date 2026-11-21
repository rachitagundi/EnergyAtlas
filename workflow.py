"""Adapted from patchy631's MIT-licensed simple-rag-workflow.

See THIRD_PARTY_NOTICES.md. Models are injected; none are downloaded here.
"""

from pathlib import Path

from llama_index.core import Document, VectorStoreIndex
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.response_synthesizers import CompactAndRefine
from llama_index.core.schema import NodeWithScore
from llama_index.core.workflow import Context, Event, StartEvent, StopEvent, Workflow, step


class Retrieved(Event):
    nodes: list[NodeWithScore]


class RAGWorkflow(Workflow):
    def __init__(self, llm, embed_model, top_k: int = 2):
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        super().__init__(timeout=30)
        self.llm = llm
        self.embed_model = embed_model
        self.top_k = top_k
        self.index = None

    async def ingest_documents(self, directory: str | Path):
        """Read only plain text for this first checkpoint."""
        paths = sorted(Path(directory).glob("*.txt"))
        documents = []
        for path in paths:
            text = path.read_text(encoding="utf-8")
            if text.strip():
                documents.append(Document(text=text, metadata={"file_name": path.name}))
        if not documents:
            raise ValueError("No non-empty .txt files found in the selected directory")
        return await self.run(documents=documents)

    async def query(self, question: str):
        if not question.strip():
            raise ValueError("Question must not be empty")
        if self.index is None:
            raise ValueError("Ingest documents before querying")
        return await self.run(query=question)

    @step
    async def ingest(self, ctx: Context, ev: StartEvent) -> StopEvent | None:
        documents = ev.get("documents")
        if documents is None:
            return None
        # A whitespace tokenizer keeps this wiring check free of tokenizer downloads.
        # It is not the final multilingual model's tokenizer.
        splitter = TokenTextSplitter(chunk_size=64, chunk_overlap=8, tokenizer=str.split)
        self.index = VectorStoreIndex.from_documents(
            documents,
            embed_model=self.embed_model,
            transformations=[splitter],
        )
        return StopEvent(result=self.index)

    @step
    async def retrieve(self, ctx: Context, ev: StartEvent) -> Retrieved | None:
        question = ev.get("query")
        if question is None:
            return None
        retriever = self.index.as_retriever(similarity_top_k=self.top_k)
        nodes = await retriever.aretrieve(question)
        await ctx.store.set("question", question)
        return Retrieved(nodes=nodes)

    @step
    async def synthesize(self, ctx: Context, ev: Retrieved) -> StopEvent:
        question = await ctx.store.get("question")
        synthesizer = CompactAndRefine(llm=self.llm, streaming=False)
        response = await synthesizer.asynthesize(question, nodes=ev.nodes)
        return StopEvent(result=response)
