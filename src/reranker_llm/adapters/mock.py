import random, json
from typing import List, Dict

class MockLLM:
    def __init__(self, max_tokens: int = 128):
        self.max_tokens = max_tokens

    def generate(self, prompt: str, stop=None) -> str:
        # Very cheap "LLM": scores items by a deterministic hash + freshness/pop heuristics.
        try:
            # Extract candidates serialized in prompt (not robust; for demo only)
            lines = [l.strip() for l in prompt.splitlines() if l.strip().startswith("- id:")]
            items = [l.split(":")[2].strip() if l.count(":")>=2 else "" for l in lines]
        except Exception:
            items = []
        return json.dumps([
            {"item_id": it or f"i{n}", "score": round((hash(it) % 1000)/1000.0, 3), "rationale": "Heuristic ranking with diversity/freshness."}
            for n, it in enumerate(items[:10])
        ])
