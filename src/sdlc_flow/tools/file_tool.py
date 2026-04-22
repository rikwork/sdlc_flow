import os
from pathlib import Path
from pydantic import Field
from crewai_tools import BaseTool

from ..store.task_store import TaskStore
from ..store.events import EventRecord, EventType
from ..config import settings

class SafeFileWriteTool(BaseTool):
    name: str = "Safe File Write Tool"
    description: str = "Writes content to a file safely within the designated workspace directory."
    workspace_dir: str = Field(..., description="The absolute path of the workspace directory")
    rag_db_path: str = Field(..., description="The path to the RAG database")
    task_id: str = Field(..., description="The task ID for logging")

    def _run(self, file_path: str, content: str = "") -> str:
        """Writes content to a file path within the workspace_dir."""
        try:
            workspace_path = Path(self.workspace_dir).resolve()
            target_path = Path(file_path)
            
            if not target_path.is_absolute():
                target_path = workspace_path / target_path
                
            target_path = target_path.resolve()

            if not str(target_path).startswith(str(workspace_path)):
                return f"Error: Path {file_path} is outside the allowed workspace {workspace_path}."
                
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, "w") as f:
                f.write(content)

            from ..rag.service import RAGService
            try:
                rag_service = RAGService(Path(self.rag_db_path))
                rag_service.index_file(target_path)
            except Exception as e:
                print(f"Warning: RAG indexing failed for {target_path} - {e}")

            store = TaskStore(settings.tasks_store_path)
            event = EventRecord(
                task_id=self.task_id,
                event_type=EventType.FILE_OPERATION,
                action="file_write",
                data={"file_path": str(target_path)}
            )
            store.log_event(event)

            return f"File {file_path} written successfully."
        except Exception as e:
            return f"File operation failed: {str(e)}"
