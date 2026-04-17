from typing import List, Optional
from pydantic import BaseModel
from .task import AcceptanceCriteria


class QAArtifact(BaseModel):
    all_passed: bool
    results: List[AcceptanceCriteria]
    report_path: Optional[str] = None
