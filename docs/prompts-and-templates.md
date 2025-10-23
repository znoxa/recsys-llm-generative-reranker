# Prompts & Templates

- `system_prompt` sets the role and strict JSON output.
- `user_template` combines user context + candidates.
- `stop_words` early‑stop sequences to reduce tokens.

Tips:
- Keep **schema** fixed to ease parsing.
- Normalize numeric features (freshness 0..1, pop 0..1).
- Use short titles and at most 2 attributes per item.
