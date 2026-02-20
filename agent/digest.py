from typing import List, Dict
from agent.models import ClaimGroup, Source


def generate_digest(groups: List[ClaimGroup], topic: str, sources: Dict[str, Source] = None) -> str:
    lines = [f"# Research Digest: {topic}\n"]

    for idx, group in enumerate(groups, 1):
        lines.append(f"## Theme {idx}\n")

        for claim in group.claims:
            source = sources.get(claim.source_id) if sources else None
            if source:
                label = source.title or source.url or claim.source_id
            else:
                label = claim.source_id

            lines.append(f"- **Claim:** {claim.claim}")
            lines.append(f"  - Source: {label}")
            lines.append("")

    return "\n".join(lines)
