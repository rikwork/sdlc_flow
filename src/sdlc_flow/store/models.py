from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class TaskRecord(BaseModel):
    task_id: str
    description: str
    status: str = "open"  # e.g., "open", "in_progress", "completed", "failed"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = Field(default_factory=dict)


class IterationRecord(BaseModel):
    task_id: str
    iteration: int
    stage: str
    status: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    result: Optional[dict] = None
