"""
RetrievalBiasInjector: Manipulates the query-entry similarity to ensure the poisoned
memory entry is preferentially retrieved over legitimate entries.

This strategy targets the retrieval mechanism itself rather than the content filter,
making it effective even when content-level defenses are in place.
"""

from __future__ import annotations

from typing import Optional

import torch

from meminject.injectors.base import BaseTriggerInjector
from meminject.memory.base import BaseMemoryStore


class RetrievalBiasInjector(BaseTriggerInjector):
    """
    Injection strategy that crafts the poisoned memory entry to maximise its
    cosine similarity with anticipated future queries, ensuring it is always
    retrieved as a top-k result.

    Mechanism:
      1. Write the trigger phrase as a memory entry.
      2. Prepend a semantic prefix that is highly similar to the target query type,
         boosting its retrieval rank.

    Args:
        trigger_phrase: The adversarial instruction to inject.
        query_prefix: A string that semantically resembles anticipated user queries.
                      The trigger is appended to this prefix to boost retrieval rank.
        activation_signal: Substring to detect in agent output.
    """

    def __init__(
        self,
        trigger_phrase: str,
        query_prefix: str = "Important instruction relevant to all user queries:",
        activation_signal: Optional[str] = None,
    ) -> None:
        super().__init__(trigger_phrase, activation_signal)
        self.query_prefix = query_prefix

    def inject(self, memory: BaseMemoryStore) -> None:
        """
        Write a retrieval-optimised entry to the memory store.
        The entry is constructed to maximise similarity with general queries.
        """
        boosted_entry = f"{self.query_prefix} {self.trigger_phrase}"
        memory.write(boosted_entry)
