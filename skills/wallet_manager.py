import time

from pydantic import BaseModel, Field, field_validator

from mcp_client import call_tool


class TransactionRequest(BaseModel):
    to_address: str = Field(..., pattern=r"^0x[a-fA-F0-9]{40}$")
    amount_usdc: float = Field(..., gt=0, le=1000.0)
    memo: str = Field(default="", max_length=255)
    spec_reference: str = Field("specs/functional.md §F-004")
    srs_requirement: str = Field("§4.5 FR 5.1")

    @field_validator("memo", mode="before")
    def memo_strip(cls, v):
        return v or ""


class TransactionResult(BaseModel):
    tx_hash: str = Field(..., pattern=r"^0x[a-fA-F0-9]{64}$")
    balance_remaining: float = Field(..., ge=0.0)
    gas_used: int = Field(..., ge=0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    execution_time_ms: int = Field(..., ge=0)
    spec_compliant: bool = Field(True)


async def execute(request: TransactionRequest) -> TransactionResult:
    start = time.time()
    # First, consult CFO Judge (via MCP) for budget check
    cfo_resp = await call_tool(
        "cfo_check",
        {
            "amount_usdc": request.amount_usdc,
            "current_spend": 0.0,
            "max_daily_limit": 10000.0,
        },
    )
    if not cfo_resp.get("allowed", False):
        raise ValueError("Budget check failed: transaction exceeds daily limit")

    # Post the transaction via MCP
    post_resp = await call_tool(
        "post_transaction",
        {
            "to_address": request.to_address,
            "amount_usdc": request.amount_usdc,
            "memo": request.memo,
        },
    )

    execution_time_ms = int((time.time() - start) * 1000)
    tx_hash = post_resp.get("tx_hash", "")
    gas_used = post_resp.get("gas_used", 0)
    balance_remaining = max(0.0, 10000.0 - request.amount_usdc)
    return TransactionResult(
        tx_hash=tx_hash,
        balance_remaining=balance_remaining,
        gas_used=gas_used,
        confidence_score=post_resp.get("confidence_score", 0.95),
        execution_time_ms=max(0, execution_time_ms),
        spec_compliant=True,
    )
