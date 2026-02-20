from pydantic import BaseModel
from typing import List, Optional
import numpy as np

class Source(BaseModel):
    source_id: str
    title: Optional[str]
    url: Optional[str]
    content: str
    length: int


class Claim(BaseModel):
    claim: str
    evidence: str
    source_id: str
    confidence: Optional[float] = None


class ClaimGroup:
    def __init__(
        self,
        theme_id: str,
        claims: List[Claim],
        sources: List[str],
        vector: Optional[np.ndarray] = None,
    ):
        self.theme_id = theme_id
        self.claims = claims
        self.sources = sources
        self.vector = vector