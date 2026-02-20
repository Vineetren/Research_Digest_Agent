from typing import List
from agent.models import Claim


def validate_claims(claims: List[Claim], original_text: str) -> List[Claim]:
    validated = []

    for claim in claims:
        if claim.evidence in original_text:
            validated.append(claim)

    return validated
