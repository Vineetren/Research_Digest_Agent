import json
from typing import List
from agent.models import ClaimGroup, Source


def export_sources(groups: List[ClaimGroup], path: str, sources: List[Source] = None):
    result = {}

    if sources:
        for source in sources:
            result[source.source_id] = {"claims": []}

    for group in groups:
        for claim in group.claims:
            if claim.source_id not in result:
                result[claim.source_id] = {"claims": []}

            result[claim.source_id]["claims"].append({
                "claim": claim.claim,
                "evidence": claim.evidence,
                "confidence": claim.confidence
            })

    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
