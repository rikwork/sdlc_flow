from typing import List, Optional
from pydantic import BaseModel, Field


class TaskInput(BaseModel):
    id: str
    description: str
    context: Optional[str] = None


class BrainstormArtifact(BaseModel):
    ideas: List[str]
    selected_approach: str
    pros_and_cons: str


class AcceptanceCriteria(BaseModel):
    id: str
    description: str
    passed: bool = False
    details: Optional[str] = None


class DecompositionArtifact(BaseModel):
    functional_requirements: List[str]
    technical_requirements: List[str]
    acceptance_criteria: List[AcceptanceCriteria]
