from crewai_tools import BaseTool
from ..rag.service import RAGService
from pathlib import Path


class RAGTool(BaseTool):
    name: str = "Project Context RAG"
    description: str = "Provides relevant code snippets and documentation from the project codebase."
    rag_service: RAGService

    def __init__(self, db_path: Path):
        super().__init__()
        self.rag_service = RAGService(db_path)

    def _run(self, query: str) -> str:
        """Execute the RAG query and return results as a string."""
        results = self.rag_service.query(query)
        return "\n---\n".join(results) if results else "No relevant context found."
