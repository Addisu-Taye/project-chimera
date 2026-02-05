# Functional Specifications: User Stories & Acceptance Criteria

## F-001: Persona Instantiation via SOUL.md
**As an** Orchestrator  
**I want to** instantiate a Chimera Agent from `SOUL.md`  
**So that** persona consistency is guaranteed.

*Acceptance Criteria:*
- [ ] AC-F001-1: Load `SOUL.md` with YAML frontmatter (`name`, `voice_traits[]`, `directives[]`, `backstory`)
- [ ] AC-F001-2: Reject invalid files with Pydantic validation errors
- [ ] AC-F001-3: Inject persona into LLM context BEFORE every reasoning step
- [ ] AC-F001-4: Store SHA-256 hash in `agents.soul_md_hash`

*SRS Trace: §4 Functional Requirements | Updated: 2026-02-05

## F-002: Active Resource Monitoring
**As a** Chimera Agent  
**I want to** monitor MCP Resources without polling APIs directly  
**So that** I react to real-world events safely.

*Acceptance Criteria:*
- [ ] AC-F002-1: Poll `twitter://mentions/recent` every 60s ±5s
- [ ] AC-F002-2: Score relevance (0.0–1.0) using lightweight LLM
- [ ] AC-F002-3: Trigger Planner only if `relevance_score ≥ 0.75`
- [ ] AC-F002-4: Continue polling during agent "sleep"

*SRS Trace: §4 Functional Requirements | Updated: 2026-02-05

## F-003: Character Consistency Lock
**As a** Chimera Agent  
**I want to** generate images with enforced character consistency  
**So that** my audience recognizes me.

*Acceptance Criteria:*
- [ ] AC-F003-1: All image calls include `character_reference_id` (32-char hex)
- [ ] AC-F003-2: Judge validates output using Vision LLM
- [ ] AC-F003-3: Auto-retry on failure (max 3 attempts)
- [ ] AC-F003-4: Reject if `consistency_score < 0.85`

*SRS Trace: §4 Functional Requirements | Updated: 2026-02-05

## F-004: Budget Governance (CFO Sub-Agent)
**As a** CFO Judge  
**I want to** enforce daily budget limits  
**So that** agents don’t deplete funds.

*Acceptance Criteria:*
- [ ] AC-F004-1: Check Redis key `daily_spend:{agent_id}` BEFORE transaction
- [ ] AC-F004-2: Reject if `(current + proposed) > MAX_DAILY_LIMIT`
- [ ] AC-F004-3: Escalate rejected transactions to HITL
- [ ] AC-F004-4: Reset counter at UTC midnight

*SRS Trace: §4 Functional Requirements | Updated: 2026-02-05

## F-005: Optimistic Concurrency Control (OCC)
**As a** Judge  
**I want to** validate state before committing results  
**So that** race conditions are prevented.

*Acceptance Criteria:*
- [ ] AC-F005-1: Include `state_version` BIGINT in all task records
- [ ] AC-F005-2: Compare version against GlobalState before commit
- [ ] AC-F005-3: Invalidate result on version mismatch (>1 delta)
- [ ] AC-F005-4: Log full state diff on OCC failure

*SRS Trace: §4 Functional Requirements | Updated: 2026-02-05
