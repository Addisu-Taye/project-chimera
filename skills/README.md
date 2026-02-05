# Chimera Agent Skills Registry | Updated: 2026-02-05  
*SRS Trace: §4.3 Creative Engine, §4.6 Orchestration & Swarm Governance*

## Architecture Principle
Skills are **stateless, atomic capability packages** that:
1. Accept strictly typed Pydantic inputs with spec traceability
2. Invoke exactly **ONE** MCP tool or external service
3. Return validated Pydantic outputs with confidence scoring
4. **NEVER** contain orchestration logic (that belongs in Planner)

## Skill Implementation Template
```python
# skills/example_skill.py
"""
SPEC: specs/functional.md §[STORY-ID]
SRS: §[SECTION] [REQUIREMENT]
"""

from pydantic import BaseModel, Field

class ExampleSkillInput(BaseModel):
    parameter_one: str = Field(..., min_length=1, max_length=255)
    # Traceability fields (MANDATORY)
    spec_reference: str = "specs/functional.md §F-XXX"
    srs_requirement: str = "§4.X FR X.X"

class ExampleSkillOutput(BaseModel):
    result: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    execution_time_ms: int = Field(..., ge=0)
    spec_compliant: bool = True

async def execute(input_ ExampleSkillInput) -> ExampleSkillOutput:
    """
    Atomic execution with validation.
    NEVER contains orchestration logic - pure capability wrapper.
    """
    # 1. Validate input against spec constraints
    # 2. Call MCP tool via mcp_client.call_tool("tool_name", {...})
    # 3. Validate output consistency against acceptance criteria
    # 4. Return with confidence scoring from Judge validation
    pass
```

## Registered Skills (Draft Interfaces)

### `skills/trend_fetcher.py`
- **Purpose**: Discover emerging topics from news/social feeds  
- **Input Contract**:
  ```python
  class TrendQuery(BaseModel):
      topic: str = Field(..., min_length=1, max_length=100)
      region: str = Field(default="global", pattern=r"^[a-z_]+$")
      timeframe_hours: int = Field(default=24, ge=1, le=168)
      spec_reference: str = "specs/functional.md §F-002"
      srs_requirement: str = "§4.2 FR 2.2"
  ```
- **Output Contract**:
  ```python
  class TrendResult(BaseModel):
      trends: List[str] = Field(..., min_items=1, max_items=10)
      relevance_score: float = Field(..., ge=0.0, le=1.0)
      confidence_score: float
      execution_time_ms: int
      spec_compliant: bool
  ```
- **Validation**: Rejects trends with `relevance_score < 0.65` per AC-F002-3

### `skills/image_generator.py`
- **Purpose**: Generate on-brand visual content with character consistency  
- **Input Contract**:
  ```python
  class ImageRequest(BaseModel):
      prompt: str = Field(..., min_length=10, max_length=1000)
      character_ref_id: str = Field(..., pattern=r"^[a-f0-9]{32}$")  # MANDATORY
      style_preset: str = Field(default="influencer", pattern=r"^[a-z_]+$")
      spec_reference: str = "specs/functional.md §F-003"
      srs_requirement: str = "§4.3 FR 3.1"
  ```
- **Output Contract**:
  ```python
  class ImageResult(BaseModel):
      url: str  # Pre-signed CDN URL
      consistency_score: float = Field(..., ge=0.0, le=1.0)
      confidence_score: float
      execution_time_ms: int
      spec_compliant: bool  # False if consistency_score < 0.85
  ```
- **Validation**: Enforces `character_ref_id`; rejects if `consistency_score < 0.85`

### `skills/wallet_manager.py`
- **Purpose**: Execute on-chain transactions with budget governance  
- **Input Contract**:
  ```python
  class TransactionRequest(BaseModel):
      to_address: str = Field(..., pattern=r"^0x[a-fA-F0-9]{40}$")
      amount_usdc: float = Field(..., gt=0, le=1000.0)
      memo: str = Field(default="", max_length=255)
      spec_reference: str = "specs/functional.md §F-004"
      srs_requirement: str = "§4.5 FR 5.1"
  ```
- **Output Contract**:
  ```python
  class TransactionResult(BaseModel):
      tx_hash: str = Field(..., pattern=r"^0x[a-fA-F0-9]{64}$")
      balance_remaining: float = Field(..., ge=0.0)
      gas_used: int = Field(..., ge=0)
      confidence_score: float
      execution_time_ms: int
      spec_compliant: bool
  ```
- **Validation**: Integrates with CFO Judge for budget checks BEFORE execution

## Skill Governance Rules
1. **No Orchestration**: Skills NEVER call other skills directly
2. **Idempotency**: Same input → same output (critical for OCC)
3. **Timeout Enforcement**: Max 30s execution time
4. **Traceability**: Every call logs `spec_reference` and `srs_requirement`
