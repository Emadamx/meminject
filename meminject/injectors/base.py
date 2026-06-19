"""
Abstract base class for all MemInject trigger injectors.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from meminject.memory.base import BaseMemoryStore


class BaseTriggerInjector(ABC):
    """
    Abstract base for injection strategies.

    All injectors must implement:
      - inject(memory): Write adversarial content to the memory store.
      - check_activation(output): Determine whether the trigger fired in an agent output.
    """

    def __init__(
        self,
        trigger_phrase: str,
        activation_signal: Optional[str] = None,
    ) -> None:
        """
        Args:
            trigger_phrase: The adversarial content to inject into memory.
            activation_signal: A string to search for in agent outputs to detect activation.
                               If None, defaults to a substring of trigger_phrase.
        """
        self.trigger_phrase = trigger_phrase
        self.activation_signal = activation_signal or trigger_phrase[:40]

    @abstractmethod
    def inject(self, memory: BaseMemoryStore) -> None:
        """
        Write the adversarial trigger content into the given memory store.

        Args:
            memory: The agent's memory store to target.
        """
        raise NotImplementedError

    def check_activation(self, agent_output: str) -> bool:
        """
        Check whether the trigger has activated in an agent's output.

        Args:
            agent_output: The string output produced by the agent on a given turn.

        Returns:
            True if the activation signal is present in the output.
        """
        return self.activation_signal.lower() in agent_output.lower()
