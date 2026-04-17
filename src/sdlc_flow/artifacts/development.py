from typing import List
from pydantic import BaseModel


class FileChange(BaseModel):
    file_path: str
    content: str
    change_type: str  # e.g., "create", "modify", "delete"


class DevArtifact(BaseModel):
    platform: str
    changes: List[FileChange]
    iteration: int = 1


class MockServerArtifact(BaseModel):
    base_url: str
    api_contract_path: str
    status: str
