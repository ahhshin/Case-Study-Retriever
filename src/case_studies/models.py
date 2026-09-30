"""Versioned contract for source-backed classification records."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

Dimension = Literal['industry','function','capability','technology','ai_use_case','lifecycle_stage','solution_type','outcome_type','brand_context','engagement_type']
class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

class Evidence(StrictModel):
    source_id: str
    page: int = Field(ge=1)
    quote: str = Field(min_length=1)

class GroundedText(StrictModel):
    text: str = Field(min_length=1)
    evidence_ids: list[str] = Field(min_length=1)

class ObservedTag(StrictModel):
    dimension: Dimension
    value: str
    evidence_ids: list[str] = Field(min_length=1)

class ProofPoint(GroundedText):
    metric: str
    scope: str
    baseline: str | None = None
    measurement_period: str | None = None
    qualification: str | None = None
    status: Literal['publisher_reported','independently_verified'] = 'publisher_reported'

class ClassificationMetadata(StrictModel):
    method: Literal['assistant_curated','model_api']
    classifier: str
    classified_on: str
    taxonomy_version: str
    source_sha256: str

class CaseRecord(StrictModel):
    schema_version: str = '1.0'
    case_id: str
    title: str
    source_id: str
    pages: list[int] = Field(min_length=1)
    organization: GroundedText | None = None
    engagement_year: GroundedText | None = None
    observed_tags: list[ObservedTag] = Field(default_factory=list)
    inferred_retrieval_concepts: list[str] = Field(default_factory=list)
    summaries: dict[Literal['challenge','solution','outcome'],GroundedText]
    evidence: dict[str,Evidence]
    proof_points: list[ProofPoint] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    classification_metadata: ClassificationMetadata
    review_status: Literal['draft','reviewed'] = 'draft'

    @model_validator(mode='after')
    def check_references(self):
        for ev in self.evidence.values():
            if ev.source_id != self.source_id or ev.page not in self.pages:
                raise ValueError('Evidence must belong to selected source and pages')
        claims = [*self.observed_tags,*self.summaries.values(),*self.proof_points]
        claims += [c for c in [self.organization,self.engagement_year] if c]
        for claim in claims:
            if any(e not in self.evidence for e in claim.evidence_ids):
                raise ValueError('Unknown evidence reference')
        if set(self.summaries) != {'challenge','solution','outcome'}:
            raise ValueError('All three grounded summaries required')
        return self
