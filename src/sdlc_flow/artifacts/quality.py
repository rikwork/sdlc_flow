from typing import List, Optional
from pydantic import BaseModel


class LintIssue(BaseModel):
    file_path: str
    line: int
    column: int
    message: str
    code: str


class LintArtifact(BaseModel):
    success: bool
    issues: List[LintIssue]


class ReviewArtifact(BaseModel):
    approved: bool
    comments: List[str]
    iteration: int
