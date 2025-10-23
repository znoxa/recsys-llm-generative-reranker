from typing import List, Dict

def format_candidates(cands: List[Dict]) -> str:
    parts = []
    for c in cands:
        parts.append(f"- id: {c['item_id']} | title: {c.get('title','')} | fresh: {c.get('freshness',0):.2f} | pop: {c.get('pop',0):.2f}")
    return "\n".join(parts)

def build_prompt(system_prompt: str, user_template: str, user_id: str, query: str, history: str, candidates: List[Dict], k: int) -> str:
    ctx = user_template.format(
        user_id=user_id,
        query=query or "",
        history=history or "(none)",
        candidates_text=format_candidates(candidates[:50]),
        k=k
    )
    return system_prompt + "\n\n" + ctx
