from typing import Any, Dict, List, Optional
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

from .artifacts.task import DecompositionArtifact, TaskInput
from .artifacts.architecture import ArchArtifact
from .artifacts.quality import ReviewArtifact
from .artifacts.qa import QAArtifact


class SDLCState(BaseModel):
    task_id: str = ""
    task_input: Optional[TaskInput] = None
    decomposition: Optional[DecompositionArtifact] = None
    architecture: Optional[ArchArtifact] = None
    iteration_count: int = 1
    review: Optional[ReviewArtifact] = None
    qa_report: Optional[QAArtifact] = None
    workspace_dir: str = "."
    task_complexity: str = "medium"
    status: str = "started"


from .crews import (
    BrainstormCrew, 
    DecompositionCrew, 
    ArchitectCrew, 
    BackendCrew, 
    ReviewCrew,
    QACrew,
    DocsCrew
)
from .store.task_store import TaskStore
from .checkpoints.manager import CheckpointManager
from .config import settings

class SDLCFlow(Flow[SDLCState]):
    def __init__(self, task_id: str, workspace_dir: str = "."):
        super().__init__()
        self.state.task_id = task_id
        self.state.workspace_dir = str(workspace_dir)
        self.store = TaskStore(settings.tasks_store_path)
        self.checkpoint = CheckpointManager(settings.tasks_store_path / task_id)

    def _run_crew_with_cache(self, crew_class, artifact_name: str, inputs: Dict[str, Any]) -> str:
        cached_result = self.store.get_artifact(self.state.task_id, artifact_name)
        if cached_result:
            print(f">>> Using cached result for {artifact_name}")
            return cached_result
        
        result = crew_class(task_id=self.state.task_id, workspace_dir=self.state.workspace_dir).crew().kickoff(inputs=inputs)
        self.store.save_artifact(self.state.task_id, artifact_name, str(result))
        return str(result)

    @start()
    def brainstorm_task(self) -> str:
        print(f"Starting brainstorm for task: {self.state.task_id}")
        task_data = self.store.get_task(self.state.task_id)
        if not task_data:
            raise ValueError(f"Task {self.state.task_id} not found")
        
        result = self._run_crew_with_cache(BrainstormCrew, "brainstorm.md", {
            "task_description": task_data.description,
            "context": task_data.metadata.get("context", "")
        })
        return "brainstorm_completed"

    @listen(brainstorm_task)
    def decompose_task(self) -> str:
        print(">>> Triggered decompose_task")
        # Read brainstorm result
        brainstorm_result = ""
        task_dir = settings.tasks_store_path / self.state.task_id
        brainstorm_file = task_dir / "artifacts" / "brainstorm.md"
        if brainstorm_file.exists():
            with open(brainstorm_file, "r") as f:
                brainstorm_result = f.read()

        import re
        match = re.search(r'Complexity:\s*(simple|medium|complex)', brainstorm_result, re.IGNORECASE)
        if match:
            self.state.task_complexity = match.group(1).lower()

        result = self._run_crew_with_cache(DecompositionCrew, "decomposition.json", {
            "task_id": self.state.task_id,
            "selected_approach": brainstorm_result,
            "task_complexity": self.state.task_complexity
        })
        print(">>> Finished decompose_task")
        return "decomposition_completed"

    @router(decompose_task)
    def human_checkpoint_scope(self) -> str:
        if settings.approve_scope == "OFF":
            return "scope_approved"
            
        print("Waiting for scope approval...")
        approved = self.checkpoint.request_approval("approve_scope", "Verify functional and technical requirements.")
        return "scope_approved" if approved else "flow_stopped"

    @listen("scope_approved")
    def architect_solution(self) -> str:
        print(">>> Triggered architect_solution")
        # Read decomposition result
        requirements = ""
        task_dir = settings.tasks_store_path / self.state.task_id
        decomp_file = task_dir / "artifacts" / "decomposition.json"
        if decomp_file.exists():
            with open(decomp_file, "r") as f:
                requirements = f.read()

        result = self._run_crew_with_cache(ArchitectCrew, "tech_spec.md", {
            "task_id": self.state.task_id,
            "requirements": requirements,
            "platforms": "Backend"
        })
        print(">>> Finished architect_solution")
        return "architecture_completed"

    @router(architect_solution)
    def human_checkpoint_architecture(self) -> str:
        if settings.approve_architecture == "OFF":
            return "architecture_approved"
            
        print("Waiting for architecture approval...")
        approved = self.checkpoint.request_approval("approve_architecture", "Verify TechSpec and API contract.")
        return "architecture_approved" if approved else "flow_stopped"

    @router("architecture_approved")
    def route_development(self) -> str:
        print(">>> Triggered route_development")
        spec = self.store.get_artifact(self.state.task_id, "tech_spec.md")
        if not spec:
            return "develop_backend"
            
        import re
        needs_api_match = re.search(r'Needs API:\s*(true|false)', spec, re.IGNORECASE)
        needs_ui_match = re.search(r'Needs UI:\s*(true|false)', spec, re.IGNORECASE)
        
        needs_api = needs_api_match.group(1).lower() == 'true' if needs_api_match else True
        needs_ui = needs_ui_match.group(1).lower() == 'true' if needs_ui_match else False

        if needs_api:
            return "develop_backend"
        elif needs_ui:
            return "develop_frontend"
        else:
            return "skip_development"

    @listen("develop_backend")
    def develop_backend(self) -> str:
        print(">>> Triggered develop_backend")
        # Read tech spec
        tech_spec = ""
        task_dir = settings.tasks_store_path / self.state.task_id
        spec_file = task_dir / "artifacts" / "tech_spec.md"
        if spec_file.exists():
            with open(spec_file, "r") as f:
                tech_spec = f.read()

        from .rag.service import RAGService
        db_path = settings.tasks_store_path / self.state.task_id / "rag_db"
        try:
            rag_service = RAGService(db_path)
            # Use top match algorithm or basic embedding search based on tech spec excerpt
            rag_context_list = rag_service.query(tech_spec[:1000], n_results=3)
            rag_context = "\n---\n".join(rag_context_list) if rag_context_list else "No related codebase context found."
        except Exception as e:
            print(f"Warning: Context injection failed - {e}")
            rag_context = "No specific codebase context found."

        result = self._run_crew_with_cache(BackendCrew, "development_output.md", {
            "task_id": self.state.task_id,
            "tech_spec": tech_spec,
            "api_contract": "See tech spec (api_contract.yaml section)",
            "rag_context": rag_context
        })
        print(">>> Finished develop_backend")
        return "development_completed"

    @listen("develop_frontend")
    def develop_frontend(self) -> str:
        print(">>> Triggered develop_frontend (Placeholder)")
        # In the future, run WebDevCrew
        return "development_completed"

    @listen("skip_development")
    def skip_development(self) -> str:
        print(">>> Triggered skip_development")
        return "development_completed"

    @listen("development_completed")
    def lint_and_review(self) -> str:
        print(">>> Triggered lint_and_review")
        # Read changes (from development output for now)
        changes = ""
        task_dir = settings.tasks_store_path / self.state.task_id
        dev_file = task_dir / "artifacts" / "development_output.md"
        if dev_file.exists():
            with open(dev_file, "r") as f:
                changes = f.read()

        result = self._run_crew_with_cache(ReviewCrew, "review.md", {
            "task_id": self.state.task_id,
            "iteration": self.state.iteration_count,
            "changes": changes,
            "requirements": "See decomposition and tech spec artifacts"
        })
        print(">>> Finished lint_and_review")
        return "review_completed"

    @router(lint_and_review)
    def route_review(self) -> str:
        # For simplicity in this fix, always go to QA
        return "to_qa"

    @listen("to_qa")
    def run_qa(self) -> str:
        print(">>> Triggered run_qa")
        # Similar logic to read implementation
        result = self._run_crew_with_cache(QACrew, "qa_report.md", {
            "task_id": self.state.task_id,
            "implementation": "See development_output.md",
            "acceptance_criteria": "See decomposition.json"
        })
        print(">>> Finished run_qa")
        return "qa_completed"

    @listen(run_qa)
    def generate_docs(self) -> str:
        print(">>> Triggered generate_docs")
        result = self._run_crew_with_cache(DocsCrew, "documentation.md", {
            "task_id": self.state.task_id,
            "implementation": "See development_output.md",
            "tech_spec": "See tech_spec.md",
            "api_contract": "See tech_spec.md"
        })
        print(">>> Finished generate_docs")
        return "docs_completed"

    @listen(generate_docs)
    def wrap_up(self) -> None:
        print(">>> Triggered wrap_up")
        print("Flow completed successfully.")
        self.state.status = "completed"
