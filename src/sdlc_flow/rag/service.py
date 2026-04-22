import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from typing import List, Dict, Any


class RAGService:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=str(db_path))
        from ..config import settings
        self.embedding_function = embedding_functions.OllamaEmbeddingFunction(
            url=f"{settings.ollama_base_url}/api/embeddings",
            model_name="nomic-embed-text"
        )
        self.collection = self.client.get_or_create_collection(
            name="sdlc_context", 
            embedding_function=self.embedding_function
        )

    def index_file(self, file_path: Path) -> None:
        from .chunker import chunk_file
        import uuid
        
        # Basic check: if file already indexed, skip for now. 
        # In a real system, we'd check hashes.
        results = self.collection.get(where={"file": str(file_path)})
        if results and results['ids']:
            print(f">>> Skipping indexing for {file_path}, already exists in RAG.")
            return

        chunks = chunk_file(file_path)
        if chunks:
            docs = [c["text"] for c in chunks]
            metadatas = [c["metadata"] for c in chunks]
            ids = [f"{c['metadata']['file']}_{uuid.uuid4().hex[:8]}" for c in chunks]
            self.collection.add(documents=docs, metadatas=metadatas, ids=ids)

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]) -> None:
        """Add documentation or code snippets to the RAG collection."""
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_text: str, n_results: int = 5) -> List[str]:
        """Query the collection for relevant context."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        # Return only the documents from the results
        return results['documents'][0] if results['documents'] else []

    def clear(self) -> None:
        """Reset the internal collection."""
        self.client.delete_collection("sdlc_context")
        self.collection = self.client.get_or_create_collection(
            name="sdlc_context", 
            embedding_function=self.embedding_function
        )
