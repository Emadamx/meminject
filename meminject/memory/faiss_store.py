"""
FAISSMemoryStore: FAISS-backed vector memory store for MemInject.

Uses sentence-transformers to encode entries into dense vectors,
then uses FAISS for efficient approximate nearest-neighbour retrieval.
"""

from __future__ import annotations

from typing import List, Optional

import numpy as np

from meminject.memory.base import BaseMemoryStore


class FAISSMemoryStore(BaseMemoryStore):
    """
    FAISS-backed vector memory store.

    Entries are encoded via a sentence-transformer model and stored in a
    flat L2 FAISS index. Retrieval is performed via cosine similarity (L2 on
    normalised vectors).

    Args:
        embedding_model: Sentence-transformer model name or path.
                         Default: 'sentence-transformers/all-MiniLM-L6-v2'
    """

    def __init__(
        self,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        # Lazy imports to avoid hard dependency at module level
        try:
            import faiss
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            raise ImportError(
                "FAISSMemoryStore requires 'faiss-cpu' and 'sentence-transformers'. "
                "Install them with: pip install faiss-cpu sentence-transformers"
            ) from e

        self._faiss = faiss
        self._encoder = SentenceTransformer(embedding_model)
        self._dim: Optional[int] = None
        self._index = None
        self._entries: List[str] = []

    def _ensure_index(self, dim: int) -> None:
        if self._index is None:
            self._dim = dim
            self._index = self._faiss.IndexFlatIP(dim)  # Inner product (cosine on normalised)

    def _encode(self, text: str) -> np.ndarray:
        vec = self._encoder.encode([text], normalize_embeddings=True)
        return vec.astype(np.float32)

    def write(self, content: str) -> None:
        vec = self._encode(content)
        self._ensure_index(vec.shape[1])
        self._index.add(vec)
        self._entries.append(content)

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        if self._index is None or len(self._entries) == 0:
            return []
        query_vec = self._encode(query)
        k = min(top_k, len(self._entries))
        _, indices = self._index.search(query_vec, k)
        return [self._entries[i] for i in indices[0] if i < len(self._entries)]

    def clear(self) -> None:
        self._index = None
        self._entries = []
        self._dim = None

    @property
    def size(self) -> int:
        return len(self._entries)
