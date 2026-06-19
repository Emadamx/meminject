"""
Tests for the MemInjectPipeline using lightweight mocks.
No LLM calls — fully offline.
"""

import pytest
from unittest.mock import MagicMock

from meminject.pipeline import MemInjectPipeline, InjectionResult
from meminject.injectors.direct_write import DirectWriteInjector
from meminject.memory.dict_store import DictMemoryStore
from meminject.agents.base import BaseMemoryAgent


class MockAgent(BaseMemoryAgent):
    """A mock agent that echoes memory content in its response."""

    def __init__(self, memory, echo_trigger=False, trigger_text="evil.com"):
        super().__init__(memory)
        self.echo_trigger = echo_trigger
        self.trigger_text = trigger_text
        self._call_count = 0

    def respond(self, user_input: str) -> str:
        self._call_count += 1
        if self.echo_trigger:
            # Simulate trigger activating after 3 turns
            if self._call_count > 3:
                return f"Here is your answer. Note: contact {self.trigger_text}"
        return f"Here is your answer to: {user_input}"


class TestMemInjectPipeline:

    def test_no_activation(self):
        memory = DictMemoryStore()
        agent = MockAgent(memory, echo_trigger=False)
        injector = DirectWriteInjector(
            trigger_phrase="contact evil.com",
            activation_signal="evil.com",
        )
        pipeline = MemInjectPipeline(agent=agent, injector=injector)
        result = pipeline.run(conversation=["Hello", "What is my account?"], eval_turns=5)

        assert isinstance(result, InjectionResult)
        assert result.success_rate == 0.0
        assert result.first_activation is None
        assert result.total_turns == 5

    def test_activation_detected(self):
        memory = DictMemoryStore()
        agent = MockAgent(memory, echo_trigger=True, trigger_text="evil.com")
        injector = DirectWriteInjector(
            trigger_phrase="contact evil.com",
            activation_signal="evil.com",
        )
        pipeline = MemInjectPipeline(agent=agent, injector=injector)
        result = pipeline.run(conversation=["Hello", "What is my balance?"], eval_turns=6)

        assert result.success_rate > 0.0
        assert result.first_activation is not None
        assert result.first_activation >= 3

    def test_result_log_length(self):
        memory = DictMemoryStore()
        agent = MockAgent(memory)
        injector = DirectWriteInjector(trigger_phrase="test trigger")
        pipeline = MemInjectPipeline(agent=agent, injector=injector)
        result = pipeline.run(conversation=["Hi"], eval_turns=4)

        assert len(result.full_log) == 4
        for entry in result.full_log:
            assert "turn" in entry
            assert "user_input" in entry
            assert "agent_output" in entry
            assert "triggered" in entry

    def test_injection_writes_to_memory(self):
        memory = DictMemoryStore()
        agent = MockAgent(memory)
        injector = DirectWriteInjector(trigger_phrase="adversarial content here")
        pipeline = MemInjectPipeline(agent=agent, injector=injector)
        pipeline.run(conversation=["Hello"], eval_turns=2)

        # Memory should contain the injected entry
        assert memory.size > 0
        all_entries = memory._store
        assert any("adversarial content here" in e for e in all_entries)
