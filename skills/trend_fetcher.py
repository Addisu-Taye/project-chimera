import time
from typing import List

from pydantic import BaseModel, Field, field_validator

from mcp_client import call_tool


class TrendQuery(BaseModel):
    topic: str = Field(..., min_length=1, max_length=100)
    region: str = Field(default="global", pattern=r"^[a-z_]+$")
    timeframe_hours: int = Field(default=24, ge=1, le=168)
    spec_reference: str = Field("specs/functional.md §F-002")
    srs_requirement: str = Field("§4.2 FR 2.2")

    @field_validator("topic", mode="before")
    def topic_must_not_be_blank(cls, v):
        if not v or not str(v).strip():
            raise ValueError("topic must not be empty")
        return v

    def __init__(self, *args, **kwargs):
        # Support legacy positional args: topic, region, timeframe_hours
        field_names = ["topic", "region", "timeframe_hours"]
        for i, val in enumerate(args):
            if i < len(field_names) and field_names[i] not in kwargs:
                kwargs[field_names[i]] = val
        super().__init__(**kwargs)


class TrendResult(BaseModel):
    trends: List[str] = Field(..., min_length=1, max_length=10)
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    confidence_score: float = Field(0.9, ge=0.0, le=1.0)
    execution_time_ms: int = Field(0, ge=0)
    spec_compliant: bool = Field(True)

    def __init__(self, *args, **kwargs):
        # Support legacy positional args: trends, relevance_score, confidence_score, execution_time_ms, spec_compliant
        field_names = [
            "trends",
            "relevance_score",
            "confidence_score",
            "execution_time_ms",
            "spec_compliant",
        ]
        for i, val in enumerate(args):
            if i < len(field_names) and field_names[i] not in kwargs:
                kwargs[field_names[i]] = val
        super().__init__(**kwargs)


async def execute(query: TrendQuery) -> TrendResult:
    """Minimal implementation to satisfy spec-driven tests.

    This is intentionally lightweight: it returns stubbed trends,
    sets confidence/relevance values within valid ranges, and
    records a small execution_time_ms.
    """
    start = time.time()
    # Call MCP tool to fetch trends (development shim)
    resp = await call_tool(
        "fetch_trends",
        {
            "topic": query.topic,
            "region": query.region,
            "timeframe_hours": query.timeframe_hours,
        },
    )
    execution_time_ms = int((time.time() - start) * 1000)
    return TrendResult(
        trends=resp.get("trends", []),
        relevance_score=resp.get("relevance_score", 0.0),
        confidence_score=resp.get("confidence_score", 0.0),
        execution_time_ms=max(execution_time_ms, resp.get("execution_time_ms", 0)),
        spec_compliant=resp.get("spec_compliant", True),
    )
