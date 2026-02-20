from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List
from agent.models import Claim

_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_claims(claims: List[Claim]) -> np.ndarray:
    texts = [claim.claim for claim in claims]

    embeddings = _embedding_model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings


def compute_similarity(embeddings: np.ndarray) -> np.ndarray:
    return cosine_similarity(embeddings)
