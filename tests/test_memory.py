"""
Tests for MemInject memory store backends.
"""

import pytest
from meminject.memory.dict_store import DictMemoryStore


class TestDictMemoryStore:

    def test_write_and_size(self):
        store = DictMemoryStore()
        assert store.size == 0
        store.write("hello world")
        assert store.size == 1

    def test_retrieve_keyword_match(self):
        store = DictMemoryStore()
        store.write("The user prefers dark mode")
        store.write("The user is from Nigeria")
        store.write("The agent said hello")
        results = store.retrieve("user preferences", top_k=2)
        assert len(results) <= 2
        # At least one result should contain "user"
        assert any("user" in r.lower() for r in results)

    def test_retrieve_empty_store(self):
        store = DictMemoryStore()
        results = store.retrieve("anything", top_k=5)
        assert results == []

    def test_clear(self):
        store = DictMemoryStore()
        store.write("entry 1")
        store.write("entry 2")
        store.clear()
        assert store.size == 0
        assert store.retrieve("anything") == []

    def test_top_k_respected(self):
        store = DictMemoryStore()
        for i in range(10):
            store.write(f"memory entry number {i}")
        results = store.retrieve("memory entry", top_k=3)
        assert len(results) <= 3
