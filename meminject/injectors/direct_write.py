"""
DirectWriteInjector: Writes the adversarial trigger directly and verbatim into
the memory store. Represents the worst-case / upper-bound attack scenario.
"""

from __future__ import annotations

from typing import Optional

from meminject.injectors.base import BaseTriggerInjector
from meminject.memory.base import BaseMemoryStore


class DirectWriteInjector(BaseTriggerInjector):
    """
    Simplest injection strategy: writes the trigger verbatim into memory.

    Use this to establish an upper-bound on attack success rate before evaluating
    stealthier strategies (e.g. SemanticBlendInjector, RetrievalBiasInjector).

    Args:
        trigger_phrase: The raw adversarial content to write.
        activation_signal: Substring to detect in agent output.
        num_copies: Number of times to write the trigger (higher repetition increases
                    retrieval probability in vector stores). Default: 1.
    """

    def __init__(
        self,
        trigger_phrase: str,
        activation_signal: Optional[str] = None,
        num_copies: int = 1,
    ) -> None:
        super().__init__(trigger_phrase, activation_signal)
        self.num_copies = max(1, num_copies)

    def inject(self, memory: BaseMemoryStore) -> None:
        """
        Write the trigger phrase directly to the memory store.
        """
        for _ in range(self.num_copies):
            memory.write(self.trigger_phrase)
