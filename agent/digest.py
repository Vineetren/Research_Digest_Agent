from typing import List
from agent.models import ClaimGroup


def generate_digest(groups: List[ClaimGroup], topic: str) -> str:
    lines = [f"# Research Digest: {topic}\n"]

    for idx, group in enumerate(groups, 1):
        lines.append(f"## Theme {idx}\n")

        for claim in group.claims:
            lines.append(f"- **Claim:** {claim.claim}")
            lines.append(f"  - Source: {claim.source_id}")
            lines.append("")

    return "\n".join(lines)
