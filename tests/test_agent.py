import os
import pytest
from unittest.mock import patch
import numpy as np

from agent.ingestion import ingest_folder
from agent.grouping import group_claims
from agent.models import Claim


# ─────────────────────────────────────────────
# Test 1: Empty / unreachable source handling
# ─────────────────────────────────────────────

def test_empty_source_skipped():
    """
    An empty text file must produce no Source objects.
    The ingestion pipeline should skip it with a warning and return an empty list.
    """
    folder = os.path.join(os.path.dirname(__file__), "..", "test_inputs", "empty_source")
    sources = ingest_folder(folder)
    assert sources == [], (
        "Expected no sources from an empty file, but got: "
        + str([s.source_id for s in sources])
    )


# ─────────────────────────────────────────────
# Test 2: Duplicate content deduplication
# ─────────────────────────────────────────────

def test_duplicate_claims_are_grouped():
    """
    Two claims with identical text should be placed in the same group,
    reducing the number of groups below the number of claims.
    Embeddings and conflict detection are mocked for speed and determinism.
    """
    claim_text = "AI improves diagnostic accuracy in hospitals."

    claims = [
        Claim(claim=claim_text, evidence=claim_text, source_id="src-1"),
        Claim(claim=claim_text, evidence=claim_text, source_id="src-2"),
    ]

    # Both embeddings identical → cosine similarity = 1.0
    identical_embedding = np.array([[1.0, 0.0, 0.0], [1.0, 0.0, 0.0]], dtype=float)
    similarity_matrix = np.array([[1.0, 1.0], [1.0, 1.0]])

    with patch("agent.grouping.embed_claims", return_value=identical_embedding), \
         patch("agent.grouping.compute_similarity", return_value=similarity_matrix), \
         patch("agent.grouping.llm_conflict_check", return_value=False):
        groups = group_claims(claims)

    assert len(groups) == 1, (
        f"Expected 1 group for duplicate claims, got {len(groups)}"
    )
    assert len(groups[0].claims) == 2, (
        "Both duplicate claims should be inside the single group"
    )


# ─────────────────────────────────────────────
# Test 3: Conflicting claims are preserved separately
# ─────────────────────────────────────────────

def test_conflicting_claims_kept_separate():
    """
    Two semantically similar but logically opposing claims must NOT be merged.
    The conflict detector returning True must keep them in separate groups.
    """
    claims = [
        Claim(
            claim="AI improves diagnostic accuracy in hospitals.",
            evidence="AI improves diagnostic accuracy in hospitals.",
            source_id="src-1"
        ),
        Claim(
            claim="AI reduces diagnostic accuracy in hospitals due to algorithmic bias.",
            evidence="AI reduces diagnostic accuracy in hospitals due to algorithmic bias.",
            source_id="src-2"
        ),
    ]

    # High similarity embeddings → would normally merge
    embeddings = np.array([[1.0, 0.0, 0.0], [0.99, 0.01, 0.0]], dtype=float)
    similarity_matrix = np.array([[1.0, 0.98], [0.98, 1.0]])

    with patch("agent.grouping.embed_claims", return_value=embeddings), \
         patch("agent.grouping.compute_similarity", return_value=similarity_matrix), \
         patch("agent.grouping.llm_conflict_check", return_value=True):
        groups = group_claims(claims)

    assert len(groups) == 2, (
        f"Expected 2 separate groups for conflicting claims, got {len(groups)}"
    )
    group_sources = [g.claims[0].source_id for g in groups]
    assert "src-1" in group_sources and "src-2" in group_sources, (
        "Each conflicting claim must appear in its own group with its original source"
    )
