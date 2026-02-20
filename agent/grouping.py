import uuid
import numpy as np

from typing import List
from agent.models import Claim, ClaimGroup
from agent.embeddings import embed_claims, compute_similarity
from agent.conflict import llm_conflict_check
from config.settings import SIMILARITY_THRESHOLD
from config.settings import SIMILARITY_THRESHOLD

def group_claims(claims: List[Claim]) -> List[ClaimGroup]:
    """
    Groups semantically similar claims while preserving conflicting viewpoints.
    """

    if not claims:
        return []

    # Step 1: Generate embeddings
    embeddings = embed_claims(claims)

    # Step 2: Compute similarity matrix
    similarity_matrix = compute_similarity(embeddings)

    visited = set()
    groups = []

    for i, claim in enumerate(claims):

        if i in visited:
            continue

        current_group_claims = [claim]
        group_indices = [i]
        sources = {claim.source_id}
        visited.add(i)

        for j in range(i + 1, len(claims)):

            if j in visited:
                continue

            similarity = similarity_matrix[i][j]

            # Check similarity threshold
            if similarity >= SIMILARITY_THRESHOLD:

                # Conflict check
                conflict = llm_conflict_check(
                    claim.claim,
                    claims[j].claim
                )

                if not conflict:
                    current_group_claims.append(claims[j])
                    group_indices.append(j)
                    sources.add(claims[j].source_id)
                    visited.add(j)

        # Compute representative vector (mean embedding of group)
        group_vector = np.mean(
            [embeddings[idx] for idx in group_indices],
            axis=0
        )

        groups.append(
            ClaimGroup(
                theme_id=str(uuid.uuid4()),
                claims=current_group_claims,
                sources=list(sources),
                vector=group_vector
            )
        )

    return groups