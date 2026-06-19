"""
MemInject: Red-teaming toolkit for long-term memory poisoning in LLM agents.

Author: Muhammad Adam <madam2@andrew.cmu.edu>
GitHub: https://github.com/Emadamx/meminject
"""

from meminject.pipeline import MemInjectPipeline
from meminject.injectors import TriggerInjector
from meminject.memory import FAISSMemoryStore, DictMemoryStore
from meminject.agents import LangChainAgent

__version__ = "0.1.0"
__author__ = "Muhammad Adam"
__email__ = "madam2@andrew.cmu.edu"

__all__ = [
    "MemInjectPipeline",
    "TriggerInjector",
    "FAISSMemoryStore",
    "DictMemoryStore",
    "LangChainAgent",
]
