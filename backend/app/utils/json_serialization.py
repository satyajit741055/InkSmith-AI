def _make_json_serializable(obj):
    """Recursively convert Pydantic models and other objects to JSON-safe types."""
    if isinstance(obj, BaseModel):
        return _make_json_serializable(obj.model_dump())
    if isinstance(obj, dict):
        return {k: _make_json_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_make_json_serializable(v) for v in obj]
    return obj