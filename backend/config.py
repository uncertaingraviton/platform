import os
import yaml
from typing import Any, Dict

CONTEXT_PATH = os.environ.get("CONTEXT_PATH", os.path.join(os.path.dirname(__file__), "context.yaml"))

_context_cache: Dict[str, Any] = {}

def load_context() -> Dict[str, Any]:
    """
    Loads the daily context from context.yaml or context.json.
    Caches the result for fast access.
    """
    global _context_cache
    if _context_cache:
        return _context_cache
    if not os.path.exists(CONTEXT_PATH):
        raise FileNotFoundError(f"Context file not found: {CONTEXT_PATH}")
    with open(CONTEXT_PATH, "r") as f:
        if CONTEXT_PATH.endswith(".yaml") or CONTEXT_PATH.endswith(".yml"):
            context = yaml.safe_load(f)
        elif CONTEXT_PATH.endswith(".json"):
            import json
            context = json.load(f)
        else:
            raise ValueError("Context file must be .yaml, .yml, or .json")
    _context_cache = context
    return context

def get_context() -> Dict[str, Any]:
    """
    Returns the cached context. Loads it if not already loaded.
    """
    return load_context()

def reload_context() -> Dict[str, Any]:
    """
    Forces reload of the context file (for hot reload/admin update).
    """
    global _context_cache
    _context_cache = {}
    return load_context() 