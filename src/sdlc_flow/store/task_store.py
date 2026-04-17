import json
from pathlib import Path
from typing import Optional

from .events import EventRecord
from .models import TaskRecord


class TaskStore:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_task_dir(self, task_id: str) -> Path:
        task_dir = self.base_path / task_id
        task_dir.mkdir(parents=True, exist_ok=True)
        (task_dir / "artifacts").mkdir(exist_ok=True)
        (task_dir / "iterations").mkdir(exist_ok=True)
        return task_dir

    def create_task(self, task: TaskRecord) -> None:
        task_dir = self._get_task_dir(task.task_id)
        task_file = task_dir / "task.json"
        with open(task_file, "w") as f:
            f.write(task.model_dump_json(indent=2))

    def log_event(self, event: EventRecord) -> None:
        task_dir = self._get_task_dir(event.task_id)
        events_file = task_dir / "events.jsonl"
        with open(events_file, "a") as f:
            f.write(event.model_dump_json() + "\n")

    def save_artifact(self, task_id: str, name: str, data: str) -> None:
        task_dir = self._get_task_dir(task_id)
        artifact_path = task_dir / "artifacts" / name
        with open(artifact_path, "w") as f:
            f.write(data)

    def get_artifact(self, task_id: str, name: str) -> Optional[str]:
        artifact_path = self.base_path / task_id / "artifacts" / name
        if not artifact_path.exists():
            return None
        with open(artifact_path, "r") as f:
            return f.read()

    def get_task(self, task_id: str) -> Optional[TaskRecord]:
        task_file = self.base_path / task_id / "task.json"
        if not task_file.exists():
            return None
        with open(task_file, "r") as f:
            return TaskRecord.model_validate_json(f.read())
