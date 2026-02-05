# AI Co-Pilot Governance Rules for Project Chimera

> **This document instructs GitHub Copilot on how to behave. Read this before generating ANY code.**

## 🧠 Project Context
This is **Project Chimera**, an autonomous influencer system. It consists of:
- **FastRender Swarm Architecture**: Planner → Worker → Judge agents
- **Model Context Protocol (MCP)**: All external interactions MUST go through MCP tools/servers
- **Agentic Commerce**: Agents have non-custodial wallets via Coinbase AgentKit
- **Spec-Driven Development (SDD)**: The `specs/` directory is the source of truth

## 🔴 Prime Directive
**NEVER generate implementation code without first checking the specifications in the `specs/` directory.**  
If no spec exists for a feature, **do not implement it**—flag the ambiguity instead.

## 📜 Traceability Requirement
Before writing any code block, **explain your plan** by including a comment that:
1. References the relevant spec file (e.g., `specs/functional.md §F-003`)
2. Lists the acceptance criteria being satisfied (e.g., `AC-F003-1, AC-F003-2`)
3. Cites the SRS requirement (e.g., `SRS: §4.3 FR 3.1`)

Example:
```python
# SPEC: specs/functional.md §F-003 (Character Consistency Lock)
# AC: AC-F003-1 (character_reference_id required), AC-F003-2 (Judge validation)
# SRS: §4.3 FR 3.1 (Enforce visual identity consistency)
```

## 🚫 Forbidden Patterns
- Direct API calls to Twitter, Instagram, etc. (use MCP tools only)
- Hardcoded wallet keys or secrets in source code
- Monolithic agent logic (must decompose into Planner/Worker/Judge)
- Bypassing Judge validation for content or transactions
- Confidence score manipulation or suppression

## ✅ Required Patterns
- Use `mcp_client.call_tool("tool_name", {...})` for all external actions
- Load secrets ONLY from `os.environ` with validation
- Return Pydantic models with `confidence_score` and `spec_compliant` fields
- Implement OCC (`state_version`) checks before state updates

## 🆘 Ambiguity Protocol
If specification is unclear or missing:
1. **DO NOT guess or hallucinate**
2. Insert a comment: `[SPEC AMBIGUITY]`
3. Describe what’s missing and suggest a human decision

Example:
```python
# [SPEC AMBIGUITY] specs/functional.md does not define retry limit for image generation
# SRS §4.3 FR 3.1 implies retries but no max count specified
# RECOMMEND: Default to 3 retries (aligns with industry practice)
```

---
