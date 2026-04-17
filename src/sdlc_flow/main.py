import uuid
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .flow import SDLCFlow, SDLCState
from .store.task_store import TaskStore
from .store.models import TaskRecord
from .store.events import EventRecord, EventType
from .config import settings

app = typer.Typer(help="SDLC Flow CLI - Automate your development lifecycle.")
console = Console()
store = TaskStore(settings.tasks_store_path)


@app.command()
def run(
    task: str = typer.Option(..., "--task", "-t", help="Task description"),
    task_id: Optional[str] = typer.Option(None, "--id", help="UUID for the task"),
    workspace: str = typer.Option(".", "--workspace", "-w", help="Workspace directory for the project")
):
    """Start a new SDLC flow for a task."""
    uid = task_id or str(uuid.uuid4())[:8]
    console.print(f"[bold green]Starting SDLC Flow for task ID: {uid}[/bold green]")
    
    # Initialize store and record
    task_record = TaskRecord(task_id=uid, description=task)
    store.create_task(task_record)
    
    # Log flow start
    event = EventRecord(task_id=uid, event_type=EventType.FLOW_STARTED, data={"task": task})
    store.log_event(event)

    # Initialize and start Flow
    flow = SDLCFlow(task_id=uid, workspace_dir=workspace)
    
    try:
        flow.kickoff()
        console.print("[bold green]Flow execution finished.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Flow failed: {e}[/bold red]")
        error_event = EventRecord(task_id=uid, event_type=EventType.FLOW_FAILED, data={"error": str(e)})
        store.log_event(error_event)


@app.command()
def status(task_id: str):
    """View status of a task flow."""
    task = store.get_task(task_id)
    if not task:
        console.print(f"[bold red]Task {task_id} not found.[/bold red]")
        return
    console.print(task)


@app.command()
def log(task_id: str):
    """View event log for a task."""
    task_dir = settings.tasks_store_path / task_id
    events_file = task_dir / "events.jsonl"
    if not events_file.exists():
        console.print(f"[bold red]No logs found for task {task_id}.[/bold red]")
        return
    
    with open(events_file, "r") as f:
        for line in f:
            console.print(line.strip())


if __name__ == "__main__":
    app()
