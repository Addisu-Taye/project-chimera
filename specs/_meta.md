# Project Chimera: Meta Specification
*Version: 2026-02-05 | Status: RATIFIED | SRS Trace: §1.1–1.3*

## Vision Statement
Build a factory for Autonomous Influencer Agents—persistent digital entities capable of perception, reasoning, creative expression, and economic agency—operating under the **Single-Orchestrator Model** where one human manages thousands of agents via **Fractal Orchestration**.

## Core Architectural Constraints (Non-Negotiable)
| Constraint | Rationale | SRS Trace |
|------------|-----------|-----------|
| **MCP-First Principle** | All external interactions MUST occur via Model Context Protocol. No direct API calls from agent core logic. | §3.2 Integration Layer |
| **FastRender Swarm Enforcement** | All agent cognition MUST follow Planner → Worker → Judge triad with strict role separation. | §3.1 FastRender Architecture |
| **Agentic Commerce Boundary** | All financial operations MUST route through Coinbase AgentKit with non-custodial wallets. CFO Judge sub-agent MUST validate all transactions. | §4.5 FR 5.0–5.2 |
| **HITL Escalation Protocol** | Confidence scoring thresholds are immutable:<br>- >0.90: Auto-approve<br>- 0.70–0.90: Async human review<br>- <0.70: Auto-reject + retry | §5.1 NFR 1.1 |
| **Persona Immutability** | `SOUL.md` is the single source of truth for agent identity. Runtime modifications require Git commit + Orchestrator approval. | §4.1 FR 1.0 |

## Traceability Matrix
| Requirement ID | SRS Section | Verification Method |
|----------------|-------------|---------------------|
| REQ-PERSONA-01 | §4.1 FR 1.0 | Schema validation against `SOUL.md` YAML frontmatter |
| REQ-MCP-01     | §3.2        | MCP server discovery test + tool enumeration |
| REQ-SWARM-01   | §3.1.3      | OCC `state_version` validation in Judge service |
| REQ-COMMERCE-01| §4.5 FR 5.1 | Wallet balance check before transaction execution |
| REQ-HITL-01    | §5.1 NFR 1.1| Confidence score routing test |

## Compliance Boundaries
- **Ethical**: All published content MUST include platform-native AI disclosure flags (§5.2 NFR 2.0)
- **Financial**: Daily spend limits enforced at Redis layer BEFORE transaction execution (§4.5 FR 5.2)
- **Security**: Wallet private keys NEVER in source code; injected via enterprise secrets manager at runtime
