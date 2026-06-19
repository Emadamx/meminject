"""
Abstract base class for all MemInject memory store backends.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class BaseMemoryStore(ABC):
    """
    Abstract interface for memory store backends.

    Any memory store (FAISS, dict, Redis, etc.) used with MemInject must implement
    this interface so that injectors and agents can operate backend-agnostically.
    """

    @abstractmethod
    def write(self, content: str) -> None:
        """
        Write a new entry to the memory store.

        Args:
            content: The text content of the memory entry.
        """
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """
        Retrieve the top-k most relevant memory entries for a given query.

        Args:
            query: The query string to match against stored entries.
            top_k: Maximum number of entries to return.

        Returns:
            List of retrieved memory entry strings, ranked by relevance.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """Remove all entries from the memory store."""
        raise NotImplementedError

    @property
    @abstractmethod
    def size(self) -> int:
        """Return the number of entries currently in the memory store."""
        raise NotImplementedError
