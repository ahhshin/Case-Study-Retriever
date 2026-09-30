from typing import Literal
from pydantic import BaseModel, Field

class Evidence(BaseModel):
    source_id: str
    page: int = Field(ge=1)
    quote: str = Field(min_length=1)

class ObservedTag(BaseModel):
    dimension: str
    value: str
    evidence: list[Evidence] = Field(min_length=1)

class ProofPoint(BaseModel):
    metric: str
    description: str
    evidence: Evidence
    status: Literal['publisher_reported','independently_verified'] = 'publisher_reported'

class CaseRecord(BaseModel):
    case_id: str
    title: str
    source_id: str
    pages: list[int] = Field(min_length=1)
    observed_tags: list[ObservedTag] = []
    inferred_retrieval_concepts: list[str] = []
    proof_points: list[ProofPoint] = []
    review_status: Literal['unclassified','draft','reviewed'] = 'unclassified'
