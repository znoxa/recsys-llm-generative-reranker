# Latency & Cost Controls

- **Pre‑filter** candidates (M ≪ 200).
- **Compact** candidate lines to ≤ 120 chars.
- **KV‑cache pooling** for system prompt.
- **Stop words** to halt decoding after JSON array.
- **Token accounting** to enforce budgets per request.
- **Batching** across requests if provider supports it.
