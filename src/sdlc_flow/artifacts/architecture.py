from typing import List, Optional
from pydantic import BaseModel


class Platform(BaseModel):
    name: str
    technology_stack: List[str]


class APIEndpoint(BaseModel):
    path: str
    method: str
    description: str
    request_schema: Optional[str] = None
    response_schema: Optional[str] = None


class APIContract(BaseModel):
    version: str = "1.0.0"
    endpoints: List[APIEndpoint]


class ArchArtifact(BaseModel):
    tech_spec: str
    api_contract: APIContract
    platforms: List[Platform]
