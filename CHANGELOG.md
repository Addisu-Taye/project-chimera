# Changelog

## [Unreleased] - 2026-02-06

- Migrate skill models to Pydantic v2: updated `skills/*` to use `Field`, `field_validator`, and `model_fields`.
- Removed temporary Pydantic v1 `__fields__` compatibility shims and import-time patches.
- Added migration notes to `specs/_meta.md` and a development MCP shim (`mcp_client.py`).
- All tests pass locally; update CI to use Pydantic >=2.
