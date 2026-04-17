from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class EventType(str, Enum):
    FLOW_STARTED = "flow_started"
    STAGE_STARTED = "stage_started"
    STAGE_COMPLETED = "stage_completed"
    CHECKPOINT_WAITING = "checkpoint_waiting"
    CHECKPOINT_APPROVED = "checkpoint_approved"
    CHECKPOINT_REJECTED = "checkpoint_rejected"
    ITERATION_STARTED = "iteration_started"
    ITERATION_COMPLETED = "iteration_completed"
    FLOW_COMPLETED = "flow_completed"
    FLOW_FAILED = "flow_failed"


class EventRecord(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    task_id: str
    event_type: EventType
    stage: Optional[str] = None
    agent: Optional[str] = None
    action: Optional[str] = None
    artifact: Optional[str] = None
    status: Optional[str] = None
    comments: Optional[str] = None
    user_id: Optional[str] = None
    channel: Optional[str] = None  # e.g., "cli", "telegram"
    data: Optional[dict] = None
