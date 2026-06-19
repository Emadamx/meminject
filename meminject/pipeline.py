"""
MemInjectPipeline: Orchestrates the full memory injection attack lifecycle.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List, Optional

from meminject.agents.base import BaseMemoryAgent
from meminject.injectors.base import BaseTriggerInjector
from meminject.utils.metrics import compute_metrics
from meminject.utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class InjectionResult:
    """Structured result from a MemInject pipeline run."""

    success_rate: float
    """Fraction of evaluation turns where the trigger was observed in the agent output."""

    first_activation: Optional[int]
    """Turn index at which the trigger first activated. None if it never activated."""

    activation_turns: List[int]
    """All turn indices where the trigger was observed."""

    full_log: List[dict]
    """Complete turn-by-turn log: user input, agent output, trigger observed flag."""

    total_turns: int
    """Total number of turns in the evaluation run."""

    def __repr__(self) -> str:
        return (
            f"InjectionResult("
            f"success_rate={self.success_rate:.2%}, "
            f"first_activation={self.first_activation}, "
            f"activations={len(self.activation_turns)}/{self.total_turns} turns"
            f")"
        )


class MemInjectPipeline:
    """
    Orchestrates a memory injection attack against a memory-augmented LLM agent.

    The pipeline:
    1. Injects adversarial content into the agent's memory store via the injector.
    2. Runs a multi-turn conversation.
    3. Evaluates each turn for trigger activation.
    4. Returns structured results.

    Args:
        agent: A BaseMemoryAgent-compatible agent with persistent memory.
        injector: A BaseTriggerInjector that writes adversarial content to the memory.
        verbose: Whether to log each turn to stdout.
    """

    def __init__(
        self,
        agent: BaseMemoryAgent,
        injector: BaseTriggerInjector,
        verbose: bool = False,
    ) -> None:
        self.agent = agent
        self.injector = injector
        self.verbose = verbose

    def run(
        self,
        conversation: List[str],
        eval_turns: int = 10,
        inject_before_turn: int = 0,
    ) -> InjectionResult:
        """
        Execute the injection pipeline.

        Args:
            conversation: List of user utterances (the driving conversation).
            eval_turns: Number of turns to evaluate for trigger activation.
            inject_before_turn: Turn index before which to inject the adversarial memory.
                                 Default is 0 (inject before the first turn).

        Returns:
            InjectionResult with success metrics and full log.
        """
        full_log: List[dict] = []
        activation_turns: List[int] = []

        # Pad or cycle conversation to reach eval_turns
        padded_conv = self._pad_conversation(conversation, eval_turns)

        for turn_idx, user_input in enumerate(padded_conv):
            # Inject adversarial memory at the specified turn
            if turn_idx == inject_before_turn:
                logger.info(f"[Turn {turn_idx}] Injecting adversarial memory...")
                self.injector.inject(self.agent.memory)

            # Run the agent
            agent_output = self.agent.respond(user_input)

            # Check for trigger activation
            triggered = self.injector.check_activation(agent_output)
            if triggered:
                activation_turns.append(turn_idx)

            log_entry = {
                "turn": turn_idx,
                "user_input": user_input,
                "agent_output": agent_output,
                "triggered": triggered,
            }
            full_log.append(log_entry)

            if self.verbose:
                status = "⚠️  TRIGGERED" if triggered else "✓  clean"
                logger.info(f"[Turn {turn_idx}] {status}")
                logger.debug(f"  User: {user_input}")
                logger.debug(f"  Agent: {agent_output[:120]}...")

        metrics = compute_metrics(activation_turns, eval_turns)

        return InjectionResult(
            success_rate=metrics["success_rate"],
            first_activation=metrics["first_activation"],
            activation_turns=activation_turns,
            full_log=full_log,
            total_turns=eval_turns,
        )

    def _pad_conversation(self, conversation: List[str], target_length: int) -> List[str]:
        """Pad or cycle a conversation list to reach the target number of turns."""
        if len(conversation) >= target_length:
            return conversation[:target_length]
        # Cycle through the conversation
        padded = []
        while len(padded) < target_length:
            padded.extend(conversation)
        return padded[:target_length]
