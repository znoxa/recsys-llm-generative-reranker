# Offline Evaluation

Run `make eval` to score a small synthetic dataset.

**Metrics**: NDCG@K, MRR, MAP, pairwise accuracy. We also log **tokens** and mock **cost** to visualize trade‑offs.

**Ablations**:
- M (candidates shown to LLM): 20/40/80
- Prompt verbosity: short vs rich facts
- Temperature: 0 vs 0.3
