from typing import Any


def summarize_payload(payload: Any) -> dict[str, Any]:
    if isinstance(payload, list):
        sample = payload[:3]
        return {
            "type": "list",
            "count": len(payload),
            "sample": sample,
        }
    if isinstance(payload, dict):
        keys = list(payload.keys())
        return {
            "type": "dict",
            "keys": keys[:10],
            "key_count": len(keys),
        }
    return {"type": type(payload).__name__, "value": str(payload)[:200]}
