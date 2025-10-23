import hashlib, yaml
from typing import Dict, Any

class ABRouter:
    def __init__(self, salt: str):
        self.salt = salt

    def bucket(self, user_id: str, exp_name: str, percent: int) -> bool:
        h = int(hashlib.sha1((self.salt+exp_name+user_id).encode()).hexdigest(),16)%100
        return h < percent
