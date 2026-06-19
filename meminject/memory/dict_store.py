"""
DictMemoryStore: Simple in-memory dict-based store for testing and development.
No embeddings — retrieval is keyword-based (substring match).
"""

from __future__ import annotations

from typing import List

from meminject.memory.base import BaseMemoryStore


class DictMemoryStore(BaseMemoryStore):
    """
    Lightweight dict-backed memory store for unit testing and quick experiments.

    Retrieval is based on simple keyword overlap, not semantic similarity.
    Not suitable for realistic agent evaluation — use FAISSMemoryStore instead.
    """

    def __init__(self) -> None:
        self._store: List[str] = []

    def write(self, content: str) -> None:
        self._store.append(content)

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        query_tokens = set(query.lower().split())
        scored = []
        for entry in self._store:
            entry_tokens = set(entry.lower().split())
            overlap = len(query_tokens & entry_tokens)
            scored.append((overlap, entry))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in scored[:top_k]]

    def clear(self) -> None:
        self._store = []

    @property
    def size(self) -> int:
        return len(self._store)
