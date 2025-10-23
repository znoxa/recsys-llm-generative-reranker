from dataclasses import dataclass
from typing import Any, Dict
import yaml

@dataclass
class Settings:
    raw: Dict[str, Any]

    @classmethod
    def from_file(cls, path: str) -> "Settings":
        with open(path, "r", encoding="utf-8") as f:
            return cls(raw=yaml.safe_load(f))

    def get(self, key: str, default=None):
        cur = self.raw
        for p in key.split("."):
            if not isinstance(cur, dict) or p not in cur:
                return default
            cur = cur[p]
        return cur
