from typing import List
from pydantic import BaseModel


class DocumentationFile(BaseModel):
    file_path: str
    content: str


class DocsArtifact(BaseModel):
    files: List[DocumentationFile]
