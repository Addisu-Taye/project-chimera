from pydantic import BaseModel, Field, field_validator
import time
from mcp_client import call_tool


class ImageRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=1000)
    character_ref_id: str = Field(..., pattern=r"^[a-f0-9]{32}$")
    style_preset: str = Field(default="influencer", pattern=r"^[a-z_]+$")
    spec_reference: str = Field('specs/functional.md §F-003')
    srs_requirement: str = Field('§4.3 FR 3.1')

    @field_validator('prompt', mode='before')
    def prompt_non_empty(cls, v):
        if not v or not str(v).strip():
            raise ValueError('prompt must not be empty')
        return v


class ImageResult(BaseModel):
    url: str
    consistency_score: float = Field(..., ge=0.0, le=1.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    execution_time_ms: int = Field(..., ge=0)
    spec_compliant: bool = Field(True)


async def execute(request: ImageRequest) -> ImageResult:
    start = time.time()
    # Call MCP image generator tool with retries per spec (max 3)
    max_retries = 3
    attempt = 0
    last_resp = None
    while attempt < max_retries:
        attempt += 1
        resp = await call_tool('generate_image', {
            'prompt': request.prompt,
            'character_ref_id': request.character_ref_id,
            'style_preset': request.style_preset,
        })
        last_resp = resp
        consistency = resp.get('consistency_score', 0.0)
        if consistency >= 0.85:
            break
    execution_time_ms = int((time.time() - start) * 1000)
    url = last_resp.get('url', '') if last_resp else ''
    spec_compliant = last_resp.get('spec_compliant', False) if last_resp else False
    return ImageResult(
        url=url,
        consistency_score=last_resp.get('consistency_score', 0.0) if last_resp else 0.0,
        confidence_score=last_resp.get('confidence_score', 0.0) if last_resp else 0.0,
        execution_time_ms=max(execution_time_ms, last_resp.get('execution_time_ms', 0) if last_resp else 0),
        spec_compliant=spec_compliant,
    )
