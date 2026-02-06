"""Minimal MCP client shim used by skills.

This file provides `call_tool(name, params)` as an async entrypoint.
Replace or extend with a real MCP client that performs authenticated calls
to your MCP server(s) in production.
"""

import asyncio
import secrets
from typing import Any, Dict


async def call_tool(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Simulated MCP tool dispatcher.

    For development/tests this returns deterministic, spec-compliant
    responses for known tool names. Replace this with the real client
    implementation that talks to downstream MCP servers.
    """
    # Simulate network latency
    await asyncio.sleep(0.01)

    if tool_name == "fetch_trends":
        topic = params.get("topic", "unknown")
        return {
            "trends": [f"{topic} trend A", f"{topic} trend B"],
            "relevance_score": 0.8,
            "confidence_score": 0.9,
            "execution_time_ms": 10,
            "spec_compliant": True,
        }

    if tool_name == "generate_image":
        char_id = params.get("character_ref_id") or "0" * 32
        token = secrets.token_hex(8)
        consistency = min(1.0, max(0.0, len(params.get("prompt", "")) / 200.0))
        return {
            "url": f"https://cdn.example.com/images/{char_id}/{token}.jpg",
            "consistency_score": consistency,
            "confidence_score": 0.9,
            "execution_time_ms": 20,
            "spec_compliant": consistency >= 0.85,
        }

    if tool_name == "cfo_check":
        # Basic allowed/denied response for budget checks
        amount = params.get("amount_usdc", 0.0)
        current = params.get("current_spend", 0.0)
        max_limit = params.get("max_daily_limit", 10000.0)
        allowed = (current + amount) <= max_limit
        return {
            "allowed": allowed,
            "current_spend": current,
            "max_daily_limit": max_limit,
        }

    if tool_name == "post_transaction":
        tx_hash = "0x" + secrets.token_hex(32)
        return {
            "tx_hash": tx_hash,
            "confirmed": True,
            "gas_used": 21000,
            "execution_time_ms": 30,
        }

    # Default: echo back for unknown tools
    return {"ok": True, "tool": tool_name, "params": params}
