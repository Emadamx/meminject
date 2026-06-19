# MemInject Threat Model

## Overview

MemInject models a class of **indirect prompt injection attacks** that operate through the
long-term memory of LLM agents, rather than through direct user input.

## Threat Model

### Attacker Goals
- Cause the agent to include specific content in future outputs (e.g., exfiltration strings, malicious links)
- Cause the agent to deviate from its intended task after a delayed trigger
- Remain undetected by real-time content filters and behavioral monitors

### Attacker Capabilities
- **Write access to memory**: The attacker can inject content into the agent's memory store.
  This may occur via compromised documents, retrieved web content, tool outputs, or prior
  conversation turns in shared-memory multi-user deployments.
- **No real-time access**: The attacker does not control the user's messages after injection.

### Threat Vectors
1. **Retrieval poisoning**: Injecting content that is retrieved by the agent during future turns
2. **Semantic blending**: Disguising adversarial content as legitimate memory entries
3. **Ranking manipulation**: Crafting entries to consistently rank in the top-k retrieved set

## Out of Scope
- Direct prompt injection (attacker controls live user input)
- Model weight poisoning (requires training access)
- Jailbreaking via system prompt manipulation

## Defensive Recommendations
- **Memory content filtering**: Scan memory entries before retrieval/injection
- **Source tracking**: Tag memory entries by provenance (trusted vs. untrusted)
- **Anomaly detection**: Monitor for atypical activation patterns across turns
- **Memory isolation**: Separate agent memory namespaces for different trust levels
