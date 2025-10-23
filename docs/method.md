# Method: LLM as Generative Re‑Ranker (LLM‑RR)

We treat re‑ranking as a **conditional generation** problem: the LLM receives user/query and candidate summaries and returns a **JSON ranking with rationales**.

## Pipeline
1. Candidate gen returns ~200 items.
2. Truncate to top‑M by popularity/freshness for cost.
3. Build prompt: system + user template + normalized candidate facts.
4. LLM generates JSON list with (item_id, score, rationale).
5. Post‑hoc calibration and diversity re‑ordering (optional).

## Practicalities
- **Token budgeting**: limit text per candidate, cap M, and use **KV‑cache** for system + format instructions.
- **Determinism**: `temperature=0`, `top_p=1`, set seed if provider supports it.
- **Safety**: filter sensitive content both pre‑ and post‑generation.
- **Fallbacks**: if latency or cost budgets are exceeded, short‑circuit to cross‑encoder or linear model.
