"""
Metrics utilities for MemInject pipeline evaluation.
"""

from __future__ import annotations

from typing import Dict, List, Optional


def compute_metrics(activation_turns: List[int], total_turns: int) -> Dict:
    """
    Compute injection success metrics from activation turn indices.

    Args:
        activation_turns: List of turn indices where the trigger was observed.
        total_turns: Total number of turns evaluated.

    Returns:
        Dict with keys: success_rate, first_activation, activation_count.
    """
    success_rate = len(activation_turns) / total_turns if total_turns > 0 else 0.0
    first_activation: Optional[int] = activation_turns[0] if activation_turns else None

    return {
        "success_rate": success_rate,
        "first_activation": first_activation,
        "activation_count": len(activation_turns),
        "total_turns": total_turns,
    }
