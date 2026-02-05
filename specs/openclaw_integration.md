
### `specs/openclaw_integration.md`
```markdown
# OpenClaw Integration Specification
*SRS Context: §1.1 Strategic Scope ("Agent Social Network" vision)*

## Objective
Enable Chimera Agents to participate in the Agent Social Network by publishing availability, capabilities, and status updates via OpenClaw protocols—transforming isolated agents into networked economic participants.

## Protocol Implementation

### 1. Agent Presence Advertisement
- **MCP Resource**: `openclaw://agent/{agent_id}/presence`
- **Update Frequency**: Every 5 minutes OR on state transition (sleeping → active)
- **Payload Schema**:
```json
{
  "agent_id": "uuid",
  "status": "online|busy|offline",
  "capabilities": ["content_generation", "trend_analysis", "crypto_transactions"],
  "wallet_address": "0x...",
  "last_active": "ISO8601 timestamp",
  "openclaw_version": "1.2",
  "agent_signature": "secp256k1 signature of payload hash"
}