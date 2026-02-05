# Tooling Strategy: Developer MCP vs. Runtime Skills | Updated: 2026-02-05  
*SRS Trace: §3.2 MCP Integration Layer, §7.2 Phase 2*

## Developer MCP Servers (For YOU – The Engineer)
These MCP servers assist **human developers** in building/maintaining Chimera. They run in your local IDE or dev environment.

| MCP Server | Purpose | Transport | Configuration | SRS Trace |
|------------|--------|----------|---------------|-----------|
| `git-mcp` | Commit/push without leaving IDE; enforce semantic commits | Stdio | Auto-discovers `.git` root; requires GPG signing | §7.2 Phase 2 |
| `filesystem-mcp` | Safe file operations with diff preview before write | Stdio | Root restricted to `C:\TRP1\project-chimera` | §7.2 Phase 2 |
| `tenx-sense-mcp` | Real-time telemetry to Tenx MCP Sense ("Black Box" flight recorder) | SSE | `TENX_API_KEY` from `.env`; **mandatory per Challenge Rules** | Challenge Prerequisite |
| `weaviate-mcp-dev` | Query semantic memory during debugging sessions | HTTP | Points to `http://localhost:8080` (dev Weaviate cluster) | §2.3 Operational Environment |

> 💡 **Why this matters**: These tools let you develop *without* switching contexts—edit files, commit code, and debug agent memory—all through MCP.

## Runtime Skills (For Agents – Not You)
These are **stateless capability packages** the Chimera Agent invokes via Planner. Skills are **thin wrappers** around MCP Tools with strict validation.

### Skill Contract Pattern (Mandatory)
All skills MUST implement this interface:

```python
from pydantic import BaseModel, Field

class BaseSkillInput(BaseModel):
    spec_reference: str = Field(..., pattern=r"^specs/.*\.md §.*$")
    srs_requirement: str = Field(..., pattern=r"^§[0-9]+\.[0-9]+.*$")

class BaseSkillOutput(BaseModel):
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    execution_time_ms: int = Field(..., ge=0)
    spec_compliant: bool = True
```

### Critical Skills Inventory
| Skill Module | Input Contract | Output Contract | MCP Dependencies | SRS Trace |
|--------------|----------------|-----------------|------------------|-----------|
| `skills/trend_fetcher.py` | `topic: str, region: str` | `trends: List[str], relevance_score: float` | `mcp-server-news`, `mcp-server-twitter` | §4.2 FR 2.2 |
| `skills/image_generator.py` | `prompt: str, character_ref_id: str` | `url: str, consistency_score: float` | `mcp-server-ideogram` | §4.3 FR 3.1 |
| `skills/wallet_manager.py` | `to_address: str, amount_usdc: float` | `tx_hash: str, balance_remaining: float` | `mcp-server-coinbase` | §4.5 FR 5.1 |

> ⚠️ **Key Distinction**:  
> - **Developer MCPs** help **you** build the system  
> - **Runtime Skills** are used by **agents** at execution time
