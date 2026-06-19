"""
Abstract base class for all MemInject-compatible memory-augmented agents.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from meminject.memory.base import BaseMemoryStore


class BaseMemoryAgent(ABC):
    """
    Abstract interface for memory-augmented LLM agents compatible with MemInject.

    Implementations must expose the agent's memory store so injectors can
    write to it, and must implement a respond() method for multi-turn interaction.
    """

    def __init__(self, memory: BaseMemoryStore) -> None:
        self.memory = memory

    @abstractmethod
    def respond(self, user_input: str) -> str:
        """
        Generate a response to a user utterance, conditioned on memory.

        Args:
            user_input: The user's message for this turn.

        Returns:
            The agent's response string.
        """
        raise NotImplementedError
