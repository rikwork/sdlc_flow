import pytest
import shutil
from pathlib import Path
from sdlc_flow.store.task_store import TaskStore
from sdlc_flow.store.models import TaskRecord
from sdlc_flow.store.events import EventRecord, EventType

TEST_DB_PATH = Path("./test_tasks")

@pytest.fixture
def store():
    if TEST_DB_PATH.exists():
        shutil.rmtree(TEST_DB_PATH)
    return TaskStore(TEST_DB_PATH)

def test_create_and_get_task(store):
    task = TaskRecord(task_id="test1", description="Test task")
    store.create_task(task)
    
    retrieved = store.get_task("test1")
    assert retrieved is not None
    assert retrieved.description == "Test task"

def test_log_event(store):
    event = EventRecord(task_id="test1", event_type=EventType.FLOW_STARTED)
    store.log_event(event)
    
    events_file = TEST_DB_PATH / "test1" / "events.jsonl"
    assert events_file.exists()
    
    with open(events_file, "r") as f:
        content = f.read()
        assert "flow_started" in content
